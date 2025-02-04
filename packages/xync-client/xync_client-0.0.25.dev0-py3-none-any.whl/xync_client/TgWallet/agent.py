from asyncio import run
from enum import StrEnum

from x_model import init_db, HTTPException, FailReason
from xync_schema import models

from xync_client.TgWallet.pyd import (
    Banks,
    FiatEpyd,
    Attrs,
    AttrsV2,
    MyAdEPydSale,
    MyAdEPydPurchase,
    AdEpydInPurchase,
    AdEpydInSale,
    AdEPyd,
)
from xync_client.loader import PG_DSN
from xync_schema.enums import AdStatus

from xync_client.Abc.Base import ListOfDicts
from xync_client.TgWallet.auth import AuthClient
from xync_schema.models import Cur, Coin, OrderStatus, Pmex, Fiat, Ad, Pmcur, Fiatex, Pm, FiatBank, PmexBank, Agent
from xync_schema.pydantic import FiatNew

from xync_client.Abc.Agent import BaseAgentClient
from xync_client.TgWallet.ex import ExClient
from xync_client.pyd import FiatXn


class Exceptions(StrEnum):
    PM_KYC = "OFFER_FIAT_COUNTRY_NOT_SUPPORTED_BY_USER_KYC_COUNTRY"


# class Status(IntEnum):
#     ALL_ACTIVE = OrderStatus.active


class AgentClient(BaseAgentClient, AuthClient):
    def pm_type_map(self, pm: Pm) -> str:
        return "V2" if pm.name.startswith("SBP") else "V1"

    # 0: Получение ордеров в статусе status, по монете coin, в валюте coin, в направлении is_sell
    async def orders(
        self, status: OrderStatus = OrderStatus.created, coin: Coin = None, cur: Cur = None, is_sell: bool = None
    ) -> ListOfDicts:
        order = await self._post(
            "/p2p/public-api/v2/offer/order/history/get-by-user-id",
            {"offset": 0, "limit": 100, "filter": {"status": "ALL_ACTIVE"}},  # "limit": 20
        )
        return order["data"]

    # 0: Получение ордера по ид
    async def settings(self) -> ListOfDicts:
        settings = await self._post("/p2p/public-api/v2/offer/settings/get")
        return settings["data"]

    # 0: Получение ордера по ид
    async def order(self, oid) -> ListOfDicts:
        orders = await self._post("/p2p/public-api/v2/offer/order/get", {"orderId": oid})
        return orders["data"]

    # 1: [T] Запрос на старт сделки
    async def order_request(self, ad_id: int, amount: float) -> dict | bool:
        await self.agent.fetch_related("ex", "ex__agents")
        ex_client: ExClient = self.agent.ex.client()
        ad: AdEPyd = await ex_client._get_ad(offer_id=ad_id)
        fiats = await self.my_fiats()
        fiats_pms = {fiat["paymentMethod"]["code"]: fiat["id"] for fiat in fiats.values()}
        if not (pms := ad.get("paymentMethods")):
            print(ad)
        ad_pms = [pm["code"] for pm in pms]
        result = list(set(fiats_pms.keys()) & set(ad_pms))
        if not result:
            return False
        pid = result[0]
        request = await self._post(
            "/p2p/public-api/v2/offer/order/create-by-amount",
            {
                "offerId": ad_id,
                "paymentDetailsId": fiats_pms[pid],
                "amount": {"currencyCode": ad["orderAmountLimits"]["currencyCode"], "amount": amount},
                "type": ad["type"],
            },
            "data",
        )
        confirm = await self._post(
            "/p2p/public-api/v2/offer/order/confirm", {"orderId": request["id"], "type": ad["type"]}
        )
        #
        await Ad.get(id=ad_id).prefetch_related("agent")
        # inagent_client: InAgentClient = maker.in_client()
        # task = inagent_client.li
        # asyncio.get_running_loop().create_task()
        return confirm

    # # # FIATS # # #
    def fiat_args2ex_pyd(
        self, exid: int | str, cur: str, detail: str, name: str, fid: int, typ: str, extra=None
    ) -> FiatEpyd:
        fiat = self.fiat_pyd(
            paymentMethodCode=exid,
            currencyCode=cur,
            name=name,
            attributes=Attrs(
                version=typ,
                values=[Attrs.KeyVal(name={"V1": "PAYMENT_DETAILS_NUMBER", "V2": "PHONE"}[typ], value=detail)],
            ),
        )
        if typ == "V2":
            assert issubclass(extra, list) and extra, "extra should not be empty on V2 type"
            fiat.attributes.values.append(
                AttrsV2.KeyVal(
                    name="BANKS",
                    value=extra,  # ["bank1", "bank2"]
                )
            )
        return fiat

    @staticmethod
    def fiat_args2upsert(exid: int | str, cur: str, detail: str, name: str, fid: int = None) -> dict:
        return {
            **({"id": fid} if fid else {}),
            "paymentMethodCode": exid,
            "currencyCode": cur,
            "name": name,
            "attributes": {"version": "V1", "values": [{"name": "PAYMENT_DETAILS_NUMBER", "value": detail}]},
        }

    # 25: Список реквизитов моих платежных методов
    async def fiats(self, _cur: Cur = None) -> list[FiatEpyd]:
        resp = await self._post("/p2p/public-api/v3/payment-details/get/by-user-id")
        return [FiatEpyd(**fiat) for fiat in resp["data"]]

    async def fiat_epyd2xpyd(self, fiat: FiatEpyd) -> FiatXn:
        if not (pmex := await Pmex.get_or_none(exid=fiat.paymentMethod.code, ex=self.agent.ex)):
            raise HTTPException(FailReason.body, f"No Pmex {fiat.paymentMethod.code} on ex#{self.agent.ex.name}", 404)
        if not (pmcur := await Pmcur.get_or_none(cur__ticker=fiat.currency, pm_id=pmex.pm_id)):
            raise HTTPException(
                FailReason.body, f"No Pmcur with cur#{fiat.currency} and pm#{fiat.paymentMethod.code}", 404
            )
        ftx = FiatXn(
            id=fiat.id,
            detail="",
            name=fiat.name,
            amount=0,
            user_id=self.agent.user_id,
            pmcur_id=pmcur.id,
        )
        for val in fiat.attributes.values:
            if val.name != "BANKS":
                ftx.detail = val.value
            else:
                val: Banks
                ftx.banks = [b.code for b in val.value]
        return ftx

    # 25: Список реквизитов моих платежных методов
    async def set_fiatexs(self) -> list[Fiatex]:
        fiat_epyds = await self.fiats()
        fiat_xpyds: list[FiatXn] = [await self.fiat_epyd2xpyd(f) for f in fiat_epyds]
        fxs: list[Fiatex] = []
        for fx in fiat_xpyds:
            df, unq = fx.args()
            fiat_db, _ = await Fiat.update_or_create(df, **unq)
            fiatex_db, _ = await Fiatex.update_or_create(exid=fx.id, ex=self.agent.ex, fiat=fiat_db)
            for bn in fx.banks:
                bank = await PmexBank.get(exid=bn)
                b, _ = await FiatBank.get_or_create(fiat=fiat_db, pmexbank=bank)
            fxs.append(fiatex_db)
        return fxs

    # 26: Создание реквизита моего платежного метода
    async def fiat_new(self, fiat: FiatNew) -> Fiat:
        pmex, _ = await Pmex.get_or_create(pm_id=fiat.pm_id, ex=self.agent.ex)  # .prefetch_related('pm')
        cur = await Cur[fiat.cur_id]
        add_fiat = await self._post(
            "/p2p/public-api/v3/payment-details/create",
            {
                "paymentMethodCode": pmex.exid,
                "currencyCode": cur.ticker,
                "name": fiat.name,
                "attributes": {"version": "V1", "values": [{"name": "PAYMENT_DETAILS_NUMBER", "value": fiat.detail}]},
            },
        )
        pmex = await Pmex.get(exid=add_fiat["data"]["paymentMethod"]["code"], ex=self.agent.ex)
        cur = await Cur.get(ticker=add_fiat["data"]["currency"])
        pmcur, _ = await Pmcur.get_or_create(cur=cur, pm_id=pmex.pm_id)
        attrs = {a["name"]: a["value"] for a in add_fiat["data"]["attributes"]["values"]}
        f, _ = await Fiat.update_or_create(
            {"detail": attrs["PAYMENT_DETAILS_NUMBER"]}, pmcur=pmcur, user_id=self.agent.user_id
        )
        await Fiatex.update_or_create({"exid": add_fiat["data"]["id"]}, ex=self.agent.ex, fiat=f)
        return f

    # 27: Редактирование реквизита моего платежного метода
    async def fiat_upd(self, fiat_id: int, detail: str, name: str = None) -> Fiat:
        fiat = await Fiat.get(fiatexs__exid=fiat_id, fiatexs__ex=self.agent.ex).prefetch_related("pmcur")
        pmex = await Pmex.get(pm_id=fiat.pmcur.pm_id, ex=self.agent.ex)
        cur = await Cur[fiat.pmcur.cur_id]
        edit_fiat = await self._post(
            "/p2p/public-api/v3/payment-details/edit",
            {
                "id": fiat_id,
                "paymentMethodCode": pmex.exid,
                "currencyCode": cur.ticker,
                "name": name,
                "attributes": {"version": "V1", "values": [{"name": "PAYMENT_DETAILS_NUMBER", "value": detail}]},
            },
        )
        pmex = await Pmex.get(exid=edit_fiat["data"]["paymentMethod"]["code"], ex=self.agent.ex)
        cur = await Cur.get(ticker=edit_fiat["data"]["currency"])
        pmcur, _ = await Pmcur.get_or_create(cur=cur, pm_id=pmex.pm_id)
        attrs = {a["name"]: a["value"] for a in edit_fiat["data"]["attributes"]["values"]}
        f, _ = await Fiat.update_or_create(
            {"detail": attrs["PAYMENT_DETAILS_NUMBER"]}, pmcur=pmcur, user_id=self.agent.user_id
        )
        await Fiatex.update_or_create({"exid": edit_fiat["data"]["id"]}, ex=self.agent.ex, fiat=f)
        return f

    # 28: Удаление реквизита моего платежного метода
    async def fiat_del(self, fiat_id: int) -> bool:
        del_fiat = await self._post("/p2p/public-api/v3/payment-details/delete", {"id": fiat_id})
        return del_fiat

    # 29: Список моих объявлений
    async def my_ads(self, status: AdStatus = None) -> ListOfDicts:
        mapping = {AdStatus.defActive: "INACTIVE", AdStatus.active: "ACTIVE"}
        ads = await self._post(
            "/p2p/public-api/v2/offer/user-own/list",
            {"offset": 0, "limit": 20},  # , "offerType": "SALE"|"PURCHASE"
        )
        return (
            [
                MyAdEPydSale(**ad) if ad["type"] == "SALE" else MyAdEPydPurchase(**ad)
                for ad in ads["data"]
                if not status or (status and ad["status"] == mapping[status])
            ]
            if status
            else ads["data"]
        )

    # 30: Создание объявления
    async def ad_new(self, ad: AdEpydInPurchase | AdEpydInSale) -> Ad:
        # coin: Coin,
        # cur: str,
        # is_sell: bool,
        # fiats: list[Fiat],
        # amount: str,
        # price: str,
        # min_fiat: str,
        # is_float: bool = False,
        # details: str = None,
        # autoreply: str = None,
        # status: AdStatus = AdStatus.active,
        # ) -> Ad.pyd():
        dct = {
            "type": typ,
            "initVolume": {"currencyCode": coin, "amount": amount},
            "orderRoundingRequired": True,
            "price": {
                "type": "FLOATING" if is_float else "FIXED",
                "baseCurrencyCode": coin,
                "quoteCurrencyCode": cur,
                "value": price,
            },
            "orderAmountLimits": {"min": min_fiat},
            "paymentConfirmTimeout": "PT15M",
            "comment": "",  # todo: real recipient name
            "paymentMethodCodes": fiats,
        }
        if is_sell:
            dct["paymentDetailsIds"] = [f.id for f in fiats]
        else:
            pm_ids = [f.pmcur.pm_id for f in fiats]
            pmexs = await Pmex.filter(ex=self.agent.ex, pm_id__in=pm_ids)
            dct["paymentMethodCodes"] = [pmex.exid for pmex in pmexs]

        create = await self._post(
            "/p2p/public-api/v2/offer/create",
            {
                "type": typ,
                "initVolume": {"currencyCode": coin.ticker, "amount": f"{amount}"},
                "orderRoundingRequired": False,
                "price": {
                    "type": "FLOATING" if is_float else "FIXED",
                    "baseCurrencyCode": coin.ticker,
                    "quoteCurrencyCode": cur,
                    "value": price,
                },
                "orderAmountLimits": {"min": min_fiat},
                "paymentConfirmTimeout": "PT15M" if is_sell else "PT3H",
                "comment": "",
                "paymentDetailsIds": fiats,
            },
        )
        return create

    async def _get_my_ad(self, offer_id: int):
        get_own = await self._post("/p2p/public-api/v2/offer/get-user-own/", {"offerId": offer_id})
        return get_own["data"]

    # 31: Редактирование объявления
    async def ad_upd(
        self,
        offer_id: int,
        amount: int,
        fiats: list[Fiat] = None,
        price: float = None,
        is_float: bool = None,
        min_fiat: int = None,
        details: str = None,
        autoreply: str = None,
        status: AdStatus = None,
    ) -> Ad.pyd():
        ad = await self._get_my_ad(offer_id)

        upd = await self._post(
            "/p2p/public-api/v2/offer/edit",
            {
                "offerId": offer_id,
                "paymentConfirmTimeout": ad["paymentConfirmTimeout"],
                "type": ad["type"],
                "orderRoundingRequired": False,
                "price": {"type": "FIXED", "value": ad["price"]["value"]},
                "orderAmountLimits": {"min": ad["orderAmountLimits"]["min"]},
                "comment": "",  # TODO: comment
                "volume": f"{amount}",
                "paymentDetailsIds": [a["id"] for a in ad["paymentDetails"]],
            },
        )
        return upd

    # 32: Удаление
    async def ad_del(self, offer_id: int) -> bool:
        ad = await self._get_my_ad(offer_id)
        ad_del = await self._post("/p2p/public-api/v2/offer/delete", {"type": ad["type"], "offerId": offer_id})
        return ad_del["status"] == "SUCCESS"

    # 33: Вкл/выкл объявления
    async def ad_switch(self, offer_id: int, active: bool) -> bool:
        ad = await self._get_my_ad(offer_id)
        pre = "" if active else "de"
        switch = await self._post(f"/p2p/public-api/v2/offer/{pre}activate", {"type": ad["type"], "offerId": offer_id})
        return switch["status"] == "SUCCESS"

    # 34: Вкл/выкл всех объявлений
    async def ads_switch(self, active: bool) -> bool:
        pre = "enable" if active else "disable"
        switch = await self._post(f"/p2p/public-api/v2/user-settings/{pre}-bidding")
        return switch["status"] == "SUCCESS"

    # 35: Получить объект юзера по его ид
    async def get_user(self, user_id: int = None, offer_id: int = None) -> dict:
        user = await self._post("/p2p/public-api/v2/offer/get", {"offerId": offer_id})
        return user["data"]["user"]

    # 36: Отправка сообщения юзеру с приложенным файлом
    async def send_user_msg(self, msg: str, file=None) -> bool:
        pass

    # 37: (Раз)Блокировать юзера
    async def block_user(self, is_blocked: bool = True) -> bool:
        return None

    # 38: Поставить отзыв юзеру
    async def rate_user(self, positive: bool) -> bool:
        return None

    # base_url = 'https://p2p.walletbot.me'
    # middle_url = '/p2p/'

    # 19 - order_paid
    async def order_paid(self, order_id: str, file: dict):
        paid = await self._post(
            "/p2p/public-api/v2/offer/order/confirm-sending-payment", {"orderId": order_id, "paymentReceipt": file}
        )
        return paid


async def main():
    await init_db(PG_DSN, models, True)
    agents = await Agent.filter(ex_id=34, auth__isnull=False).order_by("user_id").prefetch_related("ex")
    my, taker, maker = agents
    mycl, tcl, mcl = my.client(), taker.client(), maker.client()

    await mycl.set_fiatexs()
    await mycl.my_ads()

    await Coin.get(ticker="USDT")
    await Fiat.filter(user_id=taker.user_id)
    await Fiat.filter(user_id=maker.user_id)
    # fiatex = await Fiatex.get(exid=my_fiat['id']).prefetch_related('fiat')
    # ad = await tcl.ad_new(
    #     coin=coin, cur=fiatex.fiat.currency, is_sell=True, fiats=[mf.pmcur for mf in maker_fiats], amount="10", price="120", min_fiat="500", is_float=True
    # )
    # ad: AdPyd = AdPyd(**ad["data"])
    # print(ad)
    await tcl.close(), await mcl.close()


if __name__ == "__main__":
    run(main())

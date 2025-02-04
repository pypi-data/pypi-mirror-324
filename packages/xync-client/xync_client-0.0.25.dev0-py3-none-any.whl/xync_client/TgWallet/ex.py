from asyncio import run
from x_model import init_db
from xync_client.pyd import PmXpyd, AdInXpyd

from xync_schema import models
from xync_schema.models import Ex, Agent, Direction, Pair, Coin, Cur

from xync_client.TgWallet.pyd import AdFullEpyd, AdEpyd
from xync_client.loader import PG_DSN
from xync_client.Abc.Ex import BaseExClient
from xync_client.Abc.Base import FlatDict, DictOfDicts, MapOfIdsList
from xync_client.TgWallet.auth import AuthClient


class ExClient(BaseExClient, AuthClient):
    def __init__(self, ex: Ex):  # ex should be with fetched .agents
        self.agent: Agent = [ag for ag in ex.agents if ag.auth][0]  # need for AuthTrait
        super().__init__(ex)  # , "host_p2p"

    # 19: Список поддерживаемых валют тейкера
    async def curs(self) -> FlatDict:
        coins_curs = await self._post("/p2p/public-api/v2/currency/all-supported")
        return {c["code"]: c["code"] for c in coins_curs["data"]["fiat"]}

    async def _pms(self, cur: str) -> dict[str, PmXpyd]:
        pms = await self._post("/p2p/public-api/v3/payment-details/get-methods/by-currency-code", {"currencyCode": cur})
        return {pm["code"]: PmXpyd(name=pm["nameEng"], banks=pm.get("banks")) for pm in pms["data"]}

    # 20: Список платежных методов
    async def pms(self, cur: str = None) -> DictOfDicts:
        if cur:
            return await self._pms(cur)
        pms = {}
        for cur in await self.curs():
            pms |= await self._pms(cur)
        return pms

    # 21: Список платежных методов по каждой валюте
    async def cur_pms_map(self) -> MapOfIdsList:
        return {cur: list(await self._pms(cur)) for cur in await self.curs()}

    # 22: Список торгуемых монет (с ограничениям по валютам, если есть)
    async def coins(self) -> FlatDict:
        coins_curs = await self._post("/p2p/public-api/v2/currency/all-supported")
        return {c["code"]: c["code"] for c in coins_curs["data"]["crypto"]}

    # 23: Список пар валюта/монет
    async def pairs(self) -> MapOfIdsList:
        coins = await self.coins()
        curs = await self.curs()
        pairs = {cur: set(coins.values()) for cur in curs.values()}
        return pairs

    async def _get_ad(self, offer_id: int) -> AdFullEpyd:
        get_ad = await self._post("/p2p/public-api/v2/offer/get", {"offerId": offer_id})
        return AdFullEpyd(**get_ad["data"])

    # 24: Список объяв по (buy/sell, cur, coin, pm)
    async def ads(
        self, coin_exid: str, cur_exid: str, is_sell: bool, pm_exids: list[str | int] = None, amount: int = None
    ) -> list[AdEpyd]:
        params = {
            "baseCurrencyCode": coin_exid,
            "quoteCurrencyCode": cur_exid,
            "offerType": "SALE" if is_sell else "PURCHASE",
            "offset": 0,
            "limit": 100,
            # "merchantVerified": "TRUSTED"
        }
        ads = await self._post("/p2p/public-api/v2/offer/depth-of-market/", params, "data")
        return [AdEpyd(**ad) for ad in ads]

    async def ad_epyd2xpyd(self, ad: AdEpyd | AdFullEpyd) -> AdInXpyd:
        coin = await Coin.get_or_create_by_name(ad.price.baseCurrencyCode)
        cur = await Cur.get_or_create_by_name(ad.price.quoteCurrencyCode)
        pair, _ = await Pair.get_or_create(coin=coin, cur=cur, ex=self.ex)
        dr, _ = await Direction.get_or_create(pair=pair, sell=ad.is_sell)
        maker, _ = await Agent.get_or_create(exid=ad.user.userId, ex=self.ex)
        adx = AdInXpyd(
            id=ad.id,
            price=ad.price.value,
            minFiat=ad.orderAmountLimits.min,
            maxFiat=ad.orderAmountLimits.max,
            direction_id=dr.id,
            agent_id=maker.id,
            detail=getattr(ad, "comment", None),
        )
        return adx


async def test():
    await init_db(PG_DSN, models, True)
    tgex = await Ex.get(name="TgWallet").prefetch_related("agents", "agents__ex")
    cl: ExClient = tgex.client()
    await cl.set_pmcurexs()
    await cl.set_coinexs()
    ads: list[AdEpyd] = await cl.ads("USDT", "RUB", False)
    ad: AdFullEpyd = await cl._get_ad(ads[0].id)
    adx: AdInXpyd = await cl.ad_epyd2xpyd(ad)
    await cl.set_ad(adx)
    ad: AdEpyd = ads[1]
    adx: AdInXpyd = await cl.ad_epyd2xpyd(ad)
    await cl.set_ad(adx)
    await cl.close()


if __name__ == "__main__":
    run(test())

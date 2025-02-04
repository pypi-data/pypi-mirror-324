from abc import abstractmethod

from pydantic import BaseModel
from tortoise.exceptions import IntegrityError
from x_model import HTTPException, FailReason

from xync_client.Abc.Base import BaseClient
from xync_client.Abc.Ex import ListOfDicts

from xync_client.Abc.AuthTrait import BaseAuthTrait
from xync_schema.models import OrderStatus, Coin, Cur, Ad, AdStatus, Fiat, Agent, Pmex, Pmcur, Fiatex
from xync_schema.pydantic import FiatNew, FiatUpd


class BaseAgentClient(BaseClient, BaseAuthTrait):  # todo: inherit form Base or from Ex Client?
    def __init__(self, agent: Agent):
        self.agent: Agent = agent
        # self.ex_client: BaseExClient = agent.ex.client()  # todo: really need?
        super().__init__(agent.ex)  # , "host_p2p"

    @abstractmethod
    def pm_type_map(self, type_: Pmex) -> str: ...

    @abstractmethod
    async def start_listen(self) -> bool: ...

    # 0: Получшение ордеров в статусе status, по монете coin, в валюте coin, в направлении is_sell: bool
    @abstractmethod
    async def get_orders(
        self, status: OrderStatus = OrderStatus.created, coin: Coin = None, cur: Cur = None, is_sell: bool = None
    ) -> ListOfDicts: ...

    # 3N: [T] - Уведомление об одобрении запроса на сделку
    @abstractmethod
    async def request_accepted_notify(self) -> int: ...  # id

    # 1: [T] Запрос на старт сделки
    @abstractmethod
    async def order_request(self, ad_id: int, amount: float) -> dict: ...

    # async def start_order(self, order: Order) -> OrderOutClient:
    #     return OrderOutClient(self, order)

    # 1N: [M] - Запрос мейкеру на сделку
    @abstractmethod
    async def order_request_ask(self) -> dict: ...  # , ad: Ad, amount: float, pm: Pm, taker: Agent

    # 2N: [M] - Уведомление об отмене запроса на сделку
    @abstractmethod
    async def request_canceled_notify(self) -> int: ...  # id

    # # # Fiat
    async def _fiat_pyd2args(
        self, fiat: FiatNew | FiatUpd
    ) -> tuple[int | str, str, str, str, str]:  # exid,cur,dtl,name,typ
        if not (pmex := await Pmex.get_or_none(ex=self.agent.ex, pm_id=fiat.pm_id).prefetch_related("pm")):
            # if no such pm on this ex - update ex.pms
            # _res = await self.ex_client.set_pmcurexs()
            _res = await self.agent.ex.client().set_pmcurexs()
            # and then get this pm again
            pmex = await Pmex.get(ex=self.agent.ex, pm_id=fiat.pm_id).prefetch_related("pm")
        cur = await Cur[fiat.cur_id]
        return pmex.exid, cur.ticker, fiat.detail, fiat.name or pmex.name, self.pm_type_map(pmex)

    async def fiat_new_pyd2args(
        self, fiat: FiatNew
    ) -> tuple[int | str, str, str, str, str, None]:  # exid,cur,dtl,name,typ
        return await self._fiat_pyd2args(fiat) + (None,)

    async def fiat_upd_pyd2args(
        self, fiat: FiatNew, fid: int
    ) -> tuple[int | str, str, str, str, str, int]:  # *new_p2args,id
        return await self._fiat_pyd2args(fiat) + (fid,)

    @property
    @abstractmethod
    def fiat_pyd(self) -> BaseModel.__class__: ...

    @abstractmethod
    def fiat_args2pyd(
        self, exid: int | str, cur: str, detail: str, name: str, fid: int, typ: str, extra=None
    ) -> fiat_pyd: ...

    # 25: Список реквизитов моих платежных методов
    @abstractmethod
    async def fiats(self, cur: Cur = None) -> ListOfDicts: ...  # {fiat.exid: {fiat}}

    @staticmethod
    async def fiat_pyd2db(fiat_pyd: FiatNew | FiatUpd, uid: int, fid: int = None) -> tuple[Fiat, bool]:
        if not (pmcur := await Pmcur.get_or_none(cur_id=fiat_pyd.cur_id, pm_id=fiat_pyd.pm_id)):
            raise HTTPException(FailReason.body, f"No Pmcur with cur#{fiat_pyd.cur_id} and pm#{fiat_pyd.pm_id}", 404)
        df = {"detail": fiat_pyd.detail, "name": fiat_pyd.name, "amount": fiat_pyd.amount, "target": fiat_pyd.target}
        unq = {"pmcur": pmcur, "user_id": uid}
        if fid:
            unq["id"] = fid
        try:
            return await Fiat.update_or_create(df, **unq)
        except IntegrityError as e:
            raise HTTPException(FailReason.body, e)

    # 26: Создание реквизита моего платежного метода
    @abstractmethod
    async def fiat_new(self, fiat: FiatNew) -> Fiatex:
        fiat_db: Fiat = (await self.fiat_pyd2db(fiat, self.agent.user_id))[0]
        if not (fiatex := Fiatex.get_or_none(fiat=fiat_db, ex=self.agent.ex)):
            fiatex, _ = Fiatex.update_or_create({}, fiat=fiat_db, ex=self.agent.ex)
        return fiatex

    # 27: Редактирование реквизита моего платежного метода
    @abstractmethod
    async def fiat_upd(self, fiat_id: int, detail: str, name: str = None) -> Fiat: ...

    # 28: Удаление реквизита моего платежного метода
    @abstractmethod
    async def fiat_del(self, fiat_id: int) -> bool: ...

    # # # Ad
    # 29: Список моих объявлений
    @abstractmethod
    async def my_ads(self, status: AdStatus = None) -> ListOfDicts: ...

    # 30: Создание объявления
    @abstractmethod
    async def ad_new(
        self,
        coin: Coin,
        cur: Cur,
        is_sell: bool,
        fiats: list[Fiat],
        amount: str,
        price: float,
        min_fiat: str,
        is_float: bool = True,
        details: str = None,
        autoreply: str = None,
        status: AdStatus = AdStatus.active,
    ) -> Ad.pyd(): ...

    # 31: Редактирование объявления
    @abstractmethod
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
    ) -> Ad.pyd(): ...

    # 32: Удаление
    @abstractmethod
    async def ad_del(self, offer_id: int) -> bool: ...

    # 33: Вкл/выкл объявления
    @abstractmethod
    async def ad_switch(self, offer_id: int, active: bool) -> bool: ...

    # 34: Вкл/выкл всех объявлений
    @abstractmethod
    async def ads_switch(self, active: bool) -> bool: ...

    # # # User
    # 35: Получить объект юзера по его ид
    @abstractmethod
    async def get_user(self, user_id) -> dict: ...

    # 36: Отправка сообщения юзеру с приложенным файлом
    @abstractmethod
    async def send_user_msg(self, msg: str, file=None) -> bool: ...

    # 37: (Раз)Блокировать юзера
    @abstractmethod
    async def block_user(self, is_blocked: bool = True) -> bool: ...

    # 38: Поставить отзыв юзеру
    @abstractmethod
    async def rate_user(self, positive: bool) -> bool: ...

    # 39: Балансы моих монет
    @abstractmethod
    async def my_assets(self) -> dict: ...

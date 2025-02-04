from typing import Literal
from pydantic import BaseModel
from xync_client.pyd import PayMeth


class UserStatistics(BaseModel):
    userId: int
    totalOrdersCount: int
    successRate: str
    successPercent: int


class User(BaseModel):
    userId: int
    nickname: str
    avatarCode: str
    statistics: UserStatistics
    isVerified: bool
    lastOnlineMinutesAgo: int | None = None
    onlineStatus: str


class AvailableVolume(BaseModel):
    currencyCode: str
    amount: str


class Price(BaseModel):
    type: str
    baseCurrencyCode: str
    quoteCurrencyCode: str
    value: str
    estimated: str | None = None


class OrderLimits(BaseModel):
    currencyCode: str | None = None
    min: str  # In
    max: str | None = None
    approximate: bool | None = None


class ChangeLogItem(BaseModel):
    status: Literal["ACTIVE", "INACTIVE", "ACTIVATING"]
    createDateTime: str
    initiatorUserId: int


class ChangeLog(BaseModel):
    items: list[ChangeLogItem]


class TakerFilter(BaseModel):
    accountAge: str
    completedOrders: str
    userRating: str


class FeeAvailableVolume(BaseModel):
    currencyCode: str
    amount: str


class Fee(BaseModel):
    rate: str
    availableVolume: FeeAvailableVolume


class KeyVal(BaseModel):
    name: Literal["PAYMENT_DETAILS_NUMBER", "PHONE"] = "PAYMENT_DETAILS_NUMBER"
    value: str


class BanksIn(BaseModel):
    name: Literal["BANKS"] = "BANKS"
    value: list[str]


class Bank(BaseModel):
    code: str
    nameRu: str
    nameEn: str


class Banks(BanksIn):
    value: list[Bank]


class Attrs(BaseModel):
    version: Literal["V1"] = "V1"
    values: list[KeyVal]


class AttrsV2In(BaseModel):
    version: Literal["V2"]
    values: list[KeyVal | BanksIn]


class AttrsV2(AttrsV2In):
    values: list[KeyVal | Banks]


class FiatPydIn(BaseModel):
    paymentMethodCode: str
    currencyCode: str
    name: str
    attributes: Attrs | AttrsV2In


class FiatEpyd(BaseModel):
    id: int
    userId: int
    paymentMethod: PayMeth
    currency: str
    name: str = ""
    attributes: Attrs | AttrsV2


class InitVolume(BaseModel):
    currencyCode: str
    amount: str


class _PaymentMethodsTrait:
    paymentMethods: list[PayMeth]


class __BaseCommonAd(BaseModel):
    id: int | None = None
    type: Literal["PURCHASE", "SALE"]
    price: Price


class _MyAdEpydIn(__BaseCommonAd):
    paymentConfirmTimeout: str
    comment: str
    initVolume: InitVolume
    orderRoundingRequired: bool
    orderAmountLimits: OrderLimits


class MyAdInPurchaseEpyd(_MyAdEpydIn):
    paymentMethodCodes: list[str]


class MyAdInSaleEpyd(_MyAdEpydIn):
    paymentDetailsIds: list[int]


class AdEpyd(__BaseCommonAd, _PaymentMethodsTrait):
    number: str
    user: User
    availableVolume: str
    orderAmountLimits: OrderLimits
    orderVolumeLimits: OrderLimits
    takerFilter: TakerFilter

    is_sell: bool = lambda x: x.type == "SALE"


class AdFullEpyd(AdEpyd):
    availableVolume: AvailableVolume
    paymentConfirmTimeout: Literal["PT15M", "PT30M"]
    price: Price
    orderAmountLimits: OrderLimits
    orderVolumeLimits: OrderLimits
    status: Literal["ACTIVE", "INACTIVE", "ACTIVATING"]
    createDateTime: str
    comment: str
    orderConfirmationTimeout: Literal["PT3M"]
    orderAcceptTimeout: Literal["PT10M"]


class _MyAdEpyd(__BaseCommonAd):
    number: str
    availableVolume: AvailableVolume
    orderAmountLimits: OrderLimits
    orderVolumeLimits: OrderLimits
    status: str
    createDateTime: str
    changeLog: ChangeLog
    takerFilter: TakerFilter
    orderConfirmationTimeout: str
    orderAcceptTimeout: str
    fee: Fee


class MyAdEpydSale(_MyAdEpyd):
    paymentDetails: list[FiatEpyd]


class MyAdEpydPurchase(_MyAdEpyd, _PaymentMethodsTrait): ...

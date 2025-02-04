from pydantic import BaseModel, model_validator
from xync_schema.enums import AdStatus


class PayMeth(BaseModel):
    code: str
    name: str
    originNameLocale: str
    nameEng: str


class PmXpyd(BaseModel):
    id: int | None = None
    name: str
    logo: str | None = None
    banks: list[PayMeth] | None = None  # todo: refact excess data in banks


class PmcurXpyd(BaseModel):
    pm_id: int
    cur_id: int


class FiatXpyd(BaseModel):
    # unq
    id: int = None
    user_id: int
    pmcur_id: int | None = None
    pmcur: PmcurXpyd | None = None
    # df
    detail: str
    name: str = ""
    amount: float
    target: float | None = None

    banks: list[str] = []

    @classmethod
    @model_validator(mode="before")
    def check_at_least_one_field(cls, values):
        if values.get("pmcur") or values.get("pmcur_id"):
            return values
        raise ValueError("pmcur_id or pmcur is required")

    def args(self) -> tuple[dict, dict]:
        unq: tuple[str, ...] = "id", "user_id", "pmcur_id", "pmcur"
        df: tuple[str, ...] = "detail", "name", "amount", "target"

        d = self.model_dump()
        return {k: getattr(self, k) for k in df if d.get(k)}, {k: getattr(self, k) for k in unq if d.get(k)}


class AdInXpyd(BaseModel):
    # unq
    id: int
    # df
    price: float
    minFiat: float
    maxFiat: float | None = None
    detail: str | None = None
    autoMsg: str | None = None
    status: AdStatus = AdStatus.active
    agent_id: int
    direction_id: int


class FiatexXpyd(BaseModel):
    id: int | None = None
    exid: str
    ex_id: int
    fiat_id: int

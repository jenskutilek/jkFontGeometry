from decimal import ROUND_HALF_UP, Decimal, DefaultContext, setcontext

DefaultContext.rounding = ROUND_HALF_UP
setcontext(DefaultContext)


def round_hup(value: float) -> int:
    return int(round(Decimal(str(value)), 0))

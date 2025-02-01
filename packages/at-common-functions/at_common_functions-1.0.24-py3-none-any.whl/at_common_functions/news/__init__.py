from at_common_functions.news.impls.stock import list as _list_stocks
from at_common_functions.news.impls.general import list as _list_generals
from at_common_workflow import export

@export
async def list_stocks(*, symbol: str, limit: int, days_back: int = 7) -> list:
    return await _list_stocks(symbol=symbol, limit=limit, days_back=days_back)

@export
async def list_generals(*, limit: int, days_back: int = 1) -> list:
    return await _list_generals(limit=limit, days_back=days_back)
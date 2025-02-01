from at_common_functions.stock.impls.candlestick import list as _list_candlesticks
from at_common_functions.stock.impls.financial import list as _list_financials, analyze as _analyze_financials, get_latest as _get_latest_financials
from at_common_functions.stock.impls.indicator import list as _list_indicators
from at_common_functions.stock.impls.overview import get as _get_overview
from at_common_functions.stock.impls.quotation import get as _get_quotation
from at_common_workflow import export

@export
async def list_candlesticks(*, symbol: str, type: str, limit: int) -> list:
    return await _list_candlesticks(symbol=symbol, type=type, limit=limit)

@export
async def get_latest_financials(*, symbol: str) -> dict:
    return await _get_latest_financials(symbol=symbol)

@export
async def list_financials(*, symbol: str, period: str, statement: str, limit: int) -> list:
    return await _list_financials(symbol=symbol, period=period, statement=statement, limit=limit)

@export
async def analyze_financials(*, symbol: str) -> dict:
    return await _analyze_financials(symbol=symbol)

@export
async def list_indicators(*, symbol: str, type: str, limit: int) -> list:
    return await _list_indicators(symbol=symbol, type=type, limit=limit)

@export
async def get_overview(*, symbol: str) -> dict:
    return await _get_overview(symbol=symbol)

@export
async def get_quotation(*, symbol: str) -> dict:
    return await _get_quotation(symbol=symbol)

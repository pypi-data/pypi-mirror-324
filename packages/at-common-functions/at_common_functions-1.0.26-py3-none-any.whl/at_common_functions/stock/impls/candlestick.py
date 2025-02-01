from at_common_functions.utils.storage import get_storage
from at_common_models.stock.daily_candlestick import DailyCandlestickModel

async def list(*, symbol: str, type: str, limit: int) -> list:
    storage = get_storage()

    candlesticks = None
    if type == 'daily':
        candlesticks = await storage.query(
            model_class=DailyCandlestickModel,
            filters=[DailyCandlestickModel.symbol == symbol],
            sort=[DailyCandlestickModel.time.desc()],
            limit=limit
        )
    
    if candlesticks is None:
        raise ValueError(f"Invalid type for candlesticks: {type}")

    return [c.to_dict() for c in candlesticks]

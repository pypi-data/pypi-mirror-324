from at_common_functions.utils.storage import get_storage
from at_common_models.stock.daily_indicator import DailyIndicatorModel

async def list(*, symbol: str, type: str, limit: int) -> list:
    storage = get_storage()

    indicators = None
    if type == 'daily':
        indicators = await storage.query(
            model_class=DailyIndicatorModel,
            filters=[DailyIndicatorModel.symbol == symbol],
            sort=[DailyIndicatorModel.time.desc()],
            limit=limit
        )

    if indicators is None: 
        raise ValueError(f"Invalid type for indicators: {type}")
    
    return [i.to_dict() for i in indicators]
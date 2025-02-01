from at_common_functions.utils.storage import get_storage
from at_common_models.stock.overview import OverviewModel

async def get(*, symbol: str) -> dict:
    storage = get_storage()
    overviews = await storage.query(
        model_class=OverviewModel,
        filters=[OverviewModel.symbol == symbol]
    )

    if len(overviews) == 0:
        raise ValueError(f"No overview found for symbol: {symbol}")

    if len(overviews) > 1:
        raise ValueError(f"Multiple overviews found for symbol: {symbol}, got {len(overviews)}")
    
    return overviews[0].to_dict()
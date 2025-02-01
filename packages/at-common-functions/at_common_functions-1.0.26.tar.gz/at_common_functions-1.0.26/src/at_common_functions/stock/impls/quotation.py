from at_common_functions.utils.storage import get_storage
from at_common_models.stock.quotation import QuotationModel

async def get(*, symbol: str) -> dict:
    storage = get_storage()
    quotations = await storage.query(
        model_class=QuotationModel,
        filters=[QuotationModel.symbol == symbol]
    )

    if len(quotations) == 0:
        raise ValueError(f"No quotation found for symbol: {symbol}")
    
    if len(quotations) > 1:
        raise ValueError(f"Multiple quotations found for symbol: {symbol}, got {len(quotations)}")
    
    return quotations[0].to_dict()

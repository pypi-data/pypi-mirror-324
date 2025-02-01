from at_common_functions.utils.storage import get_storage
from at_common_models.news.stock import NewsStockModel
from at_common_models.news.article import NewsArticleModel
from datetime import datetime, timedelta

async def list(*, symbol: str, limit: int, days_back: int) -> list:
    storage = get_storage()
    
    cutoff_date = datetime.now() - timedelta(days=days_back)
    stock_news = await storage.query(
        model_class=NewsStockModel,
        filters=[
            NewsStockModel.symbol == symbol,
            NewsStockModel.published_at >= cutoff_date
        ],
        sort=[NewsStockModel.published_at.desc()],
        limit=limit
    )

    if not stock_news:
        return []

    articles = await storage.query(
        model_class=NewsArticleModel,
        filters=[NewsArticleModel.id.in_([news.news_id for news in stock_news])],
        sort=[NewsArticleModel.published_at.desc()]
    )
    
    return [article.to_dict() for article in articles]

    

    
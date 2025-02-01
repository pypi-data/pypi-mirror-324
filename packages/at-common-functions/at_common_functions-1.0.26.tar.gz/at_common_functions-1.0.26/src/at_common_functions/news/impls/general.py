from at_common_functions.utils.storage import get_storage
from at_common_models.news.general import NewsGeneralModel
from at_common_models.news.article import NewsArticleModel
from datetime import datetime, timedelta

async def list(*, limit: int, days_back: int) -> list:
    storage = get_storage()
    
    cutoff_date = datetime.now() - timedelta(days=days_back)
    general_news = await storage.query(
        model_class=NewsGeneralModel,
        filters=[
            NewsGeneralModel.published_at >= cutoff_date
        ],
        sort=[NewsGeneralModel.published_at.desc()],
        limit=limit
    )

    if not general_news:
        return []

    articles = await storage.query(
        model_class=NewsArticleModel,
        filters=[NewsArticleModel.id.in_([news.news_id for news in general_news])],
        sort=[NewsArticleModel.published_at.desc()]
    )
    
    return [article.to_dict() for article in articles]

    

    
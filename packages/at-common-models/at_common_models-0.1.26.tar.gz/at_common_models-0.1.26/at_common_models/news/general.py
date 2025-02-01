from sqlalchemy import Column, String, DateTime
from at_common_models.base import BaseModel

class NewsGeneralModel(BaseModel):
    __tablename__ = "news_generals"

    news_id = Column(String(40), primary_key=True, nullable=False)
    published_at = Column(DateTime, nullable=False, index=True)

    def __str__(self):
        return f"<NewsGeneral(news_id={self.news_id}, published_at={self.published_at})>"

    def __repr__(self):
        return f"<NewsGeneral(news_id={self.news_id}, published_at={self.published_at})>"

import pytest
from datetime import datetime
from at_common_models.news.article import NewsArticleModel
from at_common_models.news.stock import NewsStockModel
from at_common_models.news.general import NewsGeneralModel

def test_news_article_model(session):
    # Create test data
    article = NewsArticleModel(
        id="test123",
        source="Reuters",
        headline="Test Headline",
        summary="This is a test summary",
        url="https://example.com/news",
        published_at=datetime.now()
    )
    
    session.add(article)
    session.commit()
    
    result = session.query(NewsArticleModel).filter_by(id="test123").first()
    assert result.id == "test123"
    assert result.source == "Reuters"
    assert result.headline == "Test Headline"

def test_news_stock_model(session):
    # Create test data
    news_stock = NewsStockModel(
        news_id="test123",
        symbol="AAPL",
        published_at=datetime.now()
    )
    
    session.add(news_stock)
    session.commit()
    
    result = session.query(NewsStockModel).filter_by(news_id="test123").first()
    assert result.news_id == "test123"
    assert result.symbol == "AAPL"

def test_news_relationship(session):
    # Test the relationship between news articles and stocks
    article = NewsArticleModel(
        id="test123",
        source="Reuters",
        headline="Test Headline",
        summary="This is a test summary",
        url="https://example.com/news",
        published_at=datetime.now()
    )
    
    news_stock = NewsStockModel(
        news_id="test123",
        symbol="AAPL",
        published_at=datetime.now()
    )
    
    session.add(article)
    session.add(news_stock)
    session.commit()
    
    result = session.query(NewsStockModel).filter_by(news_id="test123").first()
    assert result.symbol == "AAPL"

def test_multiple_stocks_per_article(session):
    # Test one article related to multiple stocks
    article = NewsArticleModel(
        id="test456",
        source="Bloomberg",
        headline="Tech Giants Report",
        summary="Multiple tech companies report earnings",
        url="https://example.com/tech-news",
        published_at=datetime.now()
    )
    
    # Create multiple stock relationships
    stocks = ["AAPL", "GOOGL", "MSFT"]
    stock_relations = [
        NewsStockModel(
            news_id="test456",
            symbol=symbol,
            published_at=datetime.now()
        )
        for symbol in stocks
    ]
    
    session.add(article)
    session.add_all(stock_relations)
    session.commit()
    
    results = session.query(NewsStockModel).filter_by(news_id="test456").all()
    assert len(results) == 3
    assert set([r.symbol for r in results]) == set(stocks)

def test_news_general_model_creation():
    # Test basic model creation
    news_id = "test123"
    published_at = datetime(2024, 1, 1, 12, 0, 0)
    
    news = NewsGeneralModel(
        news_id=news_id,
        published_at=published_at
    )
    
    assert news.news_id == news_id
    assert news.published_at == published_at

def test_news_general_string_representation():
    # Test __str__ and __repr__ methods
    news_id = "test123"
    published_at = datetime(2024, 1, 1, 12, 0, 0)
    
    news = NewsGeneralModel(
        news_id=news_id,
        published_at=published_at
    )
    
    expected_str = f"<NewsGeneral(news_id={news_id}, published_at={published_at})>"
    assert str(news) == expected_str
    assert repr(news) == expected_str
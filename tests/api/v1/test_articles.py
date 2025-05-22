import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from app import crud
from app.schemas.article import ArticleCreate, ArticleUpdate


@pytest.fixture
async def create_test_admin_user(db: AsyncSession):
    """Create a superuser for testing protected endpoints"""
    from app.schemas.user import UserCreate

    admin_data = UserCreate(
        email="admin@test.com",
        password="admin_password123",
        is_superuser=True,
        full_name="Test Admin"
    )
    admin_user = await crud.user.create(db, obj_in=admin_data)
    return admin_user


@pytest.fixture
async def admin_token_headers(client: AsyncClient, create_test_admin_user):
    """Get token headers for admin user"""
    login_data = {
        "username": "admin@test.com",
        "password": "admin_password123",
    }
    response = await client.post("/api/v1/auth/login", data=login_data)
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


@pytest.fixture
async def create_test_location(db: AsyncSession):
    """Create a test location for articles"""
    from app.schemas.location import LocationCreate

    location_data = LocationCreate(
        name="Article Test Location",
        country="Test Country",
        latitude=35.6812,
        longitude=139.7671,
        description="A location for article testing",
        continent="Asia",
        is_active=True
    )
    location = await crud.location.create(db, obj_in=location_data)
    return location


@pytest.fixture
async def create_test_article(db: AsyncSession, create_test_location, create_test_admin_user):
    """Create a test article"""
    article_data = ArticleCreate(
        title="Test Article Title",
        content="This is the content of a test article for travel enthusiasts.",
        author_id=create_test_admin_user.id,
        location_id=create_test_location.id,
        summary="A brief summary of the test article",
        tags=["test", "travel", "guide"],
        is_published=True,
        is_active=True
    )
    article = await crud.article.create(db, obj_in=article_data)
    return article


@pytest.mark.asyncio
async def test_create_article(client: AsyncClient, admin_token_headers, create_test_location):
    """Test creating a new article"""
    article_data = {
        "title": "Top 10 Places to Visit",
        "content": "Here are the top 10 places every traveler should visit...",
        "location_id": create_test_location.id,
        "summary": "Essential travel destinations",
        "tags": ["travel", "top10", "destinations"],
        "is_published": True
    }

    response = await client.post(
        "/api/v1/articles/",
        headers=admin_token_headers,
        json=article_data
    )

    assert response.status_code == status.HTTP_200_OK
    created_article = response.json()
    assert created_article["title"] == "Top 10 Places to Visit"
    assert created_article["summary"] == "Essential travel destinations"
    assert "top10" in created_article["tags"]
    assert created_article["is_published"] is True


@pytest.mark.asyncio
async def test_read_articles(client: AsyncClient, create_test_article):
    """Test retrieving all published articles (public endpoint)"""
    response = await client.get("/api/v1/articles/")

    assert response.status_code == status.HTTP_200_OK
    articles = response.json()
    assert len(articles) >= 1
    assert any(article["title"] == "Test Article Title" for article in articles)


@pytest.mark.asyncio
async def test_read_articles_with_filters(client: AsyncClient, create_test_article):
    """Test retrieving articles with filters"""
    # Filter by tag
    response = await client.get("/api/v1/articles/?tag=travel")

    assert response.status_code == status.HTTP_200_OK
    articles = response.json()
    assert len(articles) >= 1
    assert all("travel" in article["tags"] for article in articles)


@pytest.mark.asyncio
async def test_search_articles(client: AsyncClient, create_test_article):
    """Test searching articles by query"""
    response = await client.get("/api/v1/articles/search?query=travel")

    assert response.status_code == status.HTTP_200_OK
    articles = response.json()
    assert len(articles) >= 1
    assert any("travel" in article["content"].lower() for article in articles)


@pytest.mark.asyncio
async def test_read_article(client: AsyncClient, create_test_article):
    """Test retrieving an article by ID"""
    article_id = create_test_article.id

    response = await client.get(f"/api/v1/articles/{article_id}")

    assert response.status_code == status.HTTP_200_OK
    article = response.json()
    assert article["id"] == article_id
    assert article["title"] == "Test Article Title"
    assert article["content"] == "This is the content of a test article for travel enthusiasts."


@pytest.mark.asyncio
async def test_read_article_not_found(client: AsyncClient):
    """Test retrieving a non-existent article"""
    response = await client.get("/api/v1/articles/999999")  # Non-existent ID

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_article(client: AsyncClient, admin_token_headers, create_test_article):
    """Test updating an article"""
    article_id = create_test_article.id
    update_data = {
        "title": "Updated Article Title",
        "content": "This is the updated content of the article.",
        "tags": ["test", "travel", "guide", "updated"]
    }

    response = await client.put(
        f"/api/v1/articles/{article_id}",
        headers=admin_token_headers,
        json=update_data
    )

    assert response.status_code == status.HTTP_200_OK
    updated_article = response.json()
    assert updated_article["title"] == "Updated Article Title"
    assert updated_article["content"] == "This is the updated content of the article."
    assert "updated" in updated_article["tags"]


@pytest.mark.asyncio
async def test_update_article_not_found(client: AsyncClient, admin_token_headers):
    """Test updating a non-existent article"""
    update_data = {
        "title": "This Article Doesn't Exist",
        "content": "Trying to update a non-existent article."
    }

    response = await client.put(
        "/api/v1/articles/999999",  # Non-existent ID
        headers=admin_token_headers,
        json=update_data
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_article(client: AsyncClient, admin_token_headers, create_test_article):
    """Test deleting an article"""
    article_id = create_test_article.id

    response = await client.delete(
        f"/api/v1/articles/{article_id}",
        headers=admin_token_headers
    )

    assert response.status_code == status.HTTP_200_OK

    # Verify article no longer exists or is marked as inactive
    get_response = await client.get(f"/api/v1/articles/{article_id}")

    # Either it should return 404 or the article should be marked as inactive
    if get_response.status_code == status.HTTP_200_OK:
        article = get_response.json()
        assert article["is_active"] is False
    else:
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_publish_unpublish_article(client: AsyncClient, admin_token_headers, create_test_article):
    """Test publishing and unpublishing an article"""
    article_id = create_test_article.id

    # Unpublish the article
    response = await client.put(
        f"/api/v1/articles/{article_id}/publish",
        headers=admin_token_headers,
        json={"is_published": False}
    )

    assert response.status_code == status.HTTP_200_OK
    article = response.json()
    assert article["is_published"] is False

    # Publish the article again
    response = await client.put(
        f"/api/v1/articles/{article_id}/publish",
        headers=admin_token_headers,
        json={"is_published": True}
    )

    assert response.status_code == status.HTTP_200_OK
    article = response.json()
    assert article["is_published"] is True


@pytest.mark.asyncio
async def test_read_articles_by_author(client: AsyncClient, create_test_article, create_test_admin_user):
    """Test retrieving articles by author"""
    author_id = create_test_admin_user.id

    response = await client.get(f"/api/v1/articles/author/{author_id}")

    assert response.status_code == status.HTTP_200_OK
    articles = response.json()
    assert len(articles) >= 1
    assert all(article["author_id"] == author_id for article in articles)


@pytest.mark.asyncio
async def test_read_articles_by_location(client: AsyncClient, create_test_article, create_test_location):
    """Test retrieving articles by location"""
    location_id = create_test_location.id

    response = await client.get(f"/api/v1/articles/location/{location_id}")

    assert response.status_code == status.HTTP_200_OK
    articles = response.json()
    assert len(articles) >= 1
    assert all(article["location_id"] == location_id for article in articles)


@pytest.mark.asyncio
async def test_unauthorized_article_operations(client: AsyncClient, create_test_article):
    """Test that protected article operations require authentication"""
    article_id = create_test_article.id

    # Try to create without auth
    create_data = {
        "title": "Unauthorized Article",
        "content": "This should not be created"
    }
    response = await client.post("/api/v1/articles/", json=create_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to update without auth
    update_data = {"title": "Updated Title"}
    response = await client.put(f"/api/v1/articles/{article_id}", json=update_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to delete without auth
    response = await client.delete(f"/api/v1/articles/{article_id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

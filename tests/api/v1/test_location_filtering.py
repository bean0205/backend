import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Country, Region, Category, Amenity, LocationAmenity, Location, Rating


@pytest.fixture
async def seed_test_data(db: AsyncSession):
    """Seed the database with test data for filtering tests"""
    # Create countries
    country1 = Country(name="United States", code="US")
    country2 = Country(name="France", code="FR")
    db.add_all([country1, country2])
    await db.commit()
    
    # Create regions
    region1 = Region(name="California", country_id=country1.id)
    region2 = Region(name="New York", country_id=country1.id)
    region3 = Region(name="Paris", country_id=country2.id)
    db.add_all([region1, region2, region3])
    await db.commit()
    
    # Create categories
    category1 = Category(name="Hotel", description="Places to stay")
    category2 = Category(name="Restaurant", description="Places to eat")
    category3 = Category(name="Attraction", description="Places to visit")
    db.add_all([category1, category2, category3])
    await db.commit()
    
    # Create amenities
    wifi = Amenity(name="WiFi", icon="wifi")
    pool = Amenity(name="Pool", icon="pool")
    parking = Amenity(name="Parking", icon="parking")
    breakfast = Amenity(name="Breakfast", icon="food")
    db.add_all([wifi, pool, parking, breakfast])
    await db.commit()
    
    # Create locations
    locations = [
        # Hotels
        Location(
            name="Luxury Hotel SF",
            description="Luxury hotel in San Francisco",
            latitude=37.7749,
            longitude=-122.4194,
            geom="SRID=4326;POINT(-122.4194 37.7749)",
            address="123 Main St",
            city="San Francisco",
            country_id=country1.id,
            region_id=region1.id,
            category_id=category1.id,
            price_min=300,
            price_max=800,
            popularity_score=4.8,
            thumbnail_url="https://example.com/luxuryhotel.jpg"
        ),
        Location(
            name="Budget Inn NY",
            description="Affordable hotel in New York",
            latitude=40.7128,
            longitude=-74.0060,
            geom="SRID=4326;POINT(-74.0060 40.7128)",
            address="456 Broadway",
            city="New York",
            country_id=country1.id,
            region_id=region2.id,
            category_id=category1.id,
            price_min=100,
            price_max=200,
            popularity_score=3.5,
            thumbnail_url="https://example.com/budgetinn.jpg"
        ),
        # Restaurants
        Location(
            name="French Bistro",
            description="Authentic French cuisine",
            latitude=48.8566,
            longitude=2.3522,
            geom="SRID=4326;POINT(2.3522 48.8566)",
            address="10 Rue de Rivoli",
            city="Paris",
            country_id=country2.id,
            region_id=region3.id,
            category_id=category2.id,
            price_min=50,
            price_max=150,
            popularity_score=4.7,
            thumbnail_url="https://example.com/frenchbistro.jpg"
        ),
        Location(
            name="California Sushi",
            description="Fresh sushi in California",
            latitude=34.0522,
            longitude=-118.2437,
            geom="SRID=4326;POINT(-118.2437 34.0522)",
            address="789 Ocean Dr",
            city="Los Angeles",
            country_id=country1.id,
            region_id=region1.id,
            category_id=category2.id,
            price_min=20,
            price_max=100,
            popularity_score=4.2,
            thumbnail_url="https://example.com/sushi.jpg"
        ),
        # Attractions
        Location(
            name="Eiffel Tower",
            description="Famous Paris landmark",
            latitude=48.8584,
            longitude=2.2945,
            geom="SRID=4326;POINT(2.2945 48.8584)",
            address="Champ de Mars",
            city="Paris",
            country_id=country2.id,
            region_id=region3.id,
            category_id=category3.id,
            price_min=10,
            price_max=25,
            popularity_score=4.9,
            thumbnail_url="https://example.com/eiffel.jpg"
        ),
        Location(
            name="Golden Gate Park",
            description="Large urban park in San Francisco",
            latitude=37.7694,
            longitude=-122.4862,
            geom="SRID=4326;POINT(-122.4862 37.7694)",
            address="501 Stanyan St",
            city="San Francisco",
            country_id=country1.id,
            region_id=region1.id,
            category_id=category3.id,
            price_min=0,
            price_max=0,
            popularity_score=4.5,
            thumbnail_url="https://example.com/goldengate.jpg"
        ),
    ]
    
    db.add_all(locations)
    await db.commit()
    
    # Add amenities to locations
    location_amenities = [
        # Luxury Hotel has all amenities
        LocationAmenity(location_id=locations[0].id, amenity_id=wifi.id),
        LocationAmenity(location_id=locations[0].id, amenity_id=pool.id),
        LocationAmenity(location_id=locations[0].id, amenity_id=parking.id),
        LocationAmenity(location_id=locations[0].id, amenity_id=breakfast.id),
        
        # Budget Inn has wifi and parking
        LocationAmenity(location_id=locations[1].id, amenity_id=wifi.id),
        LocationAmenity(location_id=locations[1].id, amenity_id=parking.id),
        
        # French Bistro has wifi and breakfast
        LocationAmenity(location_id=locations[2].id, amenity_id=wifi.id),
        LocationAmenity(location_id=locations[2].id, amenity_id=breakfast.id),
        
        # California Sushi has wifi
        LocationAmenity(location_id=locations[3].id, amenity_id=wifi.id),
    ]
    
    db.add_all(location_amenities)
    await db.commit()
    
    return locations


@pytest.mark.asyncio
async def test_filter_locations_by_country(client: AsyncClient, seed_test_data):
    """Test filtering locations by country"""
    response = await client.get("/api/v1/locations", params={"country_id": 1})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["total_items"] == 4
    assert all(item["address_short"].endswith("United States") for item in data["items"])


@pytest.mark.asyncio
async def test_filter_locations_by_region(client: AsyncClient, seed_test_data):
    """Test filtering locations by region"""
    response = await client.get("/api/v1/locations", params={"region_id": 1})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["total_items"] == 3
    for item in data["items"]:
        assert "San Francisco" in item["address_short"] or "Los Angeles" in item["address_short"]


@pytest.mark.asyncio
async def test_filter_locations_by_category(client: AsyncClient, seed_test_data):
    """Test filtering locations by category"""
    response = await client.get("/api/v1/locations", params={"category_id": 3})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["total_items"] == 2
    assert all(item["category_name"] == "Attraction" for item in data["items"])


@pytest.mark.asyncio
async def test_filter_locations_by_price_range(client: AsyncClient, seed_test_data):
    """Test filtering locations by price range"""
    response = await client.get("/api/v1/locations", params={
        "price_range_min": 0,
        "price_range_max": 100
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Should return Golden Gate Park, California Sushi, and Eiffel Tower
    assert data["total_items"] == 3


@pytest.mark.asyncio
async def test_filter_locations_by_amenities(client: AsyncClient, seed_test_data):
    """Test filtering locations by amenities"""
    response = await client.get("/api/v1/locations", params={
        "amenities": ["Pool"]
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Only Luxury Hotel has a pool
    assert data["total_items"] == 1
    assert data["items"][0]["name"] == "Luxury Hotel SF"


@pytest.mark.asyncio
async def test_sort_locations_by_price(client: AsyncClient, seed_test_data):
    """Test sorting locations by price"""
    response = await client.get("/api/v1/locations", params={
        "sort_by": "price_asc"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # First item should be free (Golden Gate Park)
    assert data["items"][0]["name"] == "Golden Gate Park"


@pytest.mark.asyncio
async def test_sort_locations_by_popularity(client: AsyncClient, seed_test_data):
    """Test sorting locations by popularity"""
    response = await client.get("/api/v1/locations", params={
        "sort_by": "popularity_desc"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Eiffel Tower should be first (popularity 4.9)
    assert data["items"][0]["name"] == "Eiffel Tower"


@pytest.mark.asyncio
async def test_pagination(client: AsyncClient, seed_test_data):
    """Test pagination of locations"""
    response = await client.get("/api/v1/locations", params={
        "page": 1,
        "size": 2
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["total_items"] == 6
    assert data["total_pages"] == 3
    assert data["current_page"] == 1
    assert len(data["items"]) == 2
    
    # Get second page
    response = await client.get("/api/v1/locations", params={
        "page": 2,
        "size": 2
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["current_page"] == 2
    assert len(data["items"]) == 2
    
    # Verify different items on different pages
    response_page1 = await client.get("/api/v1/locations", params={"page": 1, "size": 2})
    response_page2 = await client.get("/api/v1/locations", params={"page": 2, "size": 2})
    
    page1_ids = {item["id"] for item in response_page1.json()["items"]}
    page2_ids = {item["id"] for item in response_page2.json()["items"]}
    
    assert not page1_ids.intersection(page2_ids)


@pytest.mark.asyncio
async def test_search_term(client: AsyncClient, seed_test_data):
    """Test searching locations by term"""
    response = await client.get("/api/v1/locations", params={
        "search_term": "French"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["total_items"] == 1
    assert data["items"][0]["name"] == "French Bistro"


@pytest.mark.asyncio
async def test_combined_filters(client: AsyncClient, seed_test_data):
    """Test combining multiple filters"""
    response = await client.get("/api/v1/locations", params={
        "country_id": 1,
        "category_id": 1,
        "price_range_min": 100,
        "sort_by": "price_desc"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["total_items"] == 2
    # Luxury Hotel SF should be first (higher price)
    assert data["items"][0]["name"] == "Luxury Hotel SF"
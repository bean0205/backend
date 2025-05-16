"""
Sample data initialization script for testing location filtering functionality.
Run with: python -m app.scripts.init_test_data
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal
from app.db.models import Country, Region, Category, Amenity, LocationAmenity, Location


async def create_sample_data():
    """Create sample data for testing"""
    async with SessionLocal() as db:
        db: AsyncSession
        
        # Create countries
        print("Creating countries...")
        countries = [
            Country(name="United States", code="US"),
            Country(name="France", code="FR"),
            Country(name="Japan", code="JP"),
            Country(name="Italy", code="IT"),
            Country(name="Australia", code="AU"),
        ]
        db.add_all(countries)
        await db.commit()
        
        # Create regions
        print("Creating regions...")
        regions = [
            # US regions
            Region(name="California", country_id=1),
            Region(name="New York", country_id=1),
            Region(name="Florida", country_id=1),
            
            # France regions
            Region(name="Paris", country_id=2),
            Region(name="Provence", country_id=2),
            
            # Japan regions
            Region(name="Tokyo", country_id=3),
            Region(name="Kyoto", country_id=3),
            
            # Italy regions
            Region(name="Rome", country_id=4),
            Region(name="Venice", country_id=4),
            
            # Australia regions
            Region(name="Sydney", country_id=5),
            Region(name="Melbourne", country_id=5),
        ]
        db.add_all(regions)
        await db.commit()
        
        # Create categories
        print("Creating categories...")
        categories = [
            Category(name="Hotel", description="Places to stay overnight"),
            Category(name="Restaurant", description="Places to eat and drink"),
            Category(name="Attraction", description="Places to visit and explore"),
            Category(name="Beach", description="Coastal areas for relaxation"),
            Category(name="Shopping", description="Places for retail therapy"),
        ]
        db.add_all(categories)
        await db.commit()
        
        # Create amenities
        print("Creating amenities...")
        amenities = [
            Amenity(name="WiFi", icon="wifi"),
            Amenity(name="Pool", icon="pool"),
            Amenity(name="Parking", icon="parking"),
            Amenity(name="Breakfast", icon="food"),
            Amenity(name="Air Conditioning", icon="ac"),
            Amenity(name="Pet Friendly", icon="pet"),
            Amenity(name="Bar", icon="drink"),
            Amenity(name="Spa", icon="spa"),
            Amenity(name="Gym", icon="gym"),
            Amenity(name="Restaurant", icon="restaurant"),
        ]
        db.add_all(amenities)
        await db.commit()
        
        # Create locations
        print("Creating locations...")
        locations = [
            # US - California
            Location(
                name="Golden Gate Hotel",
                description="Luxury hotel with views of the Golden Gate Bridge",
                latitude=37.7749,
                longitude=-122.4194,
                geom="SRID=4326;POINT(-122.4194 37.7749)",
                address="123 Golden Gate Ave",
                city="San Francisco",
                country_id=1,
                region_id=1,
                category_id=1,
                price_min=250,
                price_max=500,
                popularity_score=4.8,
                thumbnail_url="https://example.com/goldengatehotel.jpg"
            ),
            Location(
                name="Coastal Restaurant",
                description="Seafood restaurant with ocean views",
                latitude=37.8199,
                longitude=-122.4783,
                geom="SRID=4326;POINT(-122.4783 37.8199)",
                address="456 Seafood Lane",
                city="San Francisco",
                country_id=1,
                region_id=1,
                category_id=2,
                price_min=30,
                price_max=80,
                popularity_score=4.5,
                thumbnail_url="https://example.com/coastalrestaurant.jpg"
            ),
            
            # US - New York
            Location(
                name="Central Park View",
                description="Elegant hotel overlooking Central Park",
                latitude=40.7812,
                longitude=-73.9665,
                geom="SRID=4326;POINT(-73.9665 40.7812)",
                address="789 Park Ave",
                city="New York",
                country_id=1,
                region_id=2,
                category_id=1,
                price_min=400,
                price_max=800,
                popularity_score=4.7,
                thumbnail_url="https://example.com/centralparkview.jpg"
            ),
            
            # France - Paris
            Location(
                name="Eiffel Tower View",
                description="Boutique hotel with Eiffel Tower views",
                latitude=48.8584,
                longitude=2.2945,
                geom="SRID=4326;POINT(2.2945 48.8584)",
                address="10 Avenue de la Tour",
                city="Paris",
                country_id=2,
                region_id=4,
                category_id=1,
                price_min=300,
                price_max=600,
                popularity_score=4.9,
                thumbnail_url="https://example.com/eiffeltowerview.jpg"
            ),
            Location(
                name="Le Bistro Parisien",
                description="Authentic French cuisine in the heart of Paris",
                latitude=48.8566,
                longitude=2.3522,
                geom="SRID=4326;POINT(2.3522 48.8566)",
                address="25 Rue de Rivoli",
                city="Paris",
                country_id=2,
                region_id=4,
                category_id=2,
                price_min=50,
                price_max=120,
                popularity_score=4.6,
                thumbnail_url="https://example.com/lebistroparisien.jpg"
            ),
            
            # Japan - Tokyo
            Location(
                name="Sakura Hotel",
                description="Traditional Japanese hotel with modern amenities",
                latitude=35.6762,
                longitude=139.6503,
                geom="SRID=4326;POINT(139.6503 35.6762)",
                address="1-1 Sakura Street",
                city="Tokyo",
                country_id=3,
                region_id=6,
                category_id=1,
                price_min=200,
                price_max=450,
                popularity_score=4.7,
                thumbnail_url="https://example.com/sakurahotel.jpg"
            ),
        ]
        db.add_all(locations)
        await db.commit()
        
        # Create location-amenity relationships
        print("Creating location amenities...")
        location_amenities = []
        
        # Golden Gate Hotel has WiFi, Pool, Parking, Breakfast, AC
        for amenity_id in range(1, 6):
            location_amenities.append(LocationAmenity(location_id=1, amenity_id=amenity_id))
        
        # Coastal Restaurant has WiFi, Parking, AC, Bar
        for amenity_id in [1, 3, 5, 7]:
            location_amenities.append(LocationAmenity(location_id=2, amenity_id=amenity_id))
        
        # Central Park View has WiFi, AC, Breakfast, Gym, Spa
        for amenity_id in [1, 4, 5, 8, 9]:
            location_amenities.append(LocationAmenity(location_id=3, amenity_id=amenity_id))
        
        # Eiffel Tower View has WiFi, AC, Breakfast, Bar
        for amenity_id in [1, 4, 5, 7]:
            location_amenities.append(LocationAmenity(location_id=4, amenity_id=amenity_id))
        
        # Le Bistro Parisien has WiFi, AC, Bar
        for amenity_id in [1, 5, 7]:
            location_amenities.append(LocationAmenity(location_id=5, amenity_id=amenity_id))
        
        # Sakura Hotel has WiFi, AC, Breakfast, Spa, Restaurant
        for amenity_id in [1, 4, 5, 8, 10]:
            location_amenities.append(LocationAmenity(location_id=6, amenity_id=amenity_id))
        
        db.add_all(location_amenities)
        await db.commit()
        
        print("Sample data creation completed successfully!")


if __name__ == "__main__":
    asyncio.run(create_sample_data())

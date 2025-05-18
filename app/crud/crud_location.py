from typing import List, Optional, Dict, Any, Tuple, cast
import math
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, asc, and_, or_, Float, text
from geoalchemy2 import functions as geo_func

from app.db.models import Location, Category, Country, Region, District, Ward, LocationAmenity
from app.schemas.location import (
    LocationCreate,
    LocationUpdate,
    LocationFilterParams,
    SortOption,
    PaginatedLocationResponse,
    LocationSummary
)


class CRUDLocation:
    async def create(self, db: AsyncSession, obj_in: LocationCreate) -> Location:
        """
        Create a new location.
        """
        # Extract amenities from input if present
        amenities = obj_in.amenities or []

        # Remove amenities from the data for the location model
        location_data = obj_in.dict(exclude={"amenities"})

        # Create point geography using the WKT format
        location_data["geom"] = func.ST_SetSRID(
            func.ST_MakePoint(obj_in.longitude, obj_in.latitude),
            4326
        )

        # Create location
        db_obj = Location(**location_data)
        db.add(db_obj)
        await db.flush()  # Flush to get the ID but don't commit yet

        # Create amenities
        for amenity_name in amenities:
            amenity = LocationAmenity(
                location_id=db_obj.id,
                name=amenity_name
            )
            db.add(amenity)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, id: int, obj_in: LocationUpdate) -> Location:
        """
        Update a location.
        """
        location = await self.get_by_id(db, id)
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")

        # Update attributes
        update_data = obj_in.dict(exclude_unset=True, exclude={"amenities"})

        # Update geom if latitude or longitude is provided
        if "latitude" in update_data or "longitude" in update_data:
            lat = update_data.get("latitude", location.latitude)
            lng = update_data.get("longitude", location.longitude)
            # Create point geography
            location.geom = func.ST_SetSRID(
                func.ST_MakePoint(lng, lat),
                4326
            )

        # Update other attributes
        for field, value in update_data.items():
            setattr(location, field, value)

        # Update amenities if provided
        if obj_in.amenities is not None:
            # Delete existing amenities
            await db.execute(
                text(f"DELETE FROM location_amenities WHERE location_id = {location.id}")
            )

            # Create new amenities
            for amenity_name in obj_in.amenities:
                amenity = LocationAmenity(
                    location_id=location.id,
                    name=amenity_name
                )
                db.add(amenity)

        await db.commit()
        await db.refresh(location)
        return location

    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[Location]:
        """
        Get a location by ID.
        """
        result = await db.execute(
            select(Location).where(Location.id == id)
        )
        return result.scalars().first()

    async def delete(self, db: AsyncSession, id: int) -> None:
        """
        Delete a location.
        """
        location = await self.get_by_id(db, id)
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")

        await db.delete(location)
        await db.commit()

    async def filter_locations(
            self, db: AsyncSession, params: LocationFilterParams
    ) -> PaginatedLocationResponse:
        """
        Filter locations based on various criteria and return paginated results.
        """
        # Base query joining with necessary tables
        # We need to join with category to get the category name for summary
        query = select(
            Location,
            Category.name.label("category_name")
        ).outerjoin(
            Category, Location.category_id == Category.id
        )

        # Apply filters
        if params.search_term:
            query = query.where(
                or_(
                    Location.name.ilike(f"%{params.search_term}%"),
                    Location.description.ilike(f"%{params.search_term}%"),
                    Location.address.ilike(f"%{params.search_term}%")
                )
            )

        if params.country_id:
            query = query.where(Location.country_id == params.country_id)

        if params.region_id:
            query = query.where(Location.region_id == params.region_id)

        if params.district_id:
            query = query.where(Location.district_id == params.district_id)

        if params.ward_id:
            query = query.where(Location.ward_id == params.ward_id)

        if params.category_id:
            query = query.where(Location.category_id == params.category_id)

        if params.price_range_min is not None:
            query = query.where(Location.price_min >= params.price_range_min)

        if params.price_range_max is not None:
            query = query.where(Location.price_max <= params.price_range_max)

        # Apply amenities filter if provided
        if params.amenities and len(params.amenities) > 0:
            for amenity in params.amenities:
                # Subquery to find location IDs that have this amenity
                amenity_subquery = select(LocationAmenity.location_id).where(
                    LocationAmenity.name.ilike(f"%{amenity}%")
                ).distinct()

                query = query.where(Location.id.in_(amenity_subquery))

        # Apply sorting
        if params.sort_by == SortOption.POPULARITY_DESC:
            query = query.order_by(desc(Location.popularity_score))
        elif params.sort_by == SortOption.POPULARITY_ASC:
            query = query.order_by(asc(Location.popularity_score))
        elif params.sort_by == SortOption.NAME_ASC:
            query = query.order_by(asc(Location.name))
        elif params.sort_by == SortOption.NAME_DESC:
            query = query.order_by(desc(Location.name))
        elif params.sort_by == SortOption.PRICE_ASC:
            query = query.order_by(asc(Location.price_min))
        elif params.sort_by == SortOption.PRICE_DESC:
            query = query.order_by(desc(Location.price_min))
        else:
            # Default sort by popularity
            query = query.order_by(desc(Location.popularity_score))

        # Count total items for pagination
        count_query = select(func.count()).select_from(query.subquery())
        total_count_result = await db.execute(count_query)
        total_items = total_count_result.scalar() or 0

        # Apply pagination
        query = query.offset((params.page - 1) * params.size).limit(params.size)

        # Execute query
        result = await db.execute(query)
        rows = result.all()

        # Map results to summary model
        items: List[LocationSummary] = []
        for row in rows:
            location: Location = row.Location
            category_name: Optional[str] = row.category_name

            items.append(LocationSummary(
                id=location.id,
                name=location.name,
                thumbnail_url=location.thumbnail_url,
                address_short=location.address_short,
                category_name=category_name,
                average_rating=location.average_rating,
                price_min=location.price_min,
                price_max=location.price_max
            ))

        # Calculate total pages
        total_pages = math.ceil(total_items / params.size) if total_items > 0 else 0

        return PaginatedLocationResponse(
            items=items,
            total_items=total_items,
            total_pages=total_pages,
            current_page=params.page
        )

    async def find_nearby_locations(
            self, db: AsyncSession, latitude: float, longitude: float,
            radius: float = 5.0, limit: int = 20, category_id: Optional[int] = None
    ) -> List[Location]:
        """
        Find locations near a given coordinate within a specified radius.
        Distance is calculated in kilometers.
        """
        # Create the point from input coordinates
        point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)

        # Build the query with ST_DWithin to find locations within radius
        # ST_Distance returns distance in meters, so multiply radius by 1000
        query = select(Location).where(
            func.ST_DWithin(
                Location.geom,
                point,
                radius * 1000  # Convert km to meters
            )
        ).order_by(
            func.ST_Distance(Location.geom, point)
        ).limit(limit)

        # Add category filter if provided
        if category_id:
            query = query.where(Location.category_id == category_id)

        # Execute query
        result = await db.execute(query)
        return result.scalars().all()


location = CRUDLocation()

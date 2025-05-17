# from typing import List, Optional, Union, Dict, Any, Tuple
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select, func, desc, asc, and_, or_, Float
# from sqlalchemy.orm import selectinload, joinedload, contains_eager
# from geoalchemy2.functions import ST_MakePoint, ST_SetSRID
# from sqlalchemy.sql.expression import cast
# from math import ceil
#
# from app.db.models import Location, Category, Country, Region, Amenity, LocationAmenity, Rating
# from app.schemas.location import LocationCreate, LocationUpdate, LocationFilterParams, SortOption
#
#
# class CRUDLocation:
#     async def get(
#         self,
#         db: AsyncSession,
#         location_id: int,
#         include_relations: bool = False
#     ) -> Optional[Location]:
#         """Get a location by ID"""
#         query = select(Location)
#
#         if include_relations:
#             query = query.options(
#                 joinedload(Location.category),
#                 joinedload(Location.country_rel),
#                 joinedload(Location.region),
#                 joinedload(Location.amenities_rel).joinedload(LocationAmenity.amenity),
#                 joinedload(Location.ratings)
#             )
#
#         query = query.where(Location.id == location_id)
#         result = await db.execute(query)
#         return result.scalars().first()
#
#     async def get_multi_filter(
#         self,
#         db: AsyncSession,
#         *,
#         filter_params: LocationFilterParams
#     ) -> Tuple[List[Location], int, int]:
#         """
#         Get locations with advanced filtering and pagination.
#         Returns tuple of (locations, total_count, total_pages)
#         """
#         # Calculate offset from page and size
#         offset = (filter_params.page - 1) * filter_params.size
#
#         # Build base query
#         query = select(Location).distinct()
#
#         # Add eager loading for related tables
#         query = query.options(
#             joinedload(Location.category),
#             joinedload(Location.country_rel),
#             joinedload(Location.region)
#         )
#
#         # Apply filters
#         query = self._apply_filters(query, filter_params)
#
#         # Apply sorting
#         query = self._apply_sorting(query, filter_params.sort_by)
#
#         # Execute count query first (without pagination)
#         count_query = select(func.count(Location.id.distinct()))
#         count_query = self._apply_filters(count_query, filter_params)
#         count_result = await db.execute(count_query)
#         total_count = count_result.scalar()
#
#         # Calculate total pages
#         total_pages = ceil(total_count / filter_params.size) if total_count > 0 else 1
#
#         # Apply pagination
#         query = query.offset(offset).limit(filter_params.size)
#
#         # Execute query
#         result = await db.execute(query)
#         locations = result.unique().scalars().all()
#
#         return locations, total_count, total_pages
#
#     def _apply_filters(
#         self,
#         query: Any,
#         filter_params: LocationFilterParams
#     ) -> Any:
#         """Apply all filters to the query"""
#         # Filter by active status
#         query = query.where(Location.is_active == True)
#
#         # Search term filter (search in name, description, and address)
#         if filter_params.search_term:
#             search_term = f"%{filter_params.search_term}%"
#             query = query.where(
#                 or_(
#                     Location.name.ilike(search_term),
#                     Location.description.ilike(search_term),
#                     Location.address.ilike(search_term),
#                     Location.city.ilike(search_term)
#                 )
#             )
#
#         # Country filter
#         if filter_params.country_id:
#             query = query.where(Location.country_id == filter_params.country_id)
#
#         # Region filter
#         if filter_params.region_id:
#             query = query.where(Location.region_id == filter_params.region_id)
#
#         # Category filter
#         if filter_params.category_id:
#             query = query.where(Location.category_id == filter_params.category_id)
#
#         # Price range filter
#         if filter_params.price_range_min is not None:
#             query = query.where(Location.price_min >= filter_params.price_range_min)
#
#         if filter_params.price_range_max is not None:
#             query = query.where(Location.price_max <= filter_params.price_range_max)
#
#         # Amenities filter
#         if filter_params.amenities and len(filter_params.amenities) > 0:
#             # Join with LocationAmenity and filter by amenities
#             for amenity_name in filter_params.amenities:
#                 # For each amenity, create a subquery to check if it exists
#                 subquery = select(LocationAmenity.location_id).join(
#                     Amenity, LocationAmenity.amenity_id == Amenity.id
#                 ).where(
#                     Amenity.name == amenity_name
#                 ).scalar_subquery()
#
#                 query = query.where(Location.id.in_(subquery))
#
#         # Minimum rating filter
#         if filter_params.min_rating is not None:
#             # Create a subquery to calculate average rating
#             avg_rating_subquery = select(
#                 Rating.location_id,
#                 func.avg(Rating.rating).label("avg_rating")
#             ).group_by(
#                 Rating.location_id
#             ).having(
#                 func.avg(Rating.rating) >= filter_params.min_rating
#             ).scalar_subquery()
#
#             query = query.where(Location.id.in_(avg_rating_subquery))
#
#         return query
#
#     def _apply_sorting(
#         self,
#         query: Any,
#         sort_by: Optional[SortOption]
#     ) -> Any:
#         """Apply sorting to the query"""
#         if not sort_by:
#             # Default sorting by name ascending
#             return query.order_by(asc(Location.name))
#
#         # Apply requested sorting
#         if sort_by == SortOption.NAME_ASC:
#             query = query.order_by(asc(Location.name))
#         elif sort_by == SortOption.NAME_DESC:
#             query = query.order_by(desc(Location.name))
#         elif sort_by == SortOption.POPULARITY_ASC:
#             query = query.order_by(asc(Location.popularity_score))
#         elif sort_by == SortOption.POPULARITY_DESC:
#             query = query.order_by(desc(Location.popularity_score))
#         elif sort_by in [SortOption.RATING_ASC, SortOption.RATING_DESC]:
#             # For ratings, we need to calculate average rating with a subquery
#             avg_rating = select(
#                 func.avg(Rating.rating).label("avg_rating")
#             ).where(
#                 Rating.location_id == Location.id
#             ).scalar_subquery()
#
#             if sort_by == SortOption.RATING_ASC:
#                 query = query.order_by(asc(avg_rating))
#             else:  # RATING_DESC
#                 query = query.order_by(desc(avg_rating))
#         elif sort_by == SortOption.PRICE_ASC:
#             query = query.order_by(asc(Location.price_min))
#         elif sort_by == SortOption.PRICE_DESC:
#             query = query.order_by(desc(Location.price_max))
#
#         return query
#     async def get_count(
#         self,
#         db: AsyncSession,
#         *,
#         filter_params: Optional[Dict[str, Any]] = None
#     ) -> int:
#         """Get count of locations with optional filtering"""
#         query = select(func.count(Location.id))
#
#         # Apply filters if provided
#         if filter_params:
#             if filter_params.get("search"):
#                 search_term = f"%{filter_params['search']}%"
#                 query = query.where(
#                     or_(
#                         Location.name.ilike(search_term),
#                         Location.description.ilike(search_term),
#                         Location.city.ilike(search_term)
#                     )
#                 )
#
#             if filter_params.get("is_active") is not None:
#                 query = query.where(Location.is_active == filter_params["is_active"])
#
#         result = await db.execute(query)
#         return result.scalar()
#
#     async def create(self, db: AsyncSession, *, obj_in: LocationCreate) -> Location:
#         """Create a new location"""
#         # Create PostGIS point from latitude/longitude
#         geom = func.ST_SetSRID(
#             func.ST_MakePoint(obj_in.longitude, obj_in.latitude),
#             4326
#         )
#
#         # Convert Pydantic model to dict and add geom
#         location_data = obj_in.model_dump()
#
#         # Remove country string if it exists (we're using country_id now)
#         if "country" in location_data:
#             location_data.pop("country", None)
#
#         db_obj = Location(**location_data, geom=geom)
#
#         db.add(db_obj)
#         await db.commit()
#         await db.refresh(db_obj)
#         return db_obj
#
#     async def update(
#         self,
#         db: AsyncSession,
#         *,
#         db_obj: Location,
#         obj_in: Union[LocationUpdate, Dict[str, Any]]
#     ) -> Location:
#         """Update a location"""
#         # Handle both Pydantic model and dict inputs
#         if isinstance(obj_in, dict):
#             update_data = obj_in
#         else:
#             update_data = obj_in.model_dump(exclude_unset=True)
#
#         # Remove country string if it exists (we're using country_id now)
#         if "country" in update_data:
#             update_data.pop("country", None)
#
#         # Update geom if lat/long are in the update data
#         update_geom = False
#         if "latitude" in update_data or "longitude" in update_data:
#             lat = update_data.get("latitude", db_obj.latitude)
#             lng = update_data.get("longitude", db_obj.longitude)
#             geom = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)
#             update_data["geom"] = geom
#
#         # Apply updates
#         for field, value in update_data.items():
#             if hasattr(db_obj, field) and field != "geom":
#                 setattr(db_obj, field, value)
#
#         db.add(db_obj)
#         await db.commit()
#         await db.refresh(db_obj)
#         return db_obj
#
#     async def delete(self, db: AsyncSession, *, location_id: int) -> Optional[Location]:
#         """Delete a location"""
#         obj = await self.get(db, location_id)
#         if obj:
#             await db.delete(obj)
#             await db.commit()
#         return obj
#
#
# location = CRUDLocation()

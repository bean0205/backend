from typing import List, Optional, Union, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from geoalchemy2.functions import ST_MakePoint, ST_SetSRID
from sqlalchemy.sql.expression import or_

from app.db.models import Location
from app.schemas.location import LocationCreate, LocationUpdate


class CRUDLocation:
    async def get(self, db: AsyncSession, location_id: int) -> Optional[Location]:
        """Get a location by ID"""
        query = select(Location).where(Location.id == location_id)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_multi(
        self, 
        db: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        filter_params: Optional[Dict[str, Any]] = None
    ) -> List[Location]:
        """Get multiple locations with pagination"""
        query = select(Location)
        
        # Apply filters if provided
        if filter_params:
            if filter_params.get("search"):
                search_term = f"%{filter_params['search']}%"
                query = query.where(
                    or_(
                        Location.name.ilike(search_term),
                        Location.description.ilike(search_term),
                        Location.city.ilike(search_term),
                        Location.country.ilike(search_term)
                    )
                )
            
            if filter_params.get("is_active") is not None:
                query = query.where(Location.is_active == filter_params["is_active"])
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_count(
        self, 
        db: AsyncSession,
        filter_params: Optional[Dict[str, Any]] = None
    ) -> int:
        """Get count of locations with optional filters"""
        query = select(func.count(Location.id))
        
        # Apply filters if provided
        if filter_params:
            if filter_params.get("search"):
                search_term = f"%{filter_params['search']}%"
                query = query.where(
                    or_(
                        Location.name.ilike(search_term),
                        Location.description.ilike(search_term),
                        Location.city.ilike(search_term),
                        Location.country.ilike(search_term)
                    )
                )
            
            if filter_params.get("is_active") is not None:
                query = query.where(Location.is_active == filter_params["is_active"])
        
        result = await db.execute(query)
        return result.scalar()
    
    async def create(
        self, db: AsyncSession, *, obj_in: LocationCreate
    ) -> Location:
        """Create a new location"""
        # Create WKT point geometry from lat/long
        point = ST_SetSRID(ST_MakePoint(obj_in.longitude, obj_in.latitude), 4326)
        
        db_obj = Location(
            name=obj_in.name,
            description=obj_in.description,
            latitude=obj_in.latitude,
            longitude=obj_in.longitude,
            geom=point,
            address=obj_in.address,
            city=obj_in.city,
            country=obj_in.country,
            is_active=obj_in.is_active
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: Location,
        obj_in: Union[LocationUpdate, Dict[str, Any]]
    ) -> Location:
        """Update a location"""
        obj_data = db_obj.__dict__
        
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        # Update geom if lat/long are in the update data
        update_geom = False
        if "latitude" in update_data and "longitude" in update_data:
            update_geom = True
        elif "latitude" in update_data and db_obj.longitude is not None:
            update_data["longitude"] = db_obj.longitude
            update_geom = True
        elif "longitude" in update_data and db_obj.latitude is not None:
            update_data["latitude"] = db_obj.latitude
            update_geom = True
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        # Update the geometry point if needed
        if update_geom:
            point = ST_SetSRID(
                ST_MakePoint(db_obj.longitude, db_obj.latitude), 
                4326
            )
            setattr(db_obj, "geom", point)
        
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, *, location_id: int) -> Optional[Location]:
        """Delete a location"""
        obj = await self.get(db, location_id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj


location = CRUDLocation()

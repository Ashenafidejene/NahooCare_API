import uuid
from fastapi import HTTPException
from db.mongodb import database
from models.healthcare_model import HealthcareCenter
from schemas.healthcare_schema import HealthcareCenterCreate, HealthcareSearch ,HealthcareCenterUpdate, HealthcareSearchEngin, HelathcareCenterRespons
from bson import ObjectId
from pymongo import GEOSPHERE
import logging

from schemas.saved_search_schemas import SavedSearchCreate
from services.saved_search_service import create_search_record

collection = database["healthcare_centers"]

#Ensure geospatial indexing for location-based search
collection.create_index([("location", GEOSPHERE)])

async def create_healthcare_center(center: HealthcareCenterCreate):
    try:
        existing_center = await collection.find_one({"name": center.name})
        if existing_center:
            raise HTTPException(status_code=400, detail="Healthcare name already exists")

        center_data = center.dict()
        
        center_data["location"] = {"type": "Point", "coordinates": [center.longitude, center.latitude]} 
        # Geospatial field
        center_data["center_id"] = "center_id_" + center.name
        result = await collection.insert_one(center_data)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create healthcare center")

        return True 

    except Exception as e:
        logging.error(f"Error creating healthcare center: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def search_healthcare_centers(user_id:str , search_data: HealthcareSearch):
    """
    Search for healthcare centers based on specialty and location.

    Args:
        search_data (HealthcareSearch): Search criteria including specialty, latitude, longitude, and max distance.

    Returns:
        List of healthcare centers matching the criteria.

    Raises:
        HTTPException: If no centers are found or an error occurs.
    """
    try:
        query = {
            "specialists": {"$in": search_data.specialties},  # Checks if any specialty matches
            "location": {
                "$near": {
                    "$geometry": {"type": "Point", "coordinates": [search_data.longitude, search_data.latitude]},
                    "$maxDistance": search_data.max_distance_km * 1000  # Convert km to meters
                }
            }
        }
        
        centers = await collection.find(query, {"_id": 0}).to_list(10)  # Excludes _id, limits to 10
        
        if not centers:
            raise HTTPException(status_code=404, detail="No matching healthcare centers found")
            
        return centers

    except Exception as e:
        logging.error(f"Error searching healthcare centers: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    except Exception as e:
        logging.error(f"Error searching healthcare centers: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
async def update_healthcare_center(center_id: str, update_data: HealthcareCenterUpdate):
    try:
        update_data_dict = update_data.dict(exclude_unset=True)
        if not update_data_dict:
            raise HTTPException(status_code=400, detail="No update data provided")

        result = await collection.update_one({"center_id": center_id}, {"$set": update_data_dict})
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes were made")

        return {"message": "Healthcare center updated successfully"}

    except Exception as e:
        logging.error(f"Error updating healthcare center: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
async def delete_healthcare_center(center_id: str):
    try:
        result = await collection.delete_one({"center_id": center_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Healthcare center not found")

        return {"message": "Healthcare center deleted successfully"}

    except Exception as e:
        logging.error(f"Error deleting healthcare center: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def search_engin_health_care_center(user_id: str, search_data: HealthcareSearchEngin):
    try:
        query = {}
        
        # Name search (case-insensitive partial match)
        if search_data.name:
            query["name"] = {"$regex": f".*{search_data.name}.*", "$options": "i"}
        
        # Specialty search (supports single or multiple specialties)
        if search_data.specialty:
            if isinstance(search_data.specialty, list):
                query["specialists"] = {"$in": search_data.specialty}  # Any of these specialties
            else:
                query["specialists"] = search_data.specialty  # Exact match
        
        # Location filter (if coordinates provided)
        if all([search_data.latitude, search_data.longitude, search_data.max_distance_km]):
            query["location"] = {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [search_data.longitude, search_data.latitude]
                    },
                    "$maxDistance": search_data.max_distance_km * 1000
                }
            }
        
        # Execute query with projection and limit
        centers = await collection.find(
            query,
            {"_id": 0}  # Exclude MongoDB _id field
        ).to_list(10)
        
        if not centers:
            raise HTTPException(
                status_code=404,
                detail="No healthcare centers found matching your criteria"
            )
        
        # Log the successful search
        search_record = SavedSearchCreate(
            user_id=user_id,
            search_id=str(uuid.uuid4()),
            search_parameters=search_data.model_dump(),
            results_count=len(centers),
            Analysis_id = "None"
        )
        await create_search_record(search_record)
        
        return centers
    
    except Exception as e:
        logging.error(f"Search error for user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while searching for healthcare centers"
        )

    except Exception as e:
        logging.error(f"Error searching healthcare centers: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    except Exception as e:
        logging.error(f"Error searching healthcare centers: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
async def get_healthcareCenter(name: str):
    try:
        existing_center = await collection.find_one({"name": name})
        
        if not existing_center: 
            raise HTTPException(status_code=404, detail="Healthcare Center not found")
            
        if "_id" in existing_center:
            existing_center['_id'] = str(existing_center['_id'])
            
        return HelathcareCenterRespons(
            center_id=existing_center["center_id"],
            name=existing_center["name"],
            address=existing_center["address"],
            latitude=existing_center["latitude"],
            longitude=existing_center["longitude"],
            specialists=existing_center["specialists"],
            contact_info=existing_center["contact_info"],
            available_time=existing_center["available_time"]
        )
    except Exception as e:
        logging.error(f"Error getting healthcare center: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


import uuid
from db.mongodb import database
from models.first_aid_guide_model import FirstAidGuide
from schemas.first_aid_guide_schemas import FirstAidGuideCreate, FirstAidGuideResponse, FirstAidGuideUpdate
from bson import ObjectId

collection = database["first_aid_guides"]

# Create a New First Aid Guide
async def create_first_aid_guide(guide_data: FirstAidGuideCreate):
    """
    Creates a new first aid guide in the database.
    
    Checks if a guide with the same ID already exists.
    If not, inserts the new guide and returns its ObjectId as a string.
    
    Args:
        guide_data (FirstAidGuideCreate): The data for the new guide.
    
    Returns:
        str: The ID of the newly created guide, or None if the guide already exists.
    """
    guide_dict = guide_data.dict()
    guide_dict["guide_id"] =  str(uuid.uuid4()) # Generate a unique guide ID
    result = await collection.insert_one(guide_dict)
    return str(result.inserted_id)

# Get All First Aid Guides
async def get_all_first_aid_guides():
    """
    Retrieves all first aid guides from the database.
    
    Converts ObjectId to string for JSON compatibility.
    
    Returns:
        list: List of all first aid guides, or a message if no guides are found.
    """
    try:
        guides = []
        async for guide in collection.find():
            guide["_id"] = str(guide["_id"])  # Convert ObjectId to string
            guides.append(FirstAidGuideResponse(
                category=guide["category"],
                emergency_title=guide["emergency_title"],
                instructions=guide["instructions"],
                image_url=guide["image_url"],
            ))

        if not guides:
            return {"message": "No first aid guides found"}

        return guides

    except Exception as e:
        return {"error": str(e)}  # Handle errors

# Get a First Aid Guide by Guide ID
async def get_first_aid_guide(guide_id: str):
    """
    Retrieves a specific first aid guide by its guide ID.
    
    Args:
        guide_id (str): The ID of the guide to retrieve.
    
    Returns:
        dict: The first aid guide if found, or None if not.
    """
    guide = await collection.find_one({"guide_id": guide_id})
    if guide:
        guide["_id"] = str(guide["_id"])  # Convert ObjectId to string
    return guide

# Update an Existing First Aid Guide
async def update_first_aid_guide(guide_id: str, update_data: FirstAidGuideUpdate):
    """
    Updates an existing first aid guide with new data.
    
    Args:
        guide_id (str): The ID of the guide to update.
        update_data (FirstAidGuideUpdate): The data to update in the guide.
    
    Returns:
        int: The number of documents modified (1 if successful, 0 if not).
    """
    result = await collection.update_one({"guide_id": guide_id}, {"$set": update_data.dict(exclude_unset=True)})
    return result.modified_count

# Delete a First Aid Guide by Guide ID
async def delete_first_aid_guide(guide_id: str):
    """
    Deletes a first aid guide by its guide ID.
    
    Args:
        guide_id (str): The ID of the guide to delete.
    
    Returns:
        int: The number of documents deleted (1 if successful, 0 if not).
    """
    result = await collection.delete_one({"guide_id": guide_id})
    return result.deleted_count


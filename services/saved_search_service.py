from datetime import datetime
from db.mongodb import database
from models.saved_search_model import SavedSearch
from schemas.saved_search_schemas import SavedSearchCreate, getSavedSearch
from bson import ObjectId
from typing import List

collection = database["saved_searches-update"]

#  Add a New Search History
async def create_search_record(search: SavedSearchCreate):
    """
    Saves a new search history to the database.
    Args:
        search (SearchHistoryCreate): The search history data to be saved.
    Returns:
        str: The ID of the newly saved search history.
    """
    search_data = search.dict()
    search_data["created_at"] = datetime.utcnow().isoformat()
    result = await collection.insert_one(search_data)
    return True

# Get All Search Histories by User ID
async def get_user_search_history(user_id: str) -> list[getSavedSearch]:
    """
    Retrieves all search histories for a specific user.

    Args:
        user_id (str): The ID of the user whose search histories are being retrieved.

    Returns:
        List[dict]: A list of search histories associated with the user.
    """
    search_history = []
    async for history in collection.find({"user_id": user_id}):
        history["_id"] = str(history["_id"])  # Convert ObjectId to string for JSON serialization
        search_history.append(getSavedSearch(**history))
    return search_history

#  Delete a Search History by Search ID or User ID
async def delete_search_historyAll( user_id: str):
    """
    Deletes a search history by its unique search ID or all histories by user ID.

    Args:
        search_id (str, optional): The ID of the search history to be deleted.
        user_id (str, optional): The ID of the user whose search histories will be deleted.

    Returns:
        int: The count of deleted search histories (0 if not found).
    """

    try:
        result = await collection.delete_many({"user_id": user_id})
        
        return result.deleted_count
    except Exception as e:
        print(f"Error during deletion: {e}")
        return 0
async def delete_single_search_history(search_id:str):
    try:
        result = await collection.delete_one({"search_id": search_id})
        return result.deleted_count
    except Exception as e:
        print(f"Error during deletion: {e}")
        return 0
        
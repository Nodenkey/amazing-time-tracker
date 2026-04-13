from typing import List

from fastapi import APIRouter, HTTPException, status

from app.models import TimeEntry, TimeEntryCreate, TimeEntryUpdate
from app.store import (
    create_time_entry,
    delete_time_entry,
    get_time_entry,
    list_time_entries,
    update_time_entry,
)


router = APIRouter(prefix="/time-entries", tags=["time-entries"])


@router.get("/", response_model=List[TimeEntry])
async def get_time_entries() -> List[TimeEntry]:
    return list_time_entries()


@router.get("/{entry_id}", response_model=TimeEntry)
async def get_time_entry_by_id(entry_id: str) -> TimeEntry:
    entry = get_time_entry(entry_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": f"Time entry with id {entry_id} does not exist",
                "detail": None,
            },
        )
    return entry


@router.post("/", response_model=TimeEntry, status_code=status.HTTP_201_CREATED)
async def create_time_entry_endpoint(payload: TimeEntryCreate) -> TimeEntry:
    return create_time_entry(payload)


@router.patch("/{entry_id}", response_model=TimeEntry)
async def update_time_entry_endpoint(entry_id: str, payload: TimeEntryUpdate) -> TimeEntry:
    entry = update_time_entry(entry_id, payload)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": f"Time entry with id {entry_id} does not exist",
                "detail": None,
            },
        )
    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_time_entry_endpoint(entry_id: str) -> None:
    deleted = delete_time_entry(entry_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": f"Time entry with id {entry_id} does not exist",
                "detail": None,
            },
        )

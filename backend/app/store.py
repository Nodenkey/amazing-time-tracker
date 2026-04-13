from __future__ import annotations

from datetime import date, datetime
import uuid
from typing import Dict, List, Optional


from .models import TimeEntry, TimeEntryCreate, TimeEntryUpdate


# In-memory store: id -> entry dict
_store: Dict[str, Dict] = {}


def _seed_store() -> None:
    global _store
    if _store:
        return

    now = datetime.utcnow()
    entry1_id = str(uuid.uuid4())
    entry2_id = str(uuid.uuid4())

    _store = {
        entry1_id: {
            "id": entry1_id,
            "date": date(2026, 4, 12),
            "person_name": "Sara Gordic",
            "activity": "Sprint planning and backlog refinement",
            "duration_minutes": 90,
            "notes": "Reviewed Amazing Time Tracker scope and tasks.",
            "created_at": now,
        },
        entry2_id: {
            "id": entry2_id,
            "date": date(2026, 4, 13),
            "person_name": "Ato Toffah",
            "activity": "Designed backend API and data model",
            "duration_minutes": 120,
            "notes": "Defined FastAPI endpoints and in-memory store structure.",
            "created_at": now,
        },
    }


_seed_store()


def list_time_entries() -> List[TimeEntry]:
    return [TimeEntry(**data) for data in _store.values()]


def get_time_entry(entry_id: str) -> Optional[TimeEntry]:
    data = _store.get(entry_id)
    if not data:
        return None
    return TimeEntry(**data)


def create_time_entry(payload: TimeEntryCreate) -> TimeEntry:
    entry_id = str(uuid.uuid4())
    entry_dict = {
        "id": entry_id,
        "date": payload.date,
        "person_name": payload.person_name,
        "activity": payload.activity,
        "duration_minutes": payload.duration_minutes,
        "notes": payload.notes,
        "created_at": datetime.utcnow(),
    }
    _store[entry_id] = entry_dict
    return TimeEntry(**entry_dict)


def update_time_entry(entry_id: str, payload: TimeEntryUpdate) -> Optional[TimeEntry]:
    existing = _store.get(entry_id)
    if not existing:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        existing[key] = value

    _store[entry_id] = existing
    return TimeEntry(**existing)


def delete_time_entry(entry_id: str) -> bool:
    if entry_id not in _store:
        return False
    del _store[entry_id]
    return True

"""Tests for the session state persistence and checkpointing system."""

import pytest
from agents.storage import SessionStore


@pytest.fixture
def temp_store(tmp_path):
    return SessionStore(storage_dir=str(tmp_path / "sessions"))


def test_save_and_load_checkpoint(temp_store):
    session_id = "test-session-001"
    state = {"step": 2, "agent": "research_agent", "data": {"query": "AI"}}

    # Save state
    success = temp_store.save_checkpoint(session_id, state)
    assert success is True

    # Load state back
    loaded = temp_store.load_checkpoint(session_id)
    assert loaded == state


def test_load_nonexistent_checkpoint(temp_store):
    loaded = temp_store.load_checkpoint("nonexistent-session")
    assert loaded is None


def test_list_and_delete_sessions(temp_store):
    temp_store.save_checkpoint("sess-A", {"val": 1})
    temp_store.save_checkpoint("sess-B", {"val": 2})

    sessions = temp_store.list_sessions()
    assert sorted(sessions) == ["sess-A", "sess-B"]

    # Delete one
    assert temp_store.delete_session("sess-A") is True
    assert temp_store.list_sessions() == ["sess-B"]

    # Delete nonexistent
    assert temp_store.delete_session("sess-A") is False


def test_invalid_session_id(temp_store):
    with pytest.raises(ValueError):
        temp_store.save_checkpoint("", {"data": 1})

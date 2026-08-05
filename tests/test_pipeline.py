"""Tests for the pipeline orchestration and session checkpointing functionality."""

import pytest
from agents.pipeline import Pipeline
from agents.storage import SessionStore


def test_pipeline_execution():
    def step_one(x):
        return x + " -> step1"

    def step_two(x):
        return x + " -> step2"

    pipeline = Pipeline(steps=[step_one, step_two])
    result = pipeline.run("start")
    assert result == "start -> step1 -> step2"


def test_pipeline_with_session_checkpointing(tmp_path):
    storage_dir = str(tmp_path / "sessions")
    session_id = "pipe-session-123"

    def step_one(x):
        return x * 2

    def step_two(x):
        return x + 5

    pipeline = Pipeline(
        steps=[step_one, step_two],
        session_id=session_id,
        storage_dir=storage_dir,
    )

    result = pipeline.run(10)
    assert result == 25  # (10 * 2) + 5

    # Verify checkpoint was stored correctly
    store = SessionStore(storage_dir=storage_dir)
    checkpoint = store.load_checkpoint(session_id)
    assert checkpoint is not None
    assert checkpoint["step_index"] == 1
    assert checkpoint["last_output"] == "25"


def test_pipeline_add_step():
    pipeline = Pipeline()
    pipeline.add_step(lambda x: x + 1)
    assert len(pipeline.steps) == 1
    assert pipeline.run(5) == 6

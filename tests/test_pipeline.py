"""Tests for the Pipeline orchestration engine and session persistence."""

import os
import tempfile
import pytest
from agents.pipeline import Pipeline, AgentPipeline
from agents.result import AgentResult


def test_pipeline_basic_execution():
    """Test sequential execution of steps in a pipeline."""
    def step_one(x):
        return x + 1

    def step_two(x):
        return x * 2

    pipeline = Pipeline(steps=[step_one])
    pipeline.add_step(step_two)

    result = pipeline.run(5)
    assert result == 12


def test_pipeline_with_session_storage():
    """Test pipeline execution with session state checkpointing enabled."""
    with tempfile.TemporaryDirectory() as tmpdir:
        def step_func(x):
            return f"processed_{x}"

        pipeline = Pipeline(steps=[step_func], session_id="test_session", storage_dir=tmpdir)
        result = pipeline.run("data")
        assert result == "processed_data"
        
        # Verify checkpoint persistence
        store = pipeline.store
        checkpoint = store.load_checkpoint("test_session")
        assert checkpoint is not None
        assert checkpoint["last_output"] == "processed_data"


def test_pipeline_run_chain():
    """Test executing a comma-separated agent chain using a registry."""
    class MockRegistry:
        def get(self, name):
            if name == "echo":
                return lambda x: f"echo:{x}"
            elif name == "upper":
                return lambda x: x.upper()
            return None

    registry = MockRegistry()
    pipeline = Pipeline(registry=registry)

    res = pipeline.run_chain("echo, upper", "hello")
    assert isinstance(res, AgentResult)
    assert res.content == "ECHO:HELLO"


def test_pipeline_run_chain_object_methods():
    """Test registry agent execution fallback handling for .run(), .execute(), callables, and fallback strings."""
    class ObjectAgent:
        def run(self, x):
            return f"run:{x}"

    class ExecuteAgent:
        def execute(self, x):
            return f"exec:{x}"

    class SimpleAgent:
        def __str__(self):
            return "simple"

    registry = {
        "obj_run": ObjectAgent(),
        "obj_exec": ExecuteAgent(),
        "obj_simple": SimpleAgent(),
        "unknown": None
    }

    pipeline = Pipeline(registry=registry, session_id="chain_session")
    res = pipeline.run_chain("obj_run, obj_exec, obj_simple, unknown", "start")
    assert isinstance(res, AgentResult)
    assert "Executed unknown" in res.content


def test_agent_pipeline_alias():
    """Verify that AgentPipeline is correctly aliased to Pipeline."""
    assert AgentPipeline is Pipeline

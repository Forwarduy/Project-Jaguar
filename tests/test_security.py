"""Unit tests for Project Jaguar enterprise security and credential management."""

import os
import pytest
from agents.security import CredentialManager, requires_auth, SecurityContext


def test_credential_masking():
    """Test that sensitive secrets are properly masked."""
    secret = "sk-ant-api03-abcdefghijklmnopqrstuvwxyz123456"
    masked = CredentialManager.mask_secret(secret, visible_chars=4)
    assert masked.endswith("3456")
    assert masked.startswith("*")
    assert len(masked) == len(secret)

    # Test short secret
    short_secret = "abc"
    assert CredentialManager.mask_secret(short_secret) == "****"
    assert CredentialManager.mask_secret(None) == "****"


def test_requires_auth_decorator_success(monkeypatch):
    """Test successful authorization when token and enforcement are configured."""
    monkeypatch.setenv("JAGUAR_AUTH_TOKEN", "valid-secret-token")
    monkeypatch.setenv("JAGUAR_ROLES", "admin,operator")

    @requires_auth(required_role="operator")
    def dummy_secured_action():
        return "success"

    # Mock settings enforce_auth = True
    monkeypatch.setattr("agents.security.get_settings", lambda: type("Settings", (), {"enforce_auth": True})())

    result = dummy_secured_action()
    assert result == "success"


def test_requires_auth_missing_token(monkeypatch):
    """Test permission error when auth token is missing while enforcement is active."""
    monkeypatch.delenv("JAGUAR_AUTH_TOKEN", raising=False)

    @requires_auth()
    def dummy_secured_action():
        return "success"

    monkeypatch.setattr("agents.security.get_settings", lambda: type("Settings", (), {"enforce_auth": True})())

    with pytest.raises(PermissionError, match="Authentication token missing"):
        dummy_secured_action()


def test_requires_auth_role_denied(monkeypatch):
    """Test permission error when required role is not present."""
    monkeypatch.setenv("JAGUAR_AUTH_TOKEN", "valid-token")
    monkeypatch.setenv("JAGUAR_ROLES", "viewer")

    @requires_auth(required_role="admin")
    def dummy_admin_action():
        return "success"

    monkeypatch.setattr("agents.security.get_settings", lambda: type("Settings", (), {"enforce_auth": True})())

    with pytest.raises(PermissionError, match="Access denied. Required role: admin"):
        dummy_admin_action()


def test_security_context_model():
    """Test SecurityContext Pydantic model creation."""
    ctx = SecurityContext(principal_id="user_123", roles=["admin"])
    assert ctx.principal_id == "user_123"
    assert "admin" in ctx.roles
    assert ctx.is_authenticated is True

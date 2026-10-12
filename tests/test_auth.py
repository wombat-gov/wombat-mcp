"""Tests for authentication helpers."""

from __future__ import annotations

import uuid

from wafpass_mcp.auth import UserContext, role_sufficient


def test_role_sufficient_hierarchy() -> None:
    assert role_sufficient("admin", "engineer")
    assert role_sufficient("engineer", "engineer")
    assert not role_sufficient("ciso", "engineer")


def test_user_context_role_sufficient() -> None:
    ctx = UserContext(
        user_id=uuid.uuid4(),
        username="alice",
        role="engineer",
        is_active=True,
        access_token="token",
    )
    assert ctx.role_sufficient("clevel")
    assert not ctx.role_sufficient("admin")


def test_user_context_headers_forward_mandant_context() -> None:
    ctx = UserContext(
        user_id=uuid.uuid4(),
        username="alice",
        role="admin",
        is_active=True,
        access_token="token",
        mandant_context="550e8400-e29b-41d4-a716-446655440000",
    )
    assert ctx.headers()["Authorization"] == "Bearer token"
    assert ctx.headers()["X-Mandant-Context"] == "550e8400-e29b-41d4-a716-446655440000"


def test_user_context_headers_without_mandant_context() -> None:
    ctx = UserContext(
        user_id=uuid.uuid4(),
        username="alice",
        role="admin",
        is_active=True,
        access_token="token",
    )
    assert "X-Mandant-Context" not in ctx.headers()

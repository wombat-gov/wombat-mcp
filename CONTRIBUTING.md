# Contributing to wombat-mcp

Thank you for contributing to the Wombat MCP Bridge — the Model Context Protocol server that exposes Wombat REST endpoints as tools for AI assistants.

This document is intentionally short and points to existing files in the repository. For architecture details see `TECH.md`, and for user-facing documentation see `README.md`.

---

## What this project is

`wombat-mcp` sits between an MCP host (e.g. Claude Desktop) and the upstream Wombat API (`wombat-server`). It authenticates the AI client via the same Bearer token that Wombat issued, filters the visible tools by the user's role, and proxies every tool call back to Wombat so the backend can enforce row-level authorization.

Source layout:

```
wafpass-mcp/
├── wombat_mcp/
│   ├── main.py              # FastAPI app and MCP-over-SSE endpoints
│   ├── config.py            # Environment-based settings
│   ├── auth.py              # Token validation and user context
│   ├── openapi_mapper.py    # OpenAPI → MCP tool mapping
│   └── mcp_server.py        # MCP Server bridge
├── tests/                   # pytest suite
├── scripts/                 # Standalone SSE test clients
├── .github/workflows/       # CI and release automation
├── Dockerfile
├── pyproject.toml
├── .env.example
├── README.md
└── TECH.md
```

---

## Local development setup

1. Install the package and dev dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

2. Copy and edit the environment file:

   ```bash
   cp .env.example .env
   # Edit .env to point at your Wombat backend and token validation mode.
   ```

3. Start the bridge:

   ```bash
   python -m wombat_mcp.main
   ```

For a full stack, run `wombat-server` from `../wafpass-server` and then start the bridge with `WOMBAT_API_BASE_URL=http://localhost:8000`.

---

## Running checks

Before opening a pull request, run the same checks used in CI:

```bash
ruff check wombat_mcp tests scripts
mypy wombat_mcp tests scripts
pytest tests -q
```

The release workflow (`release.yml`) runs these exact commands before publishing to PyPI.

---

## Manual end-to-end checks

Use the standalone clients in `scripts/` against a running bridge:

```bash
# List tools visible to the token's role
python scripts/mcp_list_tools.py <Wombat_TOKEN>

# Call a tool and print the backend response
python scripts/mcp_call_tool_test.py <Wombat_TOKEN>

# Minimal client that prints init + first 10 tools
python scripts/mcp_client_test.py <Wombat_TOKEN>
```

---

## Adding or changing a tool mapping

Tool definitions are generated automatically from the Wombat OpenAPI spec, but role assignments and exclusions are maintained in `wombat_mcp/openapi_mapper.py`.

To change visibility or add a new backend endpoint:

1. Update `ROLE_MAP[(method, path)]` with the minimum required role.
2. Add auth/login/callback paths to `SKIP_OPERATIONS` if they should never be exposed.
3. If you change the bridge's own HTTP surface or lifecycle, update `wombat_mcp/main.py`.
4. If token validation behavior changes, update `wombat_mcp/auth.py` and `tests/test_auth.py`.
5. Update `README.md` and `TECH.md`.

---

## Pull request expectations

- Open PRs against the `main` branch.
- Keep changes focused on one concern per PR.
- Ensure `ruff check wombat_mcp tests scripts`, `mypy wombat_mcp tests scripts`, and `pytest tests -q` pass locally.
- Update documentation when behavior changes.
- Write clear commit messages that explain the *why*, not just the *what*.

---

## License and conduct

By contributing, you agree that your contributions will be licensed under the Apache License 2.0 (see `LICENSE`).

Please read and follow our `CODE_OF_CONDUCT.md` and `SECURITY.md`.

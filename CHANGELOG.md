# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Because this project is still on `0.x`, a minor release may contain breaking
changes; this release is the coordinated WAFPass → WOMBATpass rebrand.

## [0.2.0] - 2026-11-02

### Breaking changes

- Renamed the distribution and console scripts from `wafpass-mcp*` to
  **`wombat-mcp*`**.
- Renamed the import package from `wafpass_mcp` to **`wombat_mcp`**.
- Renamed the repository from `WAF2p/wafpass-mcp` to
  `wombat-gov/wombat-mcp`.
- Environment variables now use the `WOMBAT_*` prefix instead of `WAFPASS_*`.

Legacy compatibility is retained for one migration window:

- `wafpass-mcp`, `wafpass-mcp-stdio` and `wafpass-mcp-configure` remain
  deprecated console-script aliases.
- `import wafpass_mcp` is served by the shim in `wafpass_mcp/__init__.py`.
- `WAFPASS_*` settings are promoted to `WOMBAT_*` by
  `wombat_mcp.compat.promote_legacy_env()`.

These aliases are deprecated and will be removed in a future release.

### Changed

- Branding and documentation now use WOMBATpass; Docker/compose references
  build from `./wombat-mcp` and connect to `wombat-server`.
- Package metadata and repository URLs point at the `wombat-gov`
  organisation.
- The release version is `0.2.0`.

### Migration

1. Replace `pip install wafpass-mcp` with `pip install wombat-mcp`.
2. Replace `import wafpass_mcp` with `import wombat_mcp`.
3. Update MCP client configuration from `wafpass-mcp` to `wombat-mcp`
   (and the `-stdio` / `-configure` variants).
4. Rename `WAFPASS_*` environment variables to `WOMBAT_*`.
5. Update Docker/compose paths and CI pins from `wafpass-mcp` to
   `wombat-mcp` / `wombat-gov/wombat-mcp`.
6. Pin `wombat-mcp==0.2.0` for reproducible deployments.

### Companion releases

- `wombat-core` 1.2.0
- `wombat-server` 1.2.0
- `wombat-dashboard` 1.2.0
- `wombat-action` 0.2.0

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2026-08-14

### Changed

- Upgraded backend calls to use the versioned `/api/v1/*` endpoints on `wafpass-server`.
- Made stdio the default transport for password fetch and token handling.

### Added

- Smoke tests and integration test coverage for SSE transport and tool proxying.
- Translation layer for upstream server error messages into user-facing MCP error content.

## [0.1.0] - 2026-07-29

### Added

- Initial release of the WAF++ MCP Bridge.
- SSE transport exposing the MCP endpoint on port 3001.
- IdP-agnostic security model that trusts tokens issued by `wafpass-server` and forwards the original `Authorization` header.
- Role-aware tool filtering: `tools/list` only exposes tools the authenticated user is authorized to use.
- OpenAPI-driven argument validation against Pydantic models generated from the WAFpass OpenAPI spec.
- Docker Compose support for local development alongside the WAF++ stack.

[Unreleased]: https://github.com/WAF2p/wafpass-mcp/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/WAF2p/wafpass-mcp/compare/v0.1.0...v0.1.2
[0.1.0]: https://github.com/WAF2p/wafpass-mcp/releases/tag/v0.1.0

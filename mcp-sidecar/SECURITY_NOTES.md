# Security Scan Notes — mcp-sidecar-base

## Current Image: v0.1.3
Scanned: 2026-08-10 with Trivy 0.52.2

## Accepted Residual Risks

### CRITICAL (2) — Debian OS layer, will_not_fix upstream
| CVE | Package | Reason Accepted |
|---|---|---|
| CVE-2025-7458 | libsqlite3-0 | Sidecar does not use SQLite directly; unreachable code path |
| CVE-2023-45853 | zlib1g | Vulnerable function is zip-creation (minizip); sidecar never creates zip files |

### HIGH (3) — Go binary (`step` v0.30.6)
| CVE | Package | Reason Accepted |
|---|---|---|
| CVE-2026-56852 | golang.org/x/text | DoS only, requires malformed UTF-8 in cert fields |
| GHSA-hrxh-6v49-42gf | grpc-go | Requires bypassing mTLS auth layer first |
| CVE-2026-39822 | Go stdlib (os.Root) | No untrusted path input reaches this API in current usage |

## Mitigating Controls
- Distroless base: no shell, no package manager, minimal attack surface
- Non-root user (UID 65532) enforced via USER directive
- All inter-service traffic gated by mTLS via step-ca (unauthenticated attackers cannot reach app logic)

## Fixed in This Version
- CVE-2025-44005, CVE-2026-30836 (step-ca authz bypass / unauthenticated cert issuance) — fixed by upgrading step CLI 0.28.7 → 0.30.6
- CVE-2026-33815, CVE-2026-33816 (jackc/pgx memory-safety) — fixed via same step CLI upgrade (pgx v5.8.0 → v5.9.0+ vendored)

## Review Cadence
Re-scan on every rebuild. Re-evaluate this file when:
- Smallstep releases a new step-cli version (check grpc-go/x-text bumps)
- Debian ships a fix for libsqlite3-0 or zlib1g in bookworm
- Google updates gcr.io/distroless/python3-debian12 base digest

Last reviewed: 2026-08-10

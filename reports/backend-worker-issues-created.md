# backend-worker — Issues GitHub créées (SEC-001 à SEC-007)

Statut: `gh auth` validé et issues créées.

## Tableau final

| # | Issue | Priorité | Labels | URL |
|---|-------|----------|--------|-----|
| SEC-001 | Replace header-based auth with server-verified JWT | P0 | security, backend | https://github.com/barattaalexandre-collab/backend-worker/issues/1 |
| SEC-002 | Enforce tenant isolation in all DB reads/writes | P0 | security, backend, multi-tenant | https://github.com/barattaalexandre-collab/backend-worker/issues/2 |
| SEC-003 | Harden AI action execution and prompt-injection resistance | P1 | security, backend | https://github.com/barattaalexandre-collab/backend-worker/issues/3 |
| SEC-004 | Move pending actions to Redis with replay protection | P1 | security, backend | https://github.com/barattaalexandre-collab/backend-worker/issues/4 |
| SEC-005 | Add rate limits and usage quotas on AI endpoints | P1 | security, backend | https://github.com/barattaalexandre-collab/backend-worker/issues/5 |
| SEC-006 | Harden image upload and align body/schema limits | P2 | security, backend | https://github.com/barattaalexandre-collab/backend-worker/issues/6 |
| SEC-007 | Add security observability and incident runbooks | P2 | security, backend | https://github.com/barattaalexandre-collab/backend-worker/issues/7 |

## Ordre d'implémentation recommandé

1. SEC-001
2. SEC-002 + SEC-004 (en parallèle)
3. SEC-003 + SEC-005
4. SEC-006 + SEC-007

## Notes de pilotage

- Bloquer les merges applicatifs non-sécurité tant que SEC-001 et SEC-002 ne sont pas traitées.
- Exiger des PRs atomiques avec tests auto et section "Risk/Rollback".
- Maintenir décision commerciale **NO-GO** tant que P0/P1 non validées en staging.

Tu travailles sur le repo GitHub `barattaalexandre-collab/backend-worker`.

MISSION
Exécuter les correctifs sécurité SEC-001 à SEC-007 avec PRs atomiques, tests obligatoires, et preuves.

LIS D'ABORD CES FICHIERS
1) reports/backend-worker-audit-preliminary.md
2) reports/backend-worker-cloud-code-handoff.md
3) reports/backend-worker-github-issues-prompts.md
4) reports/backend-worker-issues-created.md
5) reports/backend-worker-deployment-status-and-next-step.md

RÈGLES NON NÉGOCIABLES
- Ne jamais faire confiance à `x-user-role`, `x-user-id`, `x-organization-id` venant du client.
- Toute auth/authz doit être serveur + testée automatiquement.
- Une issue = une branche = une PR.
- Chaque PR inclut: Threat addressed, Tests, Manual verification, Risk/Rollback, Residual risk.
- Interdiction de merger si tests sécurité KO.

ORDRE D'EXÉCUTION
1. SEC-001
2. SEC-002 + SEC-004 (parallèle possible)
3. SEC-003 + SEC-005
4. SEC-006 + SEC-007

DÉTAILS MINIMUM PAR TICKET
SEC-001: JWT serveur (signature/exp/iss/aud), `request.user`, suppression auth par headers client, tests 401/403/spoof.
SEC-002: isolation tenant sur toutes queries/mutations + ownership checks + tests cross-org.
SEC-003: validation stricte output NLU/tool, allowlist stricte, confirmation actions destructives, tests prompt injection.
SEC-004: pending actions sur Redis, TTL, single-use atomique, binding user/org/session, tests concurrence/rejeu.
SEC-005: rate-limit IP/user/org + quotas/budget tokens + réponses 429 + métriques.
SEC-006: aligner bodyLimit/Zod, magic bytes, MIME réel, dimensions/taille décodée, anti path traversal.
SEC-007: audit logs structurés, request-id, dashboards/alertes, runbooks incidents.

COMMANDES MINIMALES À EXÉCUTER À CHAQUE PR
- npm run typecheck
- npm test
- npm run lint (si présent)
- tests d'intégration ciblés du ticket

SORTIE ATTENDUE APRÈS CHAQUE PR
- URL PR
- Résumé des fichiers modifiés
- Résultats CI
- Preuves tests manuels (curl/Postman)
- `Closes #<issue>`

BLOCAGE PROD RESTANT
- Vérifier Redis Upstash en prod (UPSTASH_REDIS_REST_URL + UPSTASH_REDIS_REST_TOKEN) et valider smoke tests.

Commence maintenant par SEC-001 et ouvre la PR.

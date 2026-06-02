# Checklist compacte Claude Code (vérification SEC-001..007)
1) Lire: audit-preliminary, cloud-code-handoff, github-issues-prompts, issues-created, deployment-status, variants-rollout-checklist.
2) Vérifier SEC-001: JWT serveur, plus de trust headers client (`x-user-role/x-user-id/x-organization-id`).
3) Vérifier SEC-002: isolation tenant (`organization_id`) sur toutes lectures/écritures + tests cross-org.
4) Vérifier SEC-003: validation stricte NLU/tool output + anti prompt injection + confirmation actions sensibles.
5) Vérifier SEC-004: pending actions Redis (TTL + single-use + binding user/org/session + anti-rejeu).
6) Vérifier SEC-005: rate limits IP/user/org + quotas + budget tokens + réponses 429.
7) Vérifier SEC-006: upload hardening (magic bytes, MIME réel, limites alignées, anti traversal).
8) Vérifier SEC-007: audit logs sécurité + request-id + dashboards + runbooks.
9) Exécuter: `npm run typecheck`.
10) Exécuter: `npm test`.
11) Exécuter: `npm run lint` (si présent).
12) Rendu par ticket: `OK|PARTIEL|KO` + preuves (fichiers/lignes) + tests + risques restants + action suivante.
13) Rendu variantes: N. Marti SA / Demo Garage / Demo Bâti / Demo Ing / Demo Archi => `OK|PARTIEL|KO`.
14) Verdict global: `GO` ou `NO-GO` + raisons.
15) Si blocage: expliquer précisément ce qui manque et comment lever le blocage.

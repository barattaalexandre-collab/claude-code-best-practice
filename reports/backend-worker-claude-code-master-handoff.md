# backend-worker — Master handoff à copier dans Claude Code

## Mode d'emploi

1. Ouvre Claude Code dans le repo `/Users/alexandrebaratta/backend-worker`.
2. Copie-colle le bloc ci-dessous tel quel.
3. Demande l'exécution immédiate de SEC-001.

---

```txt
Tu travailles sur le repo GitHub `barattaalexandre-collab/backend-worker`.

OBJECTIF
Implémenter le hardening sécurité SEC-001..SEC-007 via PRs atomiques, testées et traçables.

LIS D'ABORD (obligatoire)
- reports/backend-worker-audit-preliminary.md
- reports/backend-worker-cloud-code-handoff.md
- reports/backend-worker-github-issues-prompts.md
- reports/backend-worker-issues-created.md
- reports/backend-worker-deployment-status-and-next-step.md

RÈGLES
1) Une issue = une branche = une PR.
2) Ne jamais faire confiance aux headers client `x-user-role`, `x-user-id`, `x-organization-id`.
3) Toute auth/authz doit être prouvée par tests automatisés.
4) Aucune PR sécurité sans: Threat addressed, Tests, Manual verification, Risk/Rollback, Residual risk.
5) Interdit de merger si tests sécurité en échec.

ORDRE D'EXÉCUTION
- SEC-001
- SEC-002 + SEC-004 (parallèle possible)
- SEC-003 + SEC-005
- SEC-006 + SEC-007

SEC-001 — JWT auth serveur
- Créer middleware JWT (signature, exp, iss, aud).
- Exposer identité fiable dans request.user.
- Remplacer authGuard pour dépendre de request.user.role (pas header brut).
- Refuser spoof headers.
Tests:
- JWT valide => OK
- JWT invalide/expiré => 401
- rôle insuffisant => 403

SEC-002 — Tenant isolation DB
- Ajouter garde-fous `organization_id` sur toutes lectures/écritures.
- Vérifier ownership avant update/delete.
- Durcir action-execution.service.ts.
- Couvrir CRUD critiques (crm/projects/documents/supply).
Tests:
- org A ne lit/écrit jamais org B.

SEC-004 — Pending actions Redis
- Remplacer store in-memory par Redis.
- Token: TTL + single-use + binding user/org/session.
- Consommation atomique anti-rejeu.
Tests:
- double confirmation concurrente: une seule passe
- rejeu token refusé

SEC-003 — AI action hardening
- Validation stricte tool/NLU output.
- Allowlist stricte champs/opérations.
- Vérification tenant ownership avant mutation.
- Confirmation explicite actions destructives.
- Journalisation intent -> proposed -> validated -> result.
Tests:
- prompt injection ne contourne pas authz
- pas d'action cross-org via endpoint IA

SEC-005 — Rate limit + budget
- Rate limit par IP/user/org.
- Quotas et budget tokens configurables.
- Réponse 429 standardisée.
Tests:
- burst throttled
- reset fenêtre correct

SEC-006 — Upload hardening
- Aligner bodyLimit Fastify et limites Zod.
- Vérifier magic bytes JPEG/PNG, MIME réel, dimensions/taille décodée.
- Rejeter payloads corrompus/suspects.
- Bloquer path traversal.
Tests:
- MIME spoofing refusé
- oversize rejeté tôt

SEC-007 — Observabilité sécurité
- Ajouter table logs sécurité + indexes (migration).
- Ajouter logSecurityEvent non bloquant.
- Dashboards 401/403/429, actions IA, coûts.
- Alertes + runbooks incidents.
Tests:
- champs de logs obligatoires présents
- simulation incident validée

COMMANDES MINIMALES PAR PR
- npm run typecheck
- npm test
- npm run lint (si présent)
- tests d'intégration du ticket

SORTIE ATTENDUE APRÈS CHAQUE PR
- URL PR
- Fichiers modifiés
- Résultats CI
- Preuves manuelles curl/Postman
- `Closes #<issue>`

BLOCAGE PROD RESTANT
Configurer Upstash Redis en production:
- UPSTASH_REDIS_REST_URL
- UPSTASH_REDIS_REST_TOKEN
Puis valider smoke tests post-déploiement.

Commence maintenant par SEC-001 et ouvre la PR.
```

---

## Note finale

Ce fichier est volontairement compact pour usage direct en prompt d'exécution Claude Code.

# Message prêt à coller dans Claude Code — backend-worker

> À copier-coller tel quel dans Claude Code, depuis le repo `/Users/alexandrebaratta/backend-worker`.

```txt
Tu es en mode exécution sécurisée sur le repo backend-worker.

# 0) Contexte
Stack: Node >=20, Fastify v4, TypeScript ESM, Supabase, OpenAI/Anthropic, Deepgram.
Problèmes critiques connus:
- Auth basée sur headers client falsifiables
- Risque fuite cross-org (service-role + filtres applicatifs)
- pending actions en mémoire
- rate limit insuffisant
- pipeline image insuffisamment durci

# 1) Règles d'exécution
1. Une issue = une branche = une PR.
2. Commits atomiques et descriptifs.
3. Ajouter tests auto pour chaque correctif sécurité.
4. Toute PR contient: Threat addressed, Tests, Manual verification, Risk/Rollback.
5. Interdit de merger si tests sécurité échouent.

# 2) Ordre / dépendances (obligatoire)
- SEC-001 (démarrer ici)
- SEC-002 (après SEC-001)
- SEC-004 (en parallèle de SEC-002 possible)
- SEC-003 (après SEC-001+SEC-002)
- SEC-005 (après SEC-001)
- SEC-006 (après SEC-003)
- SEC-007 (après SEC-002+SEC-004+SEC-005+SEC-006)

# 3) SEC-001 — JWT auth serveur
Objectif: supprimer toute confiance en x-user-role/x-user-id/x-organization-id.

## Implémentation attendue
- Créer `src/auth/jwt-auth.ts`:
  - parse bearer token
  - verify signature + exp + iss + aud
  - construire `request.user = { userId, organizationId, role }`
- Ajouter un hook Fastify global `preHandler` pour routes `/api/*`.
- Migrer `authGuard.ts` pour utiliser `request.user.role` uniquement.
- Tolérance transitoire optionnelle (feature flag) max 7 jours si migration frontend nécessaire.

## Tests
- JWT valide => 200
- JWT invalide => 401
- JWT expiré => 401
- Header spoof `x-user-role=owner` sans droit réel => 403/401

# 4) SEC-002 — tenant isolation DB
Objectif: aucune lecture/écriture cross-org.

## Implémentation attendue
- Revue complète routes/services DB.
- Pour chaque update/delete: vérification ownership (`organization_id`) avant mutation.
- Durcir `action-execution.service.ts` (`executeUpdate*`) pour imposer garde-fou org.
- Ajouter script d'audit local (liste des endpoints et vérification filtre org).

## Tests
- User org A ne peut pas lire/écrire entité org B.
- CRUD companies/contacts/opportunities/projects/tasks/phases couverts.

# 5) SEC-004 — pending actions Redis
Objectif: sortir l'état process-memory.

## Implémentation attendue
- Créer `pending-actions-store.ts` (interface + impl Redis).
- Stocker token pending avec TTL court.
- Binding fort token -> user_id/org_id/session_id.
- Consommation atomique (GETDEL ou transaction équivalente).
- Invalidation sur usage et expirations.

## Tests
- Rejeu token => refus.
- Double confirmation concurrente => une seule passe.
- Multi-instance simulée => comportement cohérent.

# 6) SEC-003 — prompt injection / NLU hardening
Objectif: empêcher exécution d'actions IA hors policy.

## Implémentation attendue
- Schéma strict du résultat NLU/tool output.
- Rejeter champs/ops hors allowlist.
- Vérifier ownership org avant chaque mutation issue de l'IA.
- Confirmation explicite pour actions destructives.
- Journaliser `intent -> proposed action -> validated action -> DB result`.

## Tests
- Prompts malveillants ne contournent pas authz.
- Pas d'action cross-org via endpoint IA.

# 7) SEC-005 — rate limiting et budget tokens
Objectif: contrôle abuse/cost.

## Implémentation attendue
- Configurer `@fastify/rate-limit` (IP + user + org).
- Quotas journaliers configurables.
- Enforcement budget tokens dans service de coûts IA.
- Réponse 429 standardisée + headers de quota.

## Tests
- Burst requests => throttling.
- Reset fenêtre => comportement attendu.

# 8) SEC-006 — upload image hardening
Objectif: durcir `photoBase64`.

## Implémentation attendue
- Aligner `bodyLimit` Fastify avec limites Zod.
- Vérification magic bytes JPEG/PNG.
- Vérification MIME réel + dimensions + taille décodée.
- Rejet payloads corrompus/suspects.
- Bloquer path traversal si écriture temporaire fichier.

## Tests
- Image valide JPEG/PNG passe.
- MIME spoofing rejeté.
- Oversize rejeté tôt.

# 9) SEC-007 — observabilité sécurité
Objectif: audit + runbooks + alerting.

## Implémentation attendue
- Migration SQL table audit (`security_audit_logs`).
- Service `logSecurityEvent()` non bloquant (fire-and-forget sûr).
- Dashboards: 401/403/429, actions IA, coûts.
- Alertes sur seuils incidents.
- Runbooks incidents: cross-org leak, abuse token, Redis outage.

## Tests
- Présence des champs logs critiques.
- Simulation incident + validation runbook.

# 10) Commandes de vérification minimales à exécuter
- npm run typecheck
- npm test
- npm run lint (si présent)
- tests d'intégration ciblés par issue

# 11) Fermeture des issues GitHub
Pour chaque PR mergée:
- Référencer `Closes #<issue>`
- Inclure SHA + résultats CI + preuves manuelles

Commence MAINTENANT par SEC-001. Ouvre PR avec code + tests + risk/rollback.
```

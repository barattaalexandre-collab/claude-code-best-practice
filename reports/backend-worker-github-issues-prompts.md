# backend-worker — Prompts GitHub Issues (SEC-001 → SEC-007)

## Usage immédiat

Envoie ce prompt maître à Cloud Code, puis demande-lui explicitement de lire **ce fichier** pour récupérer le contenu détaillé de chaque issue.

```txt
Tu travailles sur le repo GitHub backend-worker.

Étape 1: crée 7 issues sécurité (SEC-001 à SEC-007) dans l'ordre.
Étape 2: pour le corps de chaque issue, lis le fichier `reports/backend-worker-github-issues-prompts.md` et copie les sections détaillées SEC-001..SEC-007.
Étape 3: ne code rien, crée uniquement les issues.
Étape 4: renvoie un tableau final (issue number, title, url, priority, labels).

Contraintes:
- Titres exacts obligatoires.
- Labels obligatoires: security, backend, multi-tenant (+ priority:P0/P1/P2).
- Inclure: Why this matters, Scope, Implementation tasks, Acceptance Criteria, Test Plan, Out of Scope, Depends on, Blocks.
```

---

## Résumé des issues à créer

| # | Priorité | Contenu |
|---|----------|---------|
| SEC-001 | P0 | JWT auth — 12 tasks, 5 AC, curl tests |
| SEC-002 | P0 | Tenant isolation + migration companies/contacts — 14 tasks |
| SEC-003 | P1 | Prompt injection + NLU output validation — 11 tasks |
| SEC-004 | P1 | Redis pending actions + TTL + replay protection — 11 tasks |
| SEC-005 | P1 | Rate limits + budget enforcement — 10 tasks |
| SEC-006 | P2 | Magic bytes + bodyLimit + path traversal — 11 tasks |
| SEC-007 | P2 | Audit log table + runbook + alerting — 12 tasks |

---

## SEC-001 Replace header-based auth with server-verified JWT

**Priority**: P0  
**Labels**: `security`, `backend`, `multi-tenant`, `priority:P0`

```md
## Why this matters
Les headers client (`x-user-role`, `x-user-id`, `x-organization-id`) sont falsifiables.

## Scope
Mettre en place JWT serveur comme seule source d'identité.

## Implementation tasks
- [ ] Ajouter middleware JWT (signature, exp, nbf, iss, aud).
- [ ] Refuser les algorithmes non autorisés (allowlist alg).
- [ ] Mapper `sub` -> `request.user.id`.
- [ ] Mapper org active depuis claims + vérification DB membership.
- [ ] Supprimer l'usage authz de `x-user-role`.
- [ ] Supprimer l'usage authz de `x-user-id`.
- [ ] Logger les échecs auth sans exposer token.
- [ ] Uniformiser réponses 401/403.
- [ ] Ajouter utilitaire `requireAuth()` partagé.
- [ ] Ajouter utilitaire `requireRole()` basé DB/claims signés.
- [ ] Documenter contrat d'auth API.
- [ ] Ajouter migration doc frontend pour envoi Bearer token.

## Acceptance Criteria
- [ ] Toute route protégée exige JWT valide.
- [ ] Forgery headers sans JWT => 401.
- [ ] JWT valide sans rôle requis => 403.
- [ ] Aucun chemin n'utilise rôle client brut.
- [ ] Tests auth passent en CI.

## Test Plan
### Automated
- JWT valide/invalide/expiré/issuer invalide.
- Test de spoof `x-user-role: owner` => refus.

### Manual (curl)
- `curl -H "Authorization: Bearer <valid>" ...`
- `curl -H "x-user-role: owner" ...` sans JWT

## Out of Scope
- Permissions fines ressource par ressource (SEC-002).

## Depends on
- None

## Blocks
- SEC-002
- SEC-003
- SEC-005
```

---

## SEC-002 Enforce tenant isolation in all DB reads/writes

**Priority**: P0  
**Labels**: `security`, `backend`, `multi-tenant`, `priority:P0`

```md
## Why this matters
Service-role Supabase bypass RLS: un oubli de filtre org => fuite cross-tenant.

## Scope
Imposer tenant-bound queries partout + migration progressive des modules CRUD.

## Implementation tasks
- [ ] Inventaire complet des accès DB.
- [ ] Créer couche helper `tenantQuery(orgId)`.
- [ ] Imposer clause org pour reads (list/get/search).
- [ ] Imposer clause org pour writes (insert/update/delete).
- [ ] Vérifier ownership avant update/delete.
- [ ] Durcir `action-execution.service.ts`.
- [ ] Durcir routes `crm.ts`.
- [ ] Durcir routes `projects.ts`.
- [ ] Durcir routes `documents.ts`.
- [ ] Durcir routes `supply.ts`.
- [ ] Ajouter garde-fou global en preHandler.
- [ ] Ajouter tests attack-path cross-org.
- [ ] Ajouter tests non-régression CRUD multi-tenant.
- [ ] Ajouter métrique `cross_org_denied_count`.

## Acceptance Criteria
- [ ] Aucune lecture cross-org possible.
- [ ] Aucune mutation cross-org possible.
- [ ] CRUD companies/contacts/opportunities protégé.
- [ ] CRUD projects/tasks/phases protégé.
- [ ] Logs exploitables sur refus inter-tenant.

## Test Plan
### Automated
- Suite intégration A vs B sur chaque endpoint critique.
- Unit tests ownership guards.

### Manual
- Rejouer IDs d'une autre org via Postman/curl.

## Out of Scope
- Refonte complète RBAC avancé.

## Depends on
- SEC-001

## Blocks
- SEC-003
- SEC-007
```

---

## SEC-003 Harden AI action execution and prompt-injection resistance

**Priority**: P1  
**Labels**: `security`, `backend`, `multi-tenant`, `priority:P1`

```md
## Why this matters
Le LLM peut influencer des actions DB; prompt injection peut provoquer opérations non désirées.

## Scope
Encadrer strictement NLU + exécution d'actions.

## Implementation tasks
- [ ] Ajouter validator strict du JSON/tool-output NLU.
- [ ] Refuser champs/ops hors allowlist.
- [ ] Appliquer ownership org avant exécution.
- [ ] Exiger confirmation forte pour actions destructives.
- [ ] Ajouter drapeau `high_risk_action`.
- [ ] Isoler instructions système des données utilisateur.
- [ ] Quote/sanitize contexte notes/docs.
- [ ] Limiter outils accessibles au modèle.
- [ ] Ajouter trace complète decision chain.
- [ ] Tests adversariaux prompt injection.
- [ ] Tests cross-org via endpoint IA.

## Acceptance Criteria
- [ ] Aucun output NLU invalide n'est exécuté.
- [ ] Prompt injection n'altère pas authz.
- [ ] Actions sensibles nécessitent confirmation.
- [ ] Journalisation complète disponible.
- [ ] Tests sécurité IA verts.

## Test Plan
### Automated
- Corpus de prompts malveillants.
- Validation schéma stricte tool output.

### Manual
- Conversations adversariales ciblées.

## Out of Scope
- Changement fournisseur LLM.

## Depends on
- SEC-001
- SEC-002

## Blocks
- SEC-004
- SEC-006
```

---

## SEC-004 Move pending actions to Redis with replay protection

**Priority**: P1  
**Labels**: `security`, `backend`, `priority:P1`

```md
## Why this matters
Map in-memory non durable et non multi-instance.

## Scope
Externaliser pending actions dans Redis avec protections anti-rejeu.

## Implementation tasks
- [ ] Ajouter client Redis robuste (retry/timeout).
- [ ] Stocker pending action par token opaque.
- [ ] TTL court configurable.
- [ ] Lier token à user/org/session.
- [ ] Single-use via opération atomique.
- [ ] Invalider token après consommation.
- [ ] Rejeter token expiré.
- [ ] Rejeter token d'une autre session.
- [ ] Ajouter nettoyage/monitoring des expirations.
- [ ] Tests concurrence/multi-instance.
- [ ] Dashboard erreurs pending-token.

## Acceptance Criteria
- [ ] Workflow survit aux restarts.
- [ ] Token rejeu impossible.
- [ ] Binding identité/session/org respecté.
- [ ] Concurrence gérée sans race conditions.
- [ ] Tests multi-instance passent.

## Test Plan
### Automated
- Tests atomiques consommation unique.
- Tests charge légère simultanée.

### Manual
- Double confirmation depuis 2 clients.

## Out of Scope
- UX frontend de confirmation.

## Depends on
- SEC-003

## Blocks
- SEC-007
```

---

## SEC-005 Add rate limits and usage quotas on AI endpoints

**Priority**: P1  
**Labels**: `security`, `backend`, `priority:P1`

```md
## Why this matters
Sans limites: abus, DoS logique, coûts LLM imprévisibles.

## Scope
Rate limiting + budget enforcement sur endpoints IA.

## Implementation tasks
- [ ] Rate limit par IP.
- [ ] Rate limit par org.
- [ ] Rate limit par user.
- [ ] Fenêtres glissantes configurables.
- [ ] Quotas journaliers org/user.
- [ ] Budget tokens/jour configurable.
- [ ] Erreurs normalisées 429.
- [ ] En-têtes de quota restants.
- [ ] Alertes dépassement budget.
- [ ] Tests burst + reset fenêtre.

## Acceptance Criteria
- [ ] 429 renvoyé en dépassement.
- [ ] Quotas respectés par user/org.
- [ ] Budget token enforceable.
- [ ] Observabilité quotas disponible.
- [ ] Pas de régression sur trafic normal.

## Test Plan
### Automated
- Tests de charge ciblée bursts.
- Tests reset fenêtre/quotas.

### Manual
- Scripts curl de rafale.

## Out of Scope
- Politique de pricing produit.

## Depends on
- SEC-001

## Blocks
- SEC-007
```

---

## SEC-006 Harden image upload and align body/schema limits

**Priority**: P2  
**Labels**: `security`, `backend`, `priority:P2`

```md
## Why this matters
Incohérences limites et validation image incomplète = surface d'attaque accrue.

## Scope
Durcir upload image (base64) + aligner bodyLimit/Zod + protections chemin/nom fichier si stockage disque.

## Implementation tasks
- [ ] Aligner `bodyLimit` Fastify avec policy unique.
- [ ] Aligner limite Zod même policy.
- [ ] Valider magic bytes.
- [ ] Valider MIME réel.
- [ ] Contrôler dimensions max.
- [ ] Contrôler taille décodée.
- [ ] Rejeter base64 corrompu.
- [ ] Rejeter extensions/formats non autorisés.
- [ ] Bloquer path traversal si écriture fichier temporaire.
- [ ] Logger rejets sécurité.
- [ ] Tests payloads malveillants.

## Acceptance Criteria
- [ ] Payload hors limite rejeté avant logique métier.
- [ ] MIME spoofing détecté.
- [ ] Path traversal impossible.
- [ ] Rejets traçables.
- [ ] Tests upload sécurité verts.

## Test Plan
### Automated
- Fuzz inputs base64.
- Tests limite parser/schéma.

### Manual
- Jeux d'images valides/invalides.

## Out of Scope
- OCR/vision pipeline avancée.

## Depends on
- SEC-003

## Blocks
- SEC-007
```

---

## SEC-007 Add security observability, audit log table, runbook and alerting

**Priority**: P2  
**Labels**: `security`, `backend`, `priority:P2`

```md
## Why this matters
Sans observabilité sécurité, détection/réponse incident est trop lente.

## Scope
Créer socle observabilité sécurité + runbooks opérationnels.

## Implementation tasks
- [ ] Créer table `security_audit_logs` (migration SQL).
- [ ] Logger user/org/endpoint/action/result/trace_id.
- [ ] Ajouter corrélation request-id globale.
- [ ] Logger événements auth (401/403).
- [ ] Logger rate-limit (429).
- [ ] Logger actions IA sensibles.
- [ ] Dashboard auth failures.
- [ ] Dashboard quota/rate-limit.
- [ ] Dashboard coût tokens LLM.
- [ ] Alerting seuils critiques.
- [ ] Runbook fuite cross-org.
- [ ] Runbook incident Redis/pending tokens.

## Acceptance Criteria
- [ ] Logs exploitables pour forensics basique.
- [ ] Dashboards accessibles et utiles.
- [ ] Alertes testées.
- [ ] Runbooks validés (tabletop).
- [ ] Critères Go/No-Go objectivables.

## Test Plan
### Automated
- Tests présence champs de logs obligatoires.
- Tests migration table audit.

### Manual
- Simulation incidents + vérification alertes.

## Out of Scope
- Certification SOC2/ISO.

## Depends on
- SEC-002
- SEC-003
- SEC-004
- SEC-005
- SEC-006

## Blocks
- Go/No-Go production
```

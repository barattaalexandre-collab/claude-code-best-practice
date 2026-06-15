# Handoff complet à transmettre à Claude Code (Cloud Code)

## Objectif

Ce document est prêt à être copié-collé dans Claude Code pour qu'il implémente les corrections de sécurité et de robustesse de `backend-worker`.

Contexte: l'audit précédent était préliminaire (repo cible non présent localement). Ici, on transforme ça en plan d'exécution **opérationnel GitHub**.

---

## 1) Message prêt à envoyer à Claude Code

> Tu vas auditer et corriger intégralement le repo `backend-worker`.
>
> ## Exigences
> - Runtime: Node >=20, Fastify v4, TypeScript ESM, Supabase
> - Priorité absolue: sécurité multi-tenant et authz/authn
> - Tu dois produire des PRs GitHub atomiques (une thématique par PR)
> - Tu dois ajouter des tests automatisés pour chaque correction critique
> - Tu dois fournir un rapport final de preuves (fichiers, lignes, tests, logs)
>
> ## Travaux à faire (ordre obligatoire)
>
> ### PR-1 AuthN/AuthZ fondation
> 1. Supprimer la confiance en `x-user-role`/`x-user-id`/`x-organization-id` côté client.
> 2. Mettre en place vérification JWT serveur (signature, exp, iss, aud).
> 3. Créer middleware d'identité normalisé (`request.user`) depuis JWT.
> 4. Faire dériver les rôles depuis DB membership (pas depuis headers).
> 5. Appliquer contrôle d'appartenance user-org centralisé pour toutes routes `/api/*`.
> 6. Ajouter tests d'intégration HTTP:
>    - header forgery refusé
>    - JWT invalide refusé
>    - user d'une org A ne lit/écrit pas org B
>
> ### PR-2 Isolation multi-tenant + Supabase
> 1. Réduire usage service-role sur routes user-facing.
> 2. Quand service-role est indispensable: ajouter garde-fous systématiques org-bound dans couche service/repository.
> 3. Ajouter assertions serveur obligatoires sur `organization_id` pour toutes mutations.
> 4. Ajouter tests de non-régression cross-org sur CRUD companies/contacts/opportunities/projects/tasks.
>
> ### PR-3 Sécurisation flux IA (`ai.ts`)
> 1. Encapsuler exécution d'actions DB derrière policy engine strict (allowlist champs/opérations déjà existante + contrôles org ownership).
> 2. Empêcher prompt injection d'influencer permissions/outils:
>    - séparer instructions système et données utilisateur
>    - sanitize/quote contenu récupéré (notes/docs)
>    - confirmation explicite pour actions destructives
> 3. Journaliser chaîne de décision: intent -> action proposée -> validation -> action DB finale.
> 4. Ajouter tests:
>    - payload de prompt injection ne peut pas escalader privilèges
>    - action IA ne sort jamais du tenant
>
> ### PR-4 Pending actions robustes
> 1. Remplacer `pendingActionsMap` mémoire par Redis.
> 2. Token pending action: single-use + TTL court + binding `user_id/org_id/session_id`.
> 3. Ajouter anti-rejeu (consommation atomique) + invalidation au restart deploy.
> 4. Ajouter tests multi-instance simulés.
>
> ### PR-5 Rate limiting + abuse/cost controls
> 1. Ajouter rate limiting sur `/api/ai/message` (IP + org + user).
> 2. Ajouter quotas journaliers par org/user (configurable).
> 3. Ajouter alerting sur bursts/erreurs/facture LLM.
> 4. Tests: dépassement quotas et throttling.
>
> ### PR-6 Upload image/`photoBase64` hardening
> 1. Aligner limites: parser HTTP et schéma Zod (éviter 12MB vs 1.5MB incohérent).
> 2. Valider magic bytes, MIME réel, dimensions max, taille décodée.
> 3. Rejeter formats non supportés, métadonnées suspectes, bombes zip/images.
> 4. Tests de limites et inputs malveillants.
>
> ### PR-7 Observabilité & sécurité opérationnelle
> 1. Audit logs structurés (qui, org, endpoint, action, résultat).
> 2. Corrélation request-id end-to-end.
> 3. Tableaux de bord erreurs authz, rate-limit, actions IA, latence, coûts.
> 4. Runbook incident (fuite cross-org, token abuse, outage Redis).
>
> ## Contraintes de qualité
> - Couverture de tests minimale sur modules critiques: 80% lignes, 100% chemins authz critiques.
> - Chaque PR doit contenir:
>   - code
>   - tests
>   - migration/config si nécessaire
>   - section "Risk/rollback"
> - Interdit de merger si un test sécurité échoue.
>
> ## Livrables finaux
> 1. Tableau des vulnérabilités initiales vs statut corrigé.
> 2. Liste des endpoints prouvés tenant-safe.
> 3. Rapport de pentest interne (scripts/requêtes de repro).
> 4. Check-list Go/No-Go vente cochée avec preuves.

---

## 2) Découpage GitHub recommandé

Créer les issues suivantes:

1. `SEC-001 Replace header-based auth with server-verified JWT`
2. `SEC-002 Enforce tenant isolation in all DB reads/writes`
3. `SEC-003 Harden AI action execution and prompt-injection resistance`
4. `SEC-004 Move pending actions to Redis with replay protection`
5. `SEC-005 Add rate limits and usage quotas on AI endpoints`
6. `SEC-006 Harden image upload and align body/schema limits`
7. `SEC-007 Add security observability and incident runbooks`

Puis ouvrir une PR par issue, dans cet ordre.

---

## 3) Critères d'acceptation (DoD) par thème

## Auth
- Aucun rôle accepté depuis headers client.
- JWT invalide/expiré => 401.
- User hors org => 403.

## Tenant isolation
- Chaque query/mutation prouve la contrainte tenant.
- Tests d'attaque cross-org passent (attendu: refus).

## IA actions
- Aucune action destructive sans confirmation explicite.
- Prompt injection n'altère ni rôle ni périmètre d'accès.

## Pending tokens
- Token usage unique, TTL, binding fort identité/session/org.
- Fonctionne en multi-instance.

## Rate limit
- Throttling prouvé sous charge.
- Quotas configurables et observables.

## Image hardening
- Validation binaire + dimensions + taille décodée.
- Rejets sûrs et traçables.

---

## 4) Ce qui n'a pas pu être vérifié ici (à faire absolument côté Cloud Code)

1. Vérification ligne-par-ligne de `src/routes/public/ai.ts` (~2516 lignes).
2. Vérification exhaustive de `action-execution.service.ts` sur ownership org de chaque update.
3. Vérification de toutes les routes CRUD publiques (`crm.ts`, `projects.ts`, `documents.ts`, etc.).
4. Vérification de la config Fastify réelle (CORS, bodyLimit, hooks, preValidation).
5. Vérification des migrations SQL et contraintes DB effectives.
6. Vérification de la pipeline deploy Render + variables d'environnement actives.
7. Exécution tests d'intégration réels contre base de staging.

---

## 5) Template de commentaire PR (à imposer à Cloud Code)

- **Threat addressed**: (ex: header forgery -> privilege escalation)
- **Code changes**: fichiers + rationale
- **Security tests added**: liste + résultats
- **Manual verification**: étapes curl/Postman
- **Risk/rollback**: procédure de retour arrière
- **Residual risk**: ce qui reste à traiter

---

## 6) Décision business (claire)

Tant que PR-1 à PR-6 ne sont pas mergées et validées en staging, décision: **NO-GO vente**.

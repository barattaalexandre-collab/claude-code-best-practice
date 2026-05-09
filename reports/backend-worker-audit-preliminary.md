# Audit préliminaire — backend-worker (Les Précurseurs Lab)

## Portée et limite

Cet audit est **préliminaire** et fondé uniquement sur le brief fourni dans la demande.
Le code source réel du repo `backend-worker` (chemin annoncé: `/Users/alexandrebaratta/backend-worker/`) n'est pas présent dans cet environnement (`/workspace/claude-code-best-practice`).

Conséquence: je peux produire une évaluation de risque solide, mais **pas une vérification ligne par ligne** sans accès au dépôt cible.

## Verdict exécutif (sur la base du brief)

**État actuel: non vendable en l'état pour un contexte sensible.**

Raisons principales:
1. Authentification/autorisation côté routes publiques basée sur des headers client falsifiables.
2. Utilisation d'une clé Supabase service-role (bypass RLS) partout, donc la moindre erreur de filtre `organization_id` devient fuite cross-org.
3. Flux IA qui peut déclencher des actions d'édition DB avec état en mémoire non durable et tokens non liés à identité/session.
4. Couverture de tests insuffisante sur surfaces critiques (HTTP authz, multi-tenant isolation, exécution d'actions IA).

## Réponses aux 7 questions ciblées

### 1) Header-based auth suffisant sans JWT ?
**Non. Critique.**

Si `x-user-role`, `x-user-id`, `x-organization-id` sont pris depuis le client sans preuve cryptographique (JWT signé et vérifié), n'importe quel client peut forger `owner` et usurper une org.

### 2) Cross-org data leak possible via `x-organization-id` forgery ?
**Oui, risque élevé à critique.**

Avec Supabase service-role, RLS n'arrête pas les requêtes. Toute protection repose sur des filtres applicatifs corrects à 100% dans chaque query et chaque mutation.

### 3) `pendingActionsMap` in-memory = vulnérabilité CSRF/token confusion ?
**Risque élevé (intégrité + disponibilité).**

- Perte d'état au restart (actions pendantes perdues).
- Multi-instance: token créé sur instance A, validation sur B impossible sans store partagé.
- Token UUID seul non lié strictement à user/session/org/IP + TTL faible = confusion/rejeu possibles selon implémentation exacte.

### 4) Prompt injection via contenu utilisateur dans contexte LLM ?
**Oui, risque élevé.**

Dès qu'un LLM pilote des actions d'édition, il faut:
- séparation stricte données vs instructions,
- policy tool-side non contournable,
- confirmation utilisateur forte sur actions destructives,
- allowlists strictes des champs/opérations.

### 5) Rate limiting absent sur `/api/ai/message` ?
**Problème sérieux.**

Sans rate limit par IP + par org + par user, risque DoS/coûts LLM + brute-force logique métier.

### 6) `photoBase64` path — validation suffisante ?
**Probablement insuffisante si seule taille est validée.**

Il faut aussi: magic bytes, type MIME réel, dimensions max, stripping metadata, antivirus/scan si stockage temporaire, timeout/décodeur robuste.

### 7) Body limit 12MB vs Zod 1.5MB — incohérence ?
**Oui, incohérence de défense en profondeur.**

Le body parser accepte plus que le schéma métier. Cela augmente pression mémoire/CPU avant rejet métier.

## Plan de remédiation priorisé

## P0 (immédiat, bloquant production)
1. Remplacer l'auth headers par JWT vérifié serveur (signature, exp, aud, iss).
2. Ignorer tout rôle envoyé par le client; dériver rôle depuis claims + DB membership.
3. Imposer contrôle d'appartenance `user -> organization` centralisé middleware.
4. Désactiver usages service-role pour routes user-facing; préférer token utilisateur + RLS.

## P1 (très urgent)
1. Migrer `pendingActionsMap` vers Redis (TTL explicite, single-use, bind user_id/org_id/session_id).
2. Ajouter protection anti-rejeu + horodatage + nonce + invalidation sur consommation.
3. Ajouter rate limiting (IP/org/user), circuit breakers, quotas journaliers LLM.
4. Durcir pipeline image (`photoBase64`): type réel, dimensions, size stricte au niveau parser.

## P2 (important)
1. Tests d'intégration HTTP auth/authz multi-tenant (happy + attack paths).
2. Tests de non-régression cross-org sur toutes routes CRUD/AI.
3. Audit logs immuables: qui a demandé quoi, avec quels paramètres, quelle action DB finale.

## Critères "prêt à vendre"

- Isolation multi-tenant prouvée par tests automatiques + pentest.
- AuthN/AuthZ fondée sur identité vérifiée (pas headers trust).
- Traçabilité complète des actions IA -> DB.
- Contrôles coûts/abuse (rate limits, quotas, alerting).
- Reprise après incident (store distribué, pas d'état critique en mémoire process).

## Ce qu'il faut pour l'audit complet ligne par ligne

1. Accès au dépôt `backend-worker` (ou archive ZIP).
2. Fichiers de config runtime (sans secrets): env example, `render.yaml`, scripts.
3. Schéma DB/migrations complètes.
4. Jeu de tests et procédure de lancement locale/CI.


## Que faire maintenant (plan concret)

Si tu dois avancer **immédiatement** avec ce que tu as:

1. **Ne pas lancer en prod publique** tant que l'auth n'est pas refaite.
2. **Créer une branche hardening** dédiée sécurité.
3. **Bloquer les routes sensibles** derrière un reverse proxy avec allowlist IP temporaire.
4. **Implémenter JWT vérifié serveur** avant toute nouvelle feature.
5. **Ajouter rate limiting** sur `/api/ai/message` le jour même.
6. **Planifier un mini pentest** après correctifs P0/P1.

### Checklist Go / No-Go vente

- [ ] Auth JWT serveur en place (headers client non fiables ignorés)
- [ ] Contrôle d'appartenance user-org centralisé
- [ ] Aucune route user-facing en service-role sans garde-fous stricts
- [ ] pending actions stockées en Redis avec TTL + single-use + binding session
- [ ] Rate limits actifs (IP/org/user)
- [ ] Tests d'isolation multi-tenant passants
- [ ] Logs d'audit exploitables

Tant que ces cases ne sont pas cochées, la réponse pragmatique est: **No-Go vente**.

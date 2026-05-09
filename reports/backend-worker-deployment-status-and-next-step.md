# backend-worker — Statut déploiement sécurité + action manuelle restante

## État actuel (résumé)

### Migrations
- Migration 002: exécutée avec succès.
- Migration 003: exécutée avec succès.
- Vérifications OK:
  - `companies.organization_id` ajouté, backfill, NOT NULL, index.
  - `contacts.organization_id` ajouté, backfill, NOT NULL, index.
  - table `security_audit_log` créée + index.

### Render
- Variable `SUPABASE_ANON_KEY` ajoutée dans Render.
- Rebuild/déploiement déclenché automatiquement.

### Git / commits
- Commits SEC-001 à SEC-007 poussés sur `main`.
- Déploiement Render en cours sur commit `2ee52b3`.

## Action manuelle restante (bloquante production)

Configurer Redis Upstash pour éviter la perte des pending tokens au restart.

### Pourquoi
Sans Redis, le store pending retombe en mémoire process:
- fonctionne en dev,
- mais en prod les tokens `/api/ai/confirm` peuvent être perdus au redémarrage.

### Étapes exactes
1. Aller sur https://console.upstash.com
2. Créer une base Redis (plan gratuit possible)
3. Ouvrir les credentials REST
4. Ajouter dans Render:
   - `UPSTASH_REDIS_REST_URL=https://xxx.upstash.io`
   - `UPSTASH_REDIS_REST_TOKEN=AX...`
5. Sauvegarder pour déclencher un nouveau déploiement

### Vérification après config
- Appeler endpoint de confirmation IA en créant un pending token.
- Redémarrer le service.
- Vérifier que le token reste valide jusqu'à TTL (et single-use).

## Go/No-Go
- Tant que Redis Upstash n'est pas configuré en prod: **NO-GO partiel** (fonctionnel mais résilience insuffisante pour pending actions).
- Après config Redis + test de non-régression: lever le blocage.

## Smoke tests post-déploiement (à exécuter après ajout Redis)

1. Healthcheck API
   - `curl -i https://nmarti-backend-worker.onrender.com/health`
2. Endpoint IA (requête simple)
   - vérifier code HTTP 200/4xx attendu et absence d'erreur 5xx
3. Pending action workflow
   - créer une action pending
   - confirmer une fois => succès
   - reconfirmer même token => échec (single-use)
4. Restart test
   - redéployer/restart service
   - vérifier qu'un token pending non expiré reste géré correctement via Redis

## Critère de clôture opérationnelle

- Redis Upstash configuré + smoke tests validés + logs sans erreurs critiques = **GO**.

## Mise à jour handoff Claude Code

Le fichier `/Users/alexandrebaratta/backend-worker/reports/backend-worker-a-donner-a-claude-code-maintenant.md` a été créé dans le dépôt réel `backend-worker`. Il contient l'état prod, les URLs, l'état CORS, les 3 prochaines tâches, les commandes de vérification et les incidents à éviter.

La suite opérationnelle est décrite dans `reports/backend-worker-apres-creation-handoff-claude-code.md`: faire exécuter à Claude Code les tâches Redis/Upstash, CI, puis SEC-001 phase 2, sans ouvrir de chantier UX ou produit parallèle.

## Mise à jour Sprint 2 — CI / SEC-001 / Upstash

- CI GitHub Actions complétée et poussée au commit `363682c`: build + typecheck + tests + audit tenant.
- SEC-001 phase 2 bloqué: le frontend envoie encore `x-organization-id` sur chaque appel API; retirer le fallback backend casserait la prod. À traiter comme ticket séparé de refactor auth frontend vers `Authorization: Bearer <jwt>`.
- Upstash Redis reste en attente d'action manuelle Alexandre: créer la DB Redis et fournir/configurer `UPSTASH_REDIS_REST_URL` + `UPSTASH_REDIS_REST_TOKEN` dans l'environnement sécurisé.

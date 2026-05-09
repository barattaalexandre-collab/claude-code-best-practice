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

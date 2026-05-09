# Tableau de statut live — backend-worker

## Service

- Service URL: `https://nmarti-backend-worker.onrender.com`
- Statut: **LIVE**

## SEC-001..SEC-007 (état global)

| Ticket | Statut |
|---|---|
| SEC-001 | Déployé |
| SEC-002 | Déployé |
| SEC-003 | Déployé |
| SEC-004 | Déployé (avec fallback in-memory si Redis absent) |
| SEC-005 | Déployé |
| SEC-006 | Déployé |
| SEC-007 | Déployé |

## Infra

- Front: Vercel
- Back: Render
- DB: Supabase
- Redis Upstash: **non configuré (reste à décider/activer)**

## Incidents résolus

1. Incompatibilité `@fastify/rate-limit` vs Fastify v4 (fix appliqué)
2. `npm error Invalid Version` sur Render lié au lockfile (fix appliqué)

## 3 prochaines actions

1. Décision explicite Alexandre sur activation Upstash Redis en prod.
2. Activer smoke tests post-deploy bloquants en CI/CD.
3. Vérification variante par variante (N. Marti / Bâtiment / Architecte / Ingénieur / Garage FR/IT).

# Incident Render — incompatibilité `@fastify/rate-limit` / Fastify v4

## Incident

Le déploiement Render a échoué après intégration sécurité.

## Cause racine

Plugin incompatible avec la version de Fastify:

- erreur: `@fastify/rate-limit - expected '5.x' fastify version, '4.29.1' is installed`
- contexte: le projet tourne en Fastify v4, mais `@fastify/rate-limit@10` cible Fastify v5.

## Correctif appliqué

- Downgrade `@fastify/rate-limit` vers une version compatible Fastify v4 (`^9.x`).
- Validation locale annoncée: typecheck OK (`217 pass, 0 erreurs`).
- Commit/push correctif: `a67f788`.
- Render: redeploy auto déclenché après push.

## Matrice compatibilité (résumé)

| Composant | Version projet | Version plugin | Compatibilité |
|---|---:|---:|---|
| Fastify | 4.29.1 | `@fastify/rate-limit@10` | ❌ (attend Fastify 5.x) |
| Fastify | 4.29.1 | `@fastify/rate-limit@^9` | ✅ |

## Timeline

1. Deploy Render échoue au boot.
2. Inspection events/logs -> erreur peer/runtime Fastify plugin.
3. Downgrade `@fastify/rate-limit` vers `^9.x`.
4. Typecheck OK.
5. Commit/push `a67f788`.
6. Redeploy automatique Render.

## Actions préventives (4)

1. **Pinning de major**: verrouiller major des plugins Fastify selon major Fastify runtime.
2. **CI dependency check**: job vérifiant peerDependencies critiques (Fastify/plugins).
3. **Smoke boot test CI**: test de démarrage serveur (`node dist/index.js` ou équivalent) pour détecter crash au boot.
4. **Release checklist**: contrôle "dependency major drift" avant merge/release.

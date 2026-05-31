# backend-worker — SEC-001 PR 3 mini-plan: retrait du fallback `x-organization-id`

## Statut

- SEC-001 phase 2 est validé en production avec le bundle Lovable `BUFNQkkc`.
- Ce document transforme le mini-plan PR 3 reçu en plan d'exécution contrôlé.
- Audit complémentaire intégré: trois fichiers frontend construisent encore des headers manuellement et doivent être corrigés avant retrait backend du fallback.
- **Aucun code ne doit être modifié sans validation explicite d'Alexandre.**

## Objectif PR 3

Retirer le fallback d'authentification basé sur `x-organization-id` pour que les routes protégées dépendent uniquement d'un `Authorization: Bearer <token>` valide.

## Périmètre autorisé

### Frontend

Fichiers attendus dans `precurseur-shell`:

```text
src/services/config.ts
src/components/admin/AuditLog.tsx
src/services/documentService.ts
```

Actions prévues:

1. Dans `src/services/config.ts`, **ne pas toucher** au header `x-organization-id` utilisé par `_fetchAppToken()`.
   - Ce header fait partie du bootstrap normal: sans token existant, il permet d'obtenir le Bearer token applicatif.
   - Ce n'est pas le fallback backend à supprimer.
2. Dans `getApiHeaders()`, supprimer le header transitionnel:

   ```diff
   - "x-organization-id": ORG_ID,
   ```

3. Corriger les trois constructions manuelles de headers qui ne passent pas par `getApiHeaders()`:

   | Fichier | Action |
   |---|---|
   | `src/components/admin/AuditLog.tsx` | remplacer les headers manuels par `getApiHeaders()` |
   | `src/services/documentService.ts` | remplacer le premier bloc headers manuel par `...getApiHeaders()` |
   | `src/services/documentService.ts` | remplacer le second bloc headers manuel par `...getApiHeaders()` |

4. Conserver `Authorization: Bearer <token>` sur tous les appels API protégés.
5. Conserver temporairement `x-user-role` / `x-user-id` uniquement si le code existant les utilise encore et si leur retrait n'est pas inclus dans PR 3.
6. Ne pas modifier l'UX, les swimlanes, le pricing ou les rôles métier.

### Backend

Fichiers attendus dans `backend-worker`:

```text
src/auth/jwt-auth.ts
src/server.ts
```

Actions prévues:

1. Dans `src/auth/jwt-auth.ts`, supprimer le bloc fallback qui crée `request.user` à partir de `x-organization-id` quand aucun Bearer token n'est présent.
2. Après suppression, une requête protégée sans `Authorization: Bearer` doit recevoir `401 UnauthorizedError`.
3. Dans `src/server.ts`, retirer `x-organization-id` de `allowedHeaders` CORS.
4. Ne pas supprimer le chemin de validation Bearer HS256 applicatif.
5. Ne pas supprimer le chemin JWT Supabase existant.

## Vérification obligatoire avant code

Avant toute modification, Claude Code doit vérifier qu'aucune route ne lit encore directement `x-organization-id` comme source de vérité et qu'aucun appel frontend protégé ne construit encore ses headers sans `getApiHeaders()`:

```bash
# backend-worker
rg "x-organization-id" src/routes src/auth src/server.ts

# precurseur-shell
rg "x-organization-id|headers:" src/components src/services
```

Si une occurrence apparaît dans `src/routes`, arrêter et produire un diagnostic avant de coder.
Si un appel frontend protégé construit encore ses headers manuellement, le corriger avant de retirer le fallback backend.

## Tests attendus

### Tests à conserver

- `app-token.test.ts`: le test de bootstrap qui prouve que `/api/auth/app-token` peut générer le token applicatif à partir de `x-organization-id`.
- `app-token.test.ts`: le test qui prouve qu'un Bearer HS256 valide positionne `request.user` sans header organisation.
- `app-token.test.ts`: le test qui couvre le rôle par défaut quand `x-user-role` est absent.
- `jwt-auth.test.ts`: le chemin JWT Supabase existant.

### Tests à supprimer ou adapter

Supprimer les trois tests qui valident explicitement l'ancien fallback header-only dans `jwt-auth.test.ts`.

Exemples de comportements à supprimer:

- `sets request.user with anonymous id when no Authorization but x-organization-id present`
- `uses x-user-role from header in fallback path when provided`

### Tests à ajouter

Ajouter deux tests de non-régression explicites:

```text
throws UnauthorizedError when no Authorization header, even if x-organization-id is present
sets organizationId from Bearer token, not from x-organization-id header
```

Ces tests doivent vérifier qu'une requête protégée sans Bearer token ne peut plus être authentifiée par `x-organization-id` seul, et qu'un header `x-organization-id` contradictoire ne surcharge pas l'organisation portée par le token.

## Commandes de validation locale attendues

Dans `backend-worker`:

```bash
npm run typecheck
npm test
npm run lint
```

Si `npm run lint` n'existe pas, le signaler sans bloquer la validation.

Dans `precurseur-shell`, lancer au minimum le contrôle disponible du projet, par exemple typecheck/build/test selon les scripts présents dans `package.json`.


## Ordre d'exécution sécurisé

L'ordre backend-first est refusé car il crée une fenêtre de 401 en production: les appels frontend qui construisent encore leurs headers manuellement casseraient dès que le fallback backend disparaît.

Ordre validé:

1. **Frontend d'abord**: corriger `AuditLog.tsx` et `documentService.ts` pour utiliser `getApiHeaders()`, puis supprimer `x-organization-id` de `getApiHeaders()` uniquement. Ne pas toucher à `_fetchAppToken()`.
2. Publier Lovable et vérifier en production que les appels concernés envoient bien `Authorization: Bearer <token>`.
3. **Backend ensuite**: supprimer le fallback dans `jwt-auth.ts` et retirer `x-organization-id` des `allowedHeaders` CORS.
4. Déployer Render.
5. Lancer les smoke tests production.
6. Nettoyer/adapter les tests de fallback et ajouter les tests Bearer-only dans la même PR ou dans un commit immédiatement associé, puis vérifier que la suite passe au vert.

## Smoke tests production après déploiement

Après merge/push et déploiement Render + Lovable:

```bash
# 1. Sans token: 401 attendu
curl -s -o /dev/null -w "%{http_code}" \
  https://nmarti-backend-worker.onrender.com/api/projects

# 2. Avec token valide: 200 attendu
TOKEN=$(curl -s -X POST \
  https://nmarti-backend-worker.onrender.com/api/auth/app-token \
  -H "x-organization-id: d9621b65-4eb3-4aa9-9ff1-745f17b4c989" \
  | jq -r .token)

curl -s -o /dev/null -w "%{http_code}" \
  https://nmarti-backend-worker.onrender.com/api/projects \
  -H "Authorization: Bearer $TOKEN"

# 3. x-organization-id seul: 401 attendu
curl -s -o /dev/null -w "%{http_code}" \
  https://nmarti-backend-worker.onrender.com/api/projects \
  -H "x-organization-id: d9621b65-4eb3-4aa9-9ff1-745f17b4c989"
```

Validation PR 3 impossible si le smoke test avec token valide ne retourne pas `200`.

## Rollback

Déclencher rollback si le smoke test avec Bearer valide retourne autre chose que `200` après déploiement.

Plan de rollback:

1. Backend: `git revert HEAD` dans `backend-worker`.
2. Push du revert.
3. Attendre le redéploiement Render.
4. Frontend Lovable: revenir au commit/version précédente si le changement frontend est en cause; sinon ne rien changer côté Lovable.
5. Relancer les trois smoke tests.

## Surveillance post-déploiement

Pendant 15 minutes après déploiement:

1. Ouvrir Render Dashboard → service `nmarti-backend-worker` → Logs.
2. Filtrer ou surveiller:
   - `401`,
   - `403`,
   - `auth.missing_token`,
   - `auth.invalid_token`.
3. Seuil de rollback: plus de 3 erreurs `401` ou `403` en 5 minutes sur des routes protégées utilisées par l'application.

## Prompt exact à donner à Claude Code si Alexandre valide PR 3

```text
SEC-001 PR 3 est validée uniquement pour retirer le fallback x-organization-id.

Avant de coder, vérifie:
rg "x-organization-id" src/routes src/auth src/server.ts

Si une route lit encore directement x-organization-id, arrête et donne-moi le diagnostic.

Périmètre backend:
- src/auth/jwt-auth.ts: supprimer le fallback qui crée request.user depuis x-organization-id sans Bearer.
- src/server.ts: retirer x-organization-id de allowedHeaders CORS.
- garder la validation Authorization: Bearer HS256 applicative.
- garder la validation JWT Supabase.

Périmètre frontend:
- src/services/config.ts.
- src/components/admin/AuditLog.tsx.
- src/services/documentService.ts.
- ne pas toucher au x-organization-id de _fetchAppToken: c'est le bootstrap normal app-token.
- supprimer x-organization-id uniquement dans getApiHeaders().
- remplacer les headers manuels de AuditLog.tsx par getApiHeaders().
- remplacer les deux headers manuels de documentService.ts par ...getApiHeaders().
- garder Authorization: Bearer <token>.
- ne pas toucher à l'UX, aux swimlanes, au pricing ou aux rôles métier.

Tests:
- supprimer/adapter les tests de fallback header-only.
- ajouter deux tests: sans Authorization même avec x-organization-id => 401; Bearer token gagne sur un x-organization-id contradictoire.
- lancer npm run typecheck.
- lancer npm test.
- lancer npm run lint si disponible.

À la fin, donne-moi:
- fichiers modifiés,
- diff résumé,
- tests exécutés,
- preuve rg qu'il ne reste pas de fallback x-organization-id dans les routes/auth et pas de headers manuels protégés côté frontend,
- risques restants,
- rollback.

Stop après PR 3. Ne lance aucun autre chantier SEC-002..SEC-007.
```

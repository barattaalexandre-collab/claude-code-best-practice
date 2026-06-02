# backend-worker — prochaine action après Upstash: SEC-001 phase 2

## État maintenant

Upstash Redis est terminé.

D'après le retour d'exécution:

- DB Upstash `nmarti-backend-worker` créée en Frankfurt / Free,
- `UPSTASH_REDIS_REST_URL` sauvegardée dans Render,
- `UPSTASH_REDIS_REST_TOKEN` sauvegardé dans Render,
- redeploy Render live à 10:39,
- Redis REST répond `PONG`,
- `npm test`: 217/217 pass,
- typecheck: 0 erreur,
- lint: eslint non installé localement, non présent CI,
- aucun secret committé,
- TTL + GETDEL déjà présents dans `pending-actions-store.ts`,
- pending actions utilisent Redis en production.

Donc: **ne pas refaire Upstash**.

---

## Prochaine action unique

**Lancer SEC-001 phase 2, mais en mode ticket/sprint séparé.**

Pourquoi: le frontend envoie encore `x-organization-id` sur chaque appel API. Donc on ne peut pas supprimer le fallback backend brutalement.

La prochaine action n'est pas "supprime le fallback".

La prochaine action est:

> Migrer progressivement le frontend vers `Authorization: Bearer <jwt>`, puis seulement ensuite retirer la dépendance backend aux headers client.

---

## Ce que Claude Code doit faire maintenant

Claude Code doit faire **un mini-audit + plan**, puis attendre validation avant gros changements.

### Prompt exact à copier-coller

```text
Tu es dans le repo /Users/alexandrebaratta/backend-worker.

Upstash Redis est terminé. Ne touche plus à Upstash.
CI est déjà faite au commit 363682c. Ne refais pas la CI.

Nouvelle action unique: SEC-001 phase 2.

Objectif: migrer progressivement l'auth frontend/backend pour ne plus dépendre de x-organization-id comme source de vérité.

Contexte important:
- Le frontend envoie encore x-organization-id sur chaque appel API.
- Si on supprime brutalement le fallback backend, la production casse.
- Il faut donc faire une migration progressive.

Avant de modifier le code, fais uniquement un mini-audit et donne-moi un plan:

1. Où le frontend construit les appels API ?
2. Où x-organization-id, x-user-id, x-user-role sont ajoutés ?
3. Quelle librairie/auth fournit le JWT actuel ? Supabase ? autre ?
4. Comment récupérer le token côté frontend ?
5. Où le backend lit Authorization: Bearer <jwt> ?
6. Où le backend lit encore les headers x-* ?
7. Quel plan de migration sans casser la prod proposes-tu ?
8. Quels tests ajouteras-tu ?
9. Quels fichiers modifieras-tu ?
10. Quel rollback proposes-tu ?

Ne modifie aucun fichier tant que je n'ai pas validé ton mini-audit.

Périmètre autorisé pour le plan:
- frontend API client / fetch wrapper / axios wrapper,
- ajout Authorization: Bearer <jwt>,
- backend auth middleware si nécessaire,
- tests 401 / 403 / header forgery,
- tests de non-régression pour appels existants.

Interdictions:
- ne supprime pas le fallback backend maintenant,
- ne casse pas la prod,
- ne touche pas à l'UX,
- ne touche pas aux swimlanes,
- ne touche pas au pricing,
- ne refais pas Upstash,
- ne fais pas de gros refactor non lié à l'auth.

Réponse attendue maintenant:
- mini-audit,
- plan en 2 ou 3 PR maximum,
- risques,
- tests,
- rollback.
```

---

## Si le mini-audit est bon

Ensuite seulement, autoriser une première PR très limitée:

```text
OK pour PR 1 uniquement.

Objectif PR 1:
- ajouter Authorization: Bearer <jwt> côté frontend sur les appels API,
- garder temporairement les headers existants si nécessaire pour compatibilité,
- ne pas supprimer le fallback backend,
- ajouter tests ou preuves que les appels API continuent de fonctionner,
- documenter rollback.

Ne commence pas PR 2 tant que PR 1 n'est pas validée.
```

---

## Ordre recommandé des PRs SEC-001 phase 2

### PR 1 — Frontend envoie Authorization Bearer

- Identifier le client API central.
- Récupérer le JWT depuis l'auth existante.
- Ajouter `Authorization: Bearer <jwt>` aux appels API.
- Garder temporairement compatibilité headers existants si nécessaire.
- Tests / smoke front-back.

### PR 2 — Backend privilégie JWT + membership DB

- Lire `Authorization` en priorité.
- Dériver user/org/role depuis JWT + DB membership.
- Ne plus faire confiance aux headers x-* comme vérité.
- Garder fallback strictement temporaire si nécessaire avec logs de dépréciation.
- Tests 401/403/header forgery.

### PR 3 — Suppression fallback headers

À faire seulement quand PR 1 et PR 2 sont déployées et validées.

- Supprimer fallback x-organization-id / x-user-id / x-user-role.
- Tests cross-org.
- Déploiement surveillé.

---

## Ce que toi tu dois faire maintenant

1. Ouvrir Claude Code dans `/Users/alexandrebaratta/backend-worker`.
2. Coller le prompt de mini-audit ci-dessus.
3. Attendre son plan.
4. Me montrer le plan avant de lui dire de coder.

Ne lui dis pas encore "implémente tout".

---

## Décision après mini-audit reçu

Le mini-audit est cohérent: **on valide uniquement PR 1**.

Ne pas valider PR 2 ou PR 3 maintenant.

### Pourquoi PR 1 seulement

PR 1 est la plus sûre car elle ne change pas le comportement produit visible et ne supprime pas le fallback existant.

Objectif PR 1:

- centraliser l'usage de `request.user.organizationId` côté backend,
- remplacer dans les routes les lectures directes de `request.headers['x-organization-id']`,
- garder le fallback actuel dans `jwt-auth.ts`,
- ne pas toucher au frontend,
- ne pas introduire encore `/api/auth/app-token`,
- ne pas supprimer de headers,
- ne pas casser la prod.

### Message exact à donner à Claude Code maintenant

```text
Plan validé partiellement.

Tu peux commencer PR 1 uniquement.

Périmètre PR 1:
- Backend uniquement.
- Remplacer les lectures directes de request.headers['x-organization-id'] dans les routes par request.user.organizationId.
- Fichiers concernés selon ton audit:
  - src/routes/public/crm.ts
  - src/routes/public/documents.ts
  - src/routes/public/projects.ts
  - src/routes/public/supply.ts
  - src/routes/public/voice.ts
  - src/routes/public/ai.ts
- Garder intact le fallback actuel dans src/auth/jwt-auth.ts.
- Ne pas ajouter /api/auth/app-token maintenant.
- Ne pas modifier le frontend maintenant.
- Ne pas supprimer x-organization-id côté frontend.
- Ne pas faire PR 2 ni PR 3.

Tests attendus:
- npm run typecheck
- npm test
- npm run lint si disponible
- ajouter ou adapter un test prouvant que les routes utilisent request.user.organizationId, pas une relecture directe de x-organization-id.

À la fin, donne-moi:
- fichiers modifiés,
- diff résumé,
- tests exécutés et résultats,
- preuve qu'il ne reste plus de lecture directe x-organization-id dans les routes listées,
- risques restants,
- rollback.

Stop après PR 1. Attends validation avant PR 2.
```

### Critère de validation PR 1

PR 1 est validable si:

- les routes listées n'utilisent plus directement `request.headers['x-organization-id']`,
- `request.user.organizationId` est utilisé pour le scoping DB,
- le fallback `jwt-auth.ts` reste en place,
- aucun changement frontend n'est inclus,
- typecheck et tests passent,
- rollback est documenté.

---

## PR 1 terminée — décision suivante

PR 1 est terminée et commitée dans le repo `backend-worker`.

Retour d'exécution reçu:

- commit: `f90a00c`,
- 7 fichiers de routes publiques patchés,
- `requireOrgId()` lit maintenant `request.user.organizationId`,
- `feedback.ts` utilise `request.user?.organizationId` pour le logging,
- le fallback `x-organization-id` dans `jwt-auth.ts` reste intact,
- aucun changement frontend,
- typecheck: 0 erreur,
- tests: 217/217 pass.

Donc PR 1 est validée côté exécution.

### Prochaine action unique: PR 2, mais seulement si Alexandre valide

PR 2 introduit le Bearer token applicatif. C'est plus risqué que PR 1, donc il faut l'autoriser explicitement.

Objectif PR 2:

- backend: ajouter un second chemin de validation JWT HS256 applicatif,
- backend: ajouter `/api/auth/app-token`,
- frontend: appeler `/api/auth/app-token`, garder le token en mémoire,
- frontend: ajouter `Authorization: Bearer <token>` aux appels API,
- garder temporairement `x-organization-id` pendant la transition,
- ne pas supprimer le fallback backend,
- ne pas faire PR 3.

### Message exact à donner à Claude Code pour PR 2

```text
PR 1 est validée.

Tu peux préparer PR 2 uniquement.

Objectif PR 2:
Introduire un Bearer token applicatif sans casser la production.

Périmètre autorisé:
- Backend: ajouter APP_TOKEN_SECRET dans env/config avec validation forte.
- Backend: ajouter un endpoint POST /api/auth/app-token.
- Backend: l'endpoint peut utiliser x-organization-id temporairement pour générer un app-token, mais doit être protégé par un mécanisme interne documenté.
- Backend: ajouter dans jwtAuthHook un second chemin de validation HS256 applicatif avant ou à côté du chemin Supabase.
- Frontend: dans precurseur-shell/src/services/config.ts, ajouter getAppToken() avec cache mémoire.
- Frontend: ajouter Authorization: Bearer <token> dans getApiHeaders().
- Frontend: garder x-organization-id temporairement pendant la transition.

Interdictions:
- Ne supprime pas le fallback x-organization-id dans jwt-auth.ts.
- Ne supprime pas x-organization-id côté frontend.
- Ne fais pas PR 3.
- Ne change pas l'UX.
- Ne change pas les rôles métier.
- Ne touche pas aux swimlanes ni au pricing.

Tests attendus:
- npm run typecheck
- npm test
- npm run lint si disponible
- test endpoint /api/auth/app-token: token interne invalide => 401
- test JWT HS256 valide => request.user.organizationId correctement set
- test JWT HS256 expiré => 401
- test JWT Supabase valide toujours accepté si déjà couvert
- smoke test frontend: les appels API contiennent Authorization tout en gardant les headers existants

À la fin, donne-moi:
- fichiers modifiés,
- diff résumé,
- variables d'environnement à ajouter sans révéler de secret,
- tests exécutés et résultats,
- risques restants,
- rollback.

Stop après PR 2. N'exécute pas PR 3.
```

### Attention avant de lancer PR 2

Avant de dire oui à PR 2, Alexandre doit accepter qu'une variable secrète backend soit ajoutée:

`APP_TOKEN_SECRET`

Elle doit être générée comme secret fort, configurée dans Render, et jamais commitée.

---

## Décision APP_TOKEN_SECRET avant PR 2

La proposition est validable, avec une condition: **générer et configurer `APP_TOKEN_SECRET` avant de laisser Claude Code coder PR 2**.

### Ce qu'Alexandre doit faire avant PR 2

1. Générer un secret HS256 32 bytes minimum:

```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

2. Copier la valeur générée.
3. Aller dans Render:

```text
Render Dashboard → nmarti-backend-worker → Environment → Edit → Add variable
```

4. Ajouter:

```text
KEY: APP_TOKEN_SECRET
VALUE: <valeur hex 64 caractères>
```

5. Sauvegarder et laisser Render redéployer.

### Règles secret

- Ne jamais committer `APP_TOKEN_SECRET`.
- Ne jamais le mettre dans un fichier markdown.
- Ne jamais l'afficher dans un rapport.
- Ne jamais le coller dans un ticket public.
- Local `.env` autorisé uniquement car gitignored.
- Frontend: ne contient jamais `APP_TOKEN_SECRET`.

### Validation de la proposition technique

Le flow proposé est accepté pour PR 2:

1. Si pas de `Authorization: Bearer`, garder temporairement le fallback `x-organization-id`.
2. Si Bearer présent, tenter validation HS256 avec `APP_TOKEN_SECRET`.
3. Si HS256 OK, remplir `request.user = { id: 'app', organizationId, role: 'owner' }` ou équivalent documenté.
4. Si HS256 échoue, tenter le chemin Supabase existant.
5. Si tout échoue, retourner 401.

### Message à donner à Claude Code après ajout Render

```text
APP_TOKEN_SECRET est configuré dans Render.
Tu peux lancer PR 2 uniquement avec le plan validé.
Ne loggue jamais APP_TOKEN_SECRET.
Ne le commit jamais.
Ne touche pas à PR 3.
Garde le fallback x-organization-id pendant cette PR.
```

---

## PR 2 terminée — prochaine action push + vérification prod

PR 2 est terminée côté code, avec deux corrections faites avant commit.

### Commits reçus

- `backend-worker`: `a0fe745`
  - 7 fichiers: lib, route, hook, server, config, 2 fichiers de tests.
- `precurseur-shell`: `16d34a1`
  - `config.ts`.

### Corrections intégrées avant commit

1. `app-jwt.ts`: correction de l'expiration.
   - Avant: `exp < now`.
   - Après: `exp <= now`.
   - Raison: `expirySeconds=0` devait être considéré expiré.

2. `app-token.test.ts`: correction du mock Vitest.
   - Problème: `vi.mock` est hoisté avant initialisation de `TEST_SECRET`.
   - Fix: utiliser le littéral directement dans la factory `vi.mock`.

### Validation avant commit

- 11 fichiers modifiés.
- 233 tests passent.
- Backend commit OK.
- Frontend commit OK.

### Prochaine action unique

**Pousser les deux repos puis vérifier la production.**

1. Push `backend-worker` commit `a0fe745`.
2. Push `precurseur-shell` commit `16d34a1`.
3. Attendre le redeploy Render / frontend.
4. Vérifier que `APP_TOKEN_SECRET` est bien présent dans Render.
5. Vérifier qu'un appel frontend en production contient `Authorization: Bearer <token>`.
6. Vérifier que `x-organization-id` est encore présent temporairement pendant la transition.
7. Vérifier que les endpoints restent OK.

### Message exact à donner à Claude Code maintenant

```text
PR 2 est codée et commitée:
- backend-worker: a0fe745
- precurseur-shell: 16d34a1

Prochaine action unique: push les deux repos puis vérifie la prod.

À faire:
1. Push backend-worker.
2. Push precurseur-shell.
3. Attends les redeploys Render / frontend.
4. Confirme que APP_TOKEN_SECRET est configuré dans Render, sans afficher sa valeur.
5. Vérifie en production qu'un appel API frontend envoie Authorization: Bearer <token>.
6. Vérifie que x-organization-id est encore envoyé temporairement.
7. Vérifie que les endpoints fonctionnent toujours.
8. Donne-moi le statut final.

Ne fais pas PR 3.
Ne supprime pas le fallback x-organization-id.
Ne supprime pas x-organization-id côté frontend.
Ne loggue aucun secret.
Ne touche pas à l'UX, aux swimlanes ou au pricing.

Réponse attendue:
- push backend: oui/non + commit,
- push frontend: oui/non + commit,
- deploy backend: oui/non,
- deploy frontend: oui/non,
- Authorization Bearer visible en prod: oui/non/preuve sans token,
- x-organization-id conservé temporairement: oui/non,
- endpoints OK: oui/non,
- risques restants,
- prochaine recommandation.
```

### Après validation prod

Si tout est OK, la prochaine étape sera PR 3 plus tard: retirer le fallback headers.

Ne pas lancer PR 3 tant que la prod n'a pas prouvé que `Authorization: Bearer` fonctionne correctement.

---

## Vérification prod PR 2 — blocage Lovable

La vérification production montre que le backend est prêt, mais que le frontend Lovable n'a pas encore rebuildé le bundle.

### Résultat reçu

| Check | Résultat |
|---|---|
| Push backend `a0fe745` | ✅ |
| Push frontend | ✅ GitHub, commit `5eceb1d` |
| Deploy backend Render | ✅ endpoint `app-token` live |
| Deploy frontend Lovable | ❌ ancien bundle encore servi |
| `app-token` dans bundle prod | ❌ absent |
| `Bearer` dans bundle prod | ❌ absent |
| Backend répond 200 avec HS256 token | ✅ |
| Token expiré → 401 | ✅ |
| Fallback `x-organization-id` backend | ✅ |

### Diagnostic

Lovable n'a pas redéployé depuis le push GitHub. Son pipeline est découplé du repo GitHub.

Le bundle prod ne contient pas encore:

- `getAppToken`,
- `_fetchAppToken`,
- `Bearer`,
- `/api/auth/app-token`.

Donc le frontend prod tourne encore avec l'ancien `config.ts` en mode header-only.

### Risque actuel

Risque actuel: **zéro régression détectée**.

Pourquoi:

- le backend accepte maintenant les deux chemins,
- le fallback `x-organization-id` reste actif,
- le frontend prod continue à fonctionner en header-only,
- le Bearer token ne s'activera qu'après rebuild Lovable.

### Prochaine action unique pour Alexandre

Faire un rebuild manuel Lovable.

1. Aller sur https://lovable.dev
2. Ouvrir le projet concerné.
3. Cliquer sur **Publish** ou **Deploy**.
4. Si aucun bouton ne déclenche le build: faire un micro-changement dans l'éditeur Lovable, par exemple ajouter/retirer un espace dans un commentaire, puis sauvegarder/publier.
5. Attendre la fin du build.
6. Redemander à Claude Code de vérifier le bundle prod.

### Message exact à donner à Claude Code après Publish Lovable

```text
J'ai déclenché le Publish/Deploy Lovable.

Vérifie maintenant uniquement que le nouveau bundle frontend est bien en prod.

À faire:
1. Recharge la page prod Lovable.
2. Inspecte le bundle JS servi.
3. Confirme que `app-token` ou `/api/auth/app-token` est présent dans le bundle.
4. Confirme que `Bearer` est présent dans le bundle.
5. Vérifie qu'un appel API frontend envoie Authorization: Bearer <token>, sans afficher le token.
6. Vérifie que x-organization-id est encore envoyé temporairement.
7. Vérifie que les appels API fonctionnent toujours.

Ne fais pas PR 3.
Ne supprime pas le fallback backend.
Ne modifie pas le code.
Ne touche pas à l'UX, aux swimlanes ou au pricing.

Réponse attendue:
- Lovable rebuild: oui/non,
- app-token présent dans bundle: oui/non,
- Bearer présent dans bundle: oui/non,
- Authorization header observé: oui/non/preuve sans token,
- endpoints OK: oui/non,
- risque restant,
- recommandation suivante.
```

### Ne pas lancer PR 3 maintenant

PR 3 reste bloquée tant que Lovable n'a pas rebuildé et tant que `Authorization: Bearer` n'est pas observé en production.

---

## Lovable Publish manuel insuffisant — action suivante

Après déclenchement Publish/Deploy Lovable, la vérification montre encore l'ancien bundle:

- hash bundle inchangé: `YZCSZ5jp`,
- taille inchangée: `1028553` bytes,
- `app-token` absent,
- `Bearer` absent,
- `/api/auth/app-token` absent.

### Diagnostic corrigé

Lovable ne lit probablement pas automatiquement le push GitHub `5eceb1d`.

Architecture constatée:

> Lovable → push → GitHub

et non:

> GitHub → Lovable

Donc le deploy Lovable a republié l'ancienne version interne Lovable, pas le `config.ts` modifié dans GitHub.

### Risque actuel

Toujours zéro régression détectée:

- backend `app-token` live,
- fallback `x-organization-id` actif,
- frontend prod fonctionne encore en header-only,
- Bearer dormant tant que Lovable n'a pas le nouveau `config.ts`.

### Prochaine action unique pour Alexandre — Option A recommandée

Mettre à jour `config.ts` directement dans l'éditeur Lovable.

1. Ouvrir https://lovable.dev
2. Ouvrir le projet.
3. Dans l'éditeur Lovable, ouvrir:

```text
src/services/config.ts
```

4. Remplacer son contenu par le contenu local de:

```text
/Users/alexandrebaratta/precurseur-shell/src/services/config.ts
```

5. Sauvegarder.
6. Publier / Deploy.
7. Attendre le build.
8. Demander à Claude Code de revérifier le bundle.

### Option B si disponible

Si Lovable propose une fonctionnalité de sync inverse:

```text
Settings → GitHub sync → Pull from GitHub
```

Alors utiliser cette option pour importer le commit GitHub `5eceb1d` dans Lovable, puis publier.

### Message exact à donner à Claude Code après avoir collé `config.ts` dans Lovable

```text
J'ai mis à jour src/services/config.ts directement dans l'éditeur Lovable avec le contenu local de /Users/alexandrebaratta/precurseur-shell/src/services/config.ts, puis j'ai publié.

Vérifie uniquement que Lovable sert maintenant le nouveau bundle.

À faire:
1. Recharge la page prod avec cache disabled / no-cache.
2. Vérifie si le hash du bundle a changé par rapport à YZCSZ5jp.
3. Cherche dans le bundle: app-token, /api/auth/app-token, Bearer, getAppToken ou _fetchAppToken.
4. Vérifie qu'un appel API frontend contient Authorization: Bearer <token>, sans afficher le token.
5. Vérifie que x-organization-id est encore présent temporairement.
6. Vérifie que les appels API fonctionnent toujours.

Ne modifie pas le code.
Ne lance pas PR 3.
Ne supprime aucun fallback.
Ne loggue aucun secret.

Réponse attendue:
- nouveau hash bundle: oui/non + hash,
- app-token présent: oui/non,
- Bearer présent: oui/non,
- Authorization header observé: oui/non/preuve sans token,
- x-organization-id encore présent: oui/non,
- endpoints OK: oui/non,
- recommandation suivante.
```

### Blocage PR 3 maintenu

Ne pas lancer PR 3 tant que Lovable n'a pas intégré le nouveau `config.ts` et tant que `Authorization: Bearer` n'est pas confirmé en production.

---

## SEC-001 phase 2 complet — Lovable rebuild confirmé

### Résumé honnête de l'exécution

Le code PR 2 était déjà présent côté Lovable (`.env.production` commité + mergé dans une session précédente), mais le bundle production n'avait pas été rebuildé.

Le blocage venait du bouton **Update** Lovable: les `.click()` JavaScript étaient ignorés car `isTrusted=false`.

La solution finale a été d'utiliser `mcp__Claude_in_Chrome__computer.left_click`, qui génère un vrai clic navigateur (`trusted event`). Le clic réel a déclenché le build Lovable, puis le bundle a été rebuildé en environ 30 secondes.

### État final confirmé

SEC-001 phase 2 est complet côté production.

Bundle production:

```text
BUFNQkkc
```

Valeurs compilées observées dans le bundle:

```text
ge = "https://nmarti-backend-worker.onrender.com"
Z  = "live"
ea = "d9621b65-4eb3-4aa9-9ff1-745f17b4c989"
```

### Décision

PR 2 est validée en production.

La prochaine étape possible est PR 3: suppression progressive du fallback headers, mais **pas automatiquement**. PR 3 doit être lancée seulement après une décision explicite, avec un plan de rollback.

### Prochaine action recommandée

Ne rien lancer automatiquement.

Avant PR 3, demander à Claude Code un mini-plan de suppression fallback:

```text
SEC-001 phase 2 est validé en production.
Le bundle Lovable rebuildé est BUFNQkkc et utilise le backend live.

Prépare uniquement un mini-plan PR 3 pour retirer les fallbacks headers.
Ne code rien encore.

Le plan doit couvrir:
1. où supprimer x-organization-id côté frontend,
2. où supprimer le fallback x-organization-id dans jwt-auth.ts,
3. quels tests prouvent que Authorization: Bearer suffit,
4. quels smoke tests prod exécuter,
5. quel rollback si une route casse,
6. comment surveiller les 401/403 après déploiement.

Ne modifie pas le code tant que le plan n'est pas validé.
```

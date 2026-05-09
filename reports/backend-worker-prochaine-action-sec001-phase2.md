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

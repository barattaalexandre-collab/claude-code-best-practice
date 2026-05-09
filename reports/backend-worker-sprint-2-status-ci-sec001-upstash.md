# backend-worker — statut Sprint 2: CI, SEC-001 phase 2, Upstash

## Résumé exécutif

Sprint 2 n'est pas terminé, mais il est clarifié:

| Tâche | Statut | Décision |
|---|---|---|
| CI GitHub Actions | ✅ fait | Commit réel `363682c` poussé. CI complétée avec build + typecheck + tests + audit tenant. |
| SEC-001 phase 2 | ▶️ prochaine action | Mini-audit + plan de migration frontend vers `Authorization: Bearer <jwt>` avant code. |
| Upstash Redis | ✅ fait | DB créée, variables Render sauvegardées, redeploy live, Redis `PONG`, tests 217/217. |

---

## 1. CI GitHub Actions — terminé

### Ce qui a été fait

La CI existait déjà mais était incomplète. Elle a été complétée pour inclure:

- build,
- typecheck,
- tests,
- audit tenant.

### Commit réel

`363682c`

### Statut

✅ Tous les checks passent selon le retour d'exécution.

### Suite

Ne pas rouvrir ce chantier sauf si GitHub Actions échoue sur une PR réelle.

---

## 2. SEC-001 phase 2 — bloqué et à sortir du sprint immédiat

### Blocage constaté

Le frontend envoie encore `x-organization-id` sur chaque appel API.

Conséquence: retirer brutalement le fallback côté backend casserait l'application en production.

### Décision

SEC-001 phase 2 n'est pas une petite correction backend. Le scope réel est un **refactor auth frontend + backend**:

- frontend: envoyer `Authorization: Bearer <jwt>`,
- backend: dériver user/org/role depuis JWT + membership DB,
- migration progressive pour éviter de casser la prod,
- tests 401/403/header forgery/cross-org.

### Statut

⛔ Bloqué pour le sprint immédiat.

### Action suivante

Créer un ticket séparé:

`SEC-001-P2 Refactor frontend auth to Authorization Bearer JWT and remove organization header fallback`

### Prompt court pour le futur ticket

```text
SEC-001 phase 2 est bloqué car le frontend envoie encore x-organization-id sur chaque appel API.

Objectif du ticket:
- auditer tous les appels frontend API,
- remplacer les headers x-user-id/x-user-role/x-organization-id comme source de vérité par Authorization: Bearer <jwt>,
- conserver une migration progressive si nécessaire pour ne pas casser la prod,
- côté backend, dériver user/org/role depuis JWT + membership DB,
- ajouter tests 401, 403, header forgery refusé, cross-org refusé,
- documenter rollback.

Ne pas supprimer brutalement le fallback backend tant que le frontend n'est pas migré.
```

---

## 3. Upstash Redis — action manuelle requise

### Pourquoi c'est bloqué

Claude Code ne peut pas créer les credentials Upstash à la place d'Alexandre.

### Ce qu'Alexandre doit faire

1. Aller sur https://console.upstash.com
2. Créer une DB Redis.
3. Ouvrir les credentials REST.
4. Récupérer:
   - `UPSTASH_REDIS_REST_URL`
   - `UPSTASH_REDIS_REST_TOKEN`
5. Ajouter ces variables dans Render ou les transmettre à l'environnement sécurisé utilisé pour le déploiement.

### Ce qu'il ne faut pas faire

- Ne pas coller ces secrets dans GitHub ou dans un fichier `reports/`.
- Ne pas committer le token.
- Ne pas envoyer le token dans une conversation non sécurisée.

### Après ajout des credentials

Demander à Claude Code:

```text
Les credentials Upstash Redis sont configurés dans l'environnement de déploiement.
Vérifie maintenant que pending actions utilise Redis en production, que TTL et single-use fonctionnent, puis exécute les smoke tests associés.
Ne loggue pas les secrets.
```

---

## Prochaine action recommandée

1. Considérer la CI comme terminée avec commit `363682c`.
2. Créer/configurer Upstash Redis côté Alexandre.
3. Ouvrir un ticket séparé pour SEC-001 phase 2, car le frontend doit être refactoré vers `Authorization: Bearer <jwt>`.
4. Ne pas supprimer le fallback backend tant que le frontend n'est pas migré.

## Mise à jour après exécution Upstash

Upstash Redis est terminé selon le retour d'exécution:

- DB `nmarti-backend-worker` créée en Frankfurt / Free,
- variables `UPSTASH_REDIS_REST_URL` et `UPSTASH_REDIS_REST_TOKEN` sauvegardées dans Render,
- redeploy Render live à 10:39,
- Redis REST répond `PONG`,
- typecheck 0 erreur,
- `npm test` 217/217 pass,
- lint non applicable car eslint non installé localement et non présent en CI,
- aucun secret committé,
- pending actions utilisent Redis en production.

La prochaine action est maintenant `reports/backend-worker-prochaine-action-sec001-phase2.md`: demander à Claude Code un mini-audit SEC-001 phase 2 avant toute modification.

# backend-worker — message simple à donner à Claude Code

## À ne plus faire

Ne plus envoyer à Claude Code les longs summaries, tous les rapports, ou tout l'historique.

C'est trop confus.

Claude Code doit recevoir **une seule consigne courte**, dans le vrai repo `backend-worker`.

---

## Ce qu'il faut comprendre

On en est là:

1. **CI**: déjà fait, commit `363682c`. Ne pas refaire.
2. **SEC-001 phase 2**: bloqué, car le frontend envoie encore `x-organization-id`. Ne pas toucher maintenant.
3. **Upstash Redis**: seule prochaine action utile, mais il faut d'abord les credentials Upstash.

Donc la prochaine étape n'est pas "fais tout".

La prochaine étape est:

> Configurer Upstash Redis, puis demander à Claude Code de vérifier l'intégration Redis/pending actions.

---

## Ce que toi, Alexandre, dois faire maintenant

### Étape 1 — Créer Redis Upstash

1. Va sur https://console.upstash.com
2. Crée une base Redis.
3. Ouvre l'onglet REST credentials.
4. Récupère:
   - `UPSTASH_REDIS_REST_URL`
   - `UPSTASH_REDIS_REST_TOKEN`

### Étape 2 — Mettre les variables dans Render

Dans Render, ajoute les variables d'environnement:

```text
UPSTASH_REDIS_REST_URL=...
UPSTASH_REDIS_REST_TOKEN=...
```

Important:

- ne mets pas ces secrets dans GitHub,
- ne les mets pas dans un fichier markdown,
- ne les commit pas,
- ne les colle pas dans un ticket public.

### Étape 3 — Ensuite seulement, donne le message ci-dessous à Claude Code

---

## Message exact à copier-coller dans Claude Code

```text
Contexte court:
- La CI est déjà faite au commit 363682c. Ne la refais pas.
- SEC-001 phase 2 est bloqué car le frontend envoie encore x-organization-id. Ne touche pas à SEC-001 maintenant.
- Les credentials Upstash Redis sont maintenant configurés dans l'environnement Render.

Ta seule tâche maintenant:
Vérifier que l'application utilise bien Upstash Redis pour les pending actions en production.

À faire:
1. Inspecte le code pending actions / Redis.
2. Vérifie que UPSTASH_REDIS_REST_URL et UPSTASH_REDIS_REST_TOKEN sont lus depuis l'environnement.
3. Vérifie que le fallback mémoire n'est utilisé qu'en dev ou quand Redis n'est pas configuré.
4. Vérifie TTL + single-use des pending actions.
5. Lance les tests disponibles.
6. Donne une procédure de smoke test production sans exposer les secrets.

Ne fais pas:
- pas de refonte UX,
- pas de SEC-001 phase 2,
- pas de changement frontend auth,
- pas de pricing,
- pas de swimlanes,
- pas de gros refactor.

Commandes attendues:
- npm run typecheck
- npm test
- npm run lint si disponible

Réponse attendue:
- fichiers inspectés,
- fichiers modifiés si nécessaire,
- commandes exécutées,
- résultats,
- preuve que Redis est utilisé,
- preuve TTL / single-use,
- risques restants,
- rollback.
```

---

## Si Claude Code repart sur SEC-001

Répondre:

```text
Stop. SEC-001 phase 2 est explicitement hors périmètre maintenant.
Le frontend envoie encore x-organization-id, donc ce sera un ticket séparé frontend + backend.
Reviens uniquement à Upstash Redis / pending actions.
```

---

## Si Claude Code repart sur l'UX ou le produit

Répondre:

```text
Stop. UX, produit, swimlanes, pricing et assistant IA sont hors périmètre.
La seule tâche maintenant est Upstash Redis / pending actions.
```

---

## Ticket séparé à créer plus tard pour SEC-001 phase 2

Titre:

```text
SEC-001 phase 2 — migrer le frontend vers Authorization Bearer JWT
```

Description courte:

```text
Le frontend envoie encore x-organization-id sur chaque appel API.
On ne peut pas supprimer le fallback backend sans casser la prod.
Créer un sprint séparé pour migrer les appels frontend vers Authorization: Bearer <jwt>, puis faire dériver user/org/role côté backend depuis JWT + membership DB.
```

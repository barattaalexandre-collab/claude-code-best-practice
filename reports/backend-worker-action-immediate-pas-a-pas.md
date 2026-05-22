# backend-worker — action immédiate pas à pas

## La prochaine action, maintenant

**Prochaine action unique: configurer Upstash Redis et vérifier les pending actions.**

- **Pour qui ?** Claude Code avec Chrome.
- **Ce que toi tu fais ?** Tu ouvres Claude Code dans le repo `backend-worker`, tu colles le prompt ci-dessous, puis tu aides seulement si Chrome demande une connexion Upstash/Render.
- **Ce que Claude Code ne doit pas faire ?** Pas de SEC-001, pas d'UX, pas de pricing, pas de swimlanes, pas de refactor frontend.

---

## Étape 1 — Ouvre Claude Code au bon endroit

Dans Claude Code, ouvre le vrai repo:

```bash
cd /Users/alexandrebaratta/backend-worker
```

---

## Étape 2 — Copie-colle exactement ce prompt dans Claude Code

```text
Tu es dans le repo /Users/alexandrebaratta/backend-worker.

On avance une seule action à la fois.

ACTION UNIQUE MAINTENANT:
Configurer Upstash Redis pour les pending actions, puis vérifier que ça fonctionne.

Tu peux utiliser Chrome si nécessaire.

Contexte:
- La CI est déjà faite au commit 363682c. Ne la refais pas.
- SEC-001 phase 2 est bloqué parce que le frontend envoie encore x-organization-id. Ne touche pas à SEC-001.
- La seule tâche maintenant est Upstash Redis / pending actions.

Ce que tu dois faire pas à pas:

1. Vérifie dans le code où sont gérées les pending actions et Redis/Upstash.
2. Vérifie quelles variables d'environnement sont attendues:
   - UPSTASH_REDIS_REST_URL
   - UPSTASH_REDIS_REST_TOKEN
3. Avec Chrome, ouvre Upstash et crée une base Redis si elle n'existe pas.
4. Si une connexion ou validation humaine est nécessaire, arrête-toi et demande-moi de la faire.
5. Récupère les credentials REST dans Upstash, sans les écrire dans GitHub, sans les committer, sans les afficher dans un rapport.
6. Avec Chrome, ouvre Render et ajoute les deux variables d'environnement dans le service backend-worker.
7. Déclenche ou attends le redeploy Render.
8. Vérifie que l'application utilise Redis pour les pending actions.
9. Vérifie TTL + single-use si possible.
10. Lance les checks disponibles:
    - npm run typecheck
    - npm test
    - npm run lint si disponible
11. Donne-moi le résultat final.

Interdictions:
- Ne touche pas à SEC-001 phase 2.
- Ne modifie pas l'auth frontend.
- Ne fais pas de refonte UX.
- Ne touche pas aux swimlanes.
- Ne touche pas au pricing.
- Ne fais pas de gros refactor.
- Ne commit jamais les secrets Upstash.

Si tu es bloqué:
- dis exactement à quelle étape tu es bloqué,
- dis quelle action humaine est nécessaire,
- ne pars pas sur une autre tâche.

Réponse attendue à la fin:
- Upstash créé ou déjà existant: oui/non,
- variables Render ajoutées: oui/non,
- redeploy Render: oui/non,
- pending actions utilisent Redis: oui/non/preuve,
- TTL + single-use vérifiés: oui/non/preuve,
- commandes exécutées et résultats,
- risques restants,
- rollback.
```

---

## Étape 3 — Si Claude Code demande une connexion

Si Claude Code/Chrome demande de te connecter:

1. connecte-toi toi-même à Upstash ou Render,
2. ne colle pas les secrets dans le chat,
3. laisse Claude Code continuer après la connexion.

---

## Étape 4 — Si Claude Code part hors sujet

Copie-colle simplement:

```text
Stop. Ce n'est pas la tâche actuelle.
La seule tâche maintenant est Upstash Redis / pending actions.
Ne touche pas à SEC-001, UX, frontend auth, swimlanes ou pricing.
Reviens à l'étape Upstash/Render/Redis.
```

---

## Étape 5 — Quand c'est terminé

Tu dois obtenir une réponse avec:

- Upstash créé ou confirmé,
- variables Render ajoutées,
- redeploy fait,
- test pending actions Redis,
- `npm run typecheck`,
- `npm test`,
- `npm run lint` si disponible,
- risques restants,
- rollback.

Tant que tu n'as pas ça, on ne passe pas à SEC-001 phase 2.

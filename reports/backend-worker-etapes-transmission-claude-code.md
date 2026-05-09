# backend-worker — étapes à suivre et éléments à transmettre à Claude Code

## Objectif

Ce document donne la marche à suivre **étape par étape**: quoi faire, quoi ouvrir, quoi copier-coller, quoi transmettre, quoi vérifier, et quand passer à l'étape suivante.

La priorité actuelle est claire: **exécuter les 3 tâches déjà listées dans le fichier créé dans le vrai repo `backend-worker`**:

1. Redis / Upstash,
2. CI / vérifications automatisées,
3. SEC-001 phase 2.

---

## Étape 0 — Préparer le contexte

### Ce que tu fais

Ouvre Claude Code directement dans le vrai dépôt applicatif:

```bash
cd /Users/alexandrebaratta/backend-worker
```

### Ce que tu transmets

Dis simplement à Claude Code:

```text
Tu es dans le repo backend-worker. Avant de modifier quoi que ce soit, lis le fichier reports/backend-worker-a-donner-a-claude-code-maintenant.md et confirme-moi que tu as compris les 3 tâches prioritaires.
```

### Ce que tu dois recevoir

Claude Code doit répondre avec un résumé court des 3 tâches:

- Redis / Upstash,
- CI,
- SEC-001 phase 2.

S'il propose UX, swimlanes, import client, pricing ou refonte globale, tu refuses et tu le recentres.

---

## Étape 1 — Demander le mini-plan avant code

### Ce que tu transmets

Copie-colle:

```text
Avant de modifier le code, donne-moi un mini-plan en 5 à 10 lignes:

1. fichiers que tu vas inspecter,
2. hypothèses sur Redis / pending actions,
3. hypothèses sur CI,
4. hypothèses sur SEC-001 phase 2,
5. risques principaux,
6. ordre exact des changements,
7. tests que tu vas lancer.

Ne modifie aucun fichier tant que je n'ai pas validé ce mini-plan.
```

### Ce que tu dois vérifier

Le mini-plan doit rester limité à:

- Redis / Upstash,
- CI,
- SEC-001 phase 2.

Il ne doit pas ouvrir de chantier produit ou UX.

---

## Étape 2 — Autoriser uniquement la tâche 1: Redis / Upstash

### Ce que tu transmets

Après validation du mini-plan, copie-colle:

```text
OK pour commencer uniquement par la tâche 1: Redis / Upstash.

Objectif:
- vérifier comment les pending actions sont stockées,
- configurer ou préparer l'intégration Upstash Redis,
- garantir TTL + single-use,
- limiter le fallback mémoire au dev si nécessaire,
- documenter les variables Render / prod à ajouter,
- ajouter ou mettre à jour les tests si possible.

Ne commence pas encore la CI ni SEC-001 phase 2.

À la fin de cette tâche, donne-moi:
- fichiers modifiés,
- variables d'environnement nécessaires,
- commandes exécutées,
- résultat des tests,
- preuve ou procédure de smoke test pending action,
- rollback.
```

### Ce que tu dois recevoir

Claude Code doit fournir:

- les fichiers modifiés,
- les variables Upstash nécessaires,
- une preuve TTL / single-use ou une procédure de test,
- les commandes exécutées,
- le rollback.

### Décision

Si Redis / Upstash est OK, tu passes à l'étape 3.

Sinon, tu demandes une correction minimale avant de continuer.

---

## Étape 3 — Autoriser uniquement la tâche 2: CI / vérifications automatisées

### Ce que tu transmets

```text
OK pour la tâche 2 uniquement: CI / vérifications automatisées.

Objectif:
- ajouter ou corriger le workflow CI,
- lancer npm run typecheck,
- lancer npm test,
- lancer npm run lint si disponible,
- faire échouer la CI si typecheck ou tests échouent,
- documenter lint comme absent si le script n'existe pas.

Ne commence pas SEC-001 phase 2 tant que cette tâche n'est pas validée.

À la fin, donne-moi:
- fichier CI modifié ou créé,
- commandes exécutées,
- résultat exact,
- ce qui bloque une PR,
- rollback.
```

### Ce que tu dois recevoir

Claude Code doit fournir:

- le fichier CI,
- les commandes et résultats,
- la preuve que typecheck/tests sont bloquants,
- le statut lint,
- le rollback.

### Décision

Si CI OK, tu passes à l'étape 4.

Sinon, tu restes sur CI.

---

## Étape 4 — Autoriser uniquement la tâche 3: SEC-001 phase 2

### Ce que tu transmets

```text
OK pour la tâche 3 uniquement: SEC-001 phase 2.

Objectif:
- terminer le durcissement auth,
- supprimer toute dépendance à x-user-role, x-user-id, x-organization-id comme source de vérité,
- dériver user / org / rôle depuis identité serveur fiable ou DB membership,
- ajouter ou compléter tests 401 / 403 / header forgery,
- documenter les risques restants.

Ne fais pas de refonte UX, pas de swimlanes, pas d'import client, pas de pricing.

À la fin, donne-moi:
- fichiers modifiés,
- tests ajoutés ou modifiés,
- commandes exécutées,
- preuve JWT absent/invalide => 401,
- preuve user hors org => 403,
- preuve header forgery refusé,
- risques restants,
- rollback,
- verdict GO / NO-GO pour passer au Sprint 2.
```

### Ce que tu dois recevoir

Claude Code doit fournir:

- preuves 401 / 403 / header forgery,
- tests passants,
- risques restants,
- rollback,
- verdict GO / NO-GO.

---

## Étape 5 — Vérification finale avant Sprint 2

### Ce que tu demandes

```text
Fais maintenant le récapitulatif final des 3 tâches:

1. Redis / Upstash: statut, preuves, risques restants.
2. CI: statut, preuves, risques restants.
3. SEC-001 phase 2: statut, preuves, risques restants.

Puis exécute ou confirme les commandes:
- npm run typecheck
- npm test
- npm run lint si disponible

Termine par un verdict clair: GO ou NO-GO pour Sprint 2.
```

### Conditions pour dire GO Sprint 2

Tu peux passer au Sprint 2 uniquement si:

- Redis / Upstash est configuré ou le blocage est clairement documenté,
- CI existe et bloque typecheck/tests,
- SEC-001 phase 2 est terminé ou les risques restants sont acceptés,
- `npm run typecheck` OK,
- `npm test` OK,
- `npm run lint` OK ou absent documenté,
- rollback disponible.

---

## Résumé ultra-court à transmettre

Si tu veux aller très vite, tu peux juste donner ceci à Claude Code:

```text
Lis reports/backend-worker-a-donner-a-claude-code-maintenant.md.

Travaille étape par étape, sans refonte globale:
1. Redis / Upstash uniquement.
2. CI uniquement.
3. SEC-001 phase 2 uniquement.

Avant chaque étape: donne un mini-plan.
Après chaque étape: donne fichiers modifiés, commandes exécutées, résultats, preuves et rollback.

Ne touche pas à l'UX, swimlanes, import client, pricing ou refonte assistant.

Checks obligatoires:
- npm run typecheck
- npm test
- npm run lint si disponible.

À la fin: verdict GO / NO-GO pour Sprint 2.
```

# backend-worker — réalité GitHub / prochaine action Claude Code

## Constat corrigé

Le précédent commit local `12ac4dc` et la PR annoncée depuis cette session ne sont **pas** la source de vérité opérationnelle: la PR est introuvable sur GitHub et le commit `12ac4dc` n'est pas sur `origin/main`.

La cause probable est une exécution dans un worktree temporaire nettoyé ensuite.

## Ce qui existe vraiment maintenant

La source opérationnelle à utiliser est le dépôt réel `backend-worker`.

État confirmé par Alexandre:

- 19 fichiers `reports/` existent réellement dans le dépôt local `backend-worker`,
- l'index a été remis à jour avec ces 19 fichiers réels,
- le tout a été commit et pushé,
- commit de référence: `e86a9b6`,
- le handoff Sprint 2 est sur GitHub,
- le fichier à ouvrir pour Claude Code est:
  `reports/backend-worker-a-donner-a-claude-code-maintenant.md`.

## Nouvelle règle pour éviter la confusion

Ne plus se baser sur les PRs/commits annoncés par cette session locale si GitHub ne les montre pas.

Pour l'exécution réelle:

1. ouvrir le dépôt `backend-worker`,
2. se placer sur la branche contenant `e86a9b6` ou `origin/main` à jour,
3. ouvrir `reports/backend-worker-a-donner-a-claude-code-maintenant.md`,
4. suivre ce fichier comme handoff principal,
5. ne pas recréer un nouveau plan dans un worktree temporaire.

## Ce qu'il faut donner à Claude Code maintenant

Dans Claude Code, ouvrir le repo réel puis transmettre:

```text
Lis `reports/backend-worker-a-donner-a-claude-code-maintenant.md` dans ce repo.

Considère ce fichier comme le handoff principal actuellement pushé sur GitHub.

Exécute les tâches qui y sont listées, dans l'ordre, sans repartir d'anciens documents locaux ni d'une PR introuvable.

Avant de modifier le code:
- résume les tâches détectées,
- confirme la branche et le commit courant,
- confirme que tu vois bien l'index des 19 fichiers reports,
- propose un plan court.

Après chaque tâche:
- donne les fichiers modifiés,
- commandes exécutées,
- résultats,
- risques restants,
- rollback.

Ne touche pas aux sujets hors périmètre sans validation explicite.
```

## Vérification minimum avant de continuer

Claude Code doit confirmer:

- branche courante,
- commit courant ou base GitHub,
- présence de `reports/backend-worker-a-donner-a-claude-code-maintenant.md`,
- présence de l'index remis à jour,
- tâches à exécuter selon ce fichier.

Sans cette confirmation, ne pas lancer de modifications.

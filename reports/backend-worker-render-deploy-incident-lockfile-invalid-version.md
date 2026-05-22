# Incident Render — `npm error Invalid Version:` (lockfile)

## Incident

Le déploiement Render échouait pendant `npm install` avec:

- `npm error Invalid Version:`

## Cause racine

- Sur Render (npm v10), le `package-lock.json` contenait des entrées optionnelles Windows esbuild sans champ `version`.
- npm v10 validait strictement ces entrées et cassait l'installation sur Linux.

## Correctif appliqué

- Suppression des entrées stub concernées dans `package-lock.json`.
- Changement lockfile minimal: 8 lignes supprimées.
- Commit/push du fix: `ed39686`.

## Résultat

- Build Render relancé sur `ed39686`.
- Déploiement réussi, service live.

## Prévention

1. Épingler une version npm cohérente entre local/CI/Render.
2. Ajouter un check CI `npm ci` sur environnement Linux.
3. Rejeter les lockfiles contenant des entrées package sans `version`.

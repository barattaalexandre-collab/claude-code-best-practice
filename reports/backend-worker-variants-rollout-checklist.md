# Vérification rollout multi-versions (App Pro / Demo)

## Réponse courte

Dans cet environnement, **je ne peux pas confirmer** que les 5 variantes (N. Marti SA, Garage, Bâti, Ing, Archi) ont reçu les modifs.

Pourquoi:
- le repo disponible ici contient des documents de pilotage/audit,
- il ne contient pas les 5 codebases applicatives ni leur historique de déploiement.

## Variantes à vérifier

1. App Pro N. Marti SA
2. App Pro Demo Garage
3. App Pro Demo Bâti
4. App Pro Demo Ing
5. App Demo Archi

## Ce qu'il faut vérifier pour chacune

- Les commits SEC-001..SEC-007 sont bien présents sur la branche déployée.
- Les migrations DB 002/003 sont appliquées sur la bonne base.
- Les variables Render incluent:
  - `SUPABASE_ANON_KEY`
  - `UPSTASH_REDIS_REST_URL`
  - `UPSTASH_REDIS_REST_TOKEN`
- Les smoke tests post-déploiement passent.

## Procédure rapide (à faire par variante)

1. Identifier repo + branche + URL Render de la variante.
2. Vérifier SHA déployé = SHA incluant SEC-001..SEC-007.
3. Vérifier env vars Render.
4. Exécuter smoke tests.
5. Marquer statut: `OK` / `Partiel` / `KO`.

## Tableau de suivi (à remplir)

| Variante | Repo/Branche | SHA déployé | Migrations 002/003 | Env Redis | Smoke tests | Statut |
|---|---|---|---|---|---|---|
| N. Marti SA |  |  |  |  |  |  |
| Demo Garage |  |  |  |  |  |  |
| Demo Bâti |  |  |  |  |  |  |
| Demo Ing |  |  |  |  |  |  |
| Demo Archi |  |  |  |  |  |  |

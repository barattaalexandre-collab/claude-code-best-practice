# Retour test web app N. Marti — 2026-05-08

## Statut

**Retour terrain / incident produit à traiter en priorité.**

Ce document ne remplace pas les décisions officielles V1. Il capture le retour d'Alexandre après test réel de la web app N. Marti.

## Constats remontés

1. Alexandre ne peut pas entrer dans l'application avec un vrai accès plateforme/admin.
2. L'application affiche encore un sélecteur de rôle de type **mock** dans l'interface.
3. Alexandre doit entrer via des comptes / profils Nicolas Marti au lieu d'avoir son accès `platform_admin`.
4. Alexandre ne peut pas observer en direct tous les mouvements, flux, écritures et actions de l'application.
5. La voix/transcription comprend bien ce qui est dit.
6. Le problème principal est après transcription: les informations ne remontent pas correctement dans les bons objets métier.
7. L'IA ne distingue pas correctement plusieurs chantiers pour une même personne / même client lorsqu'il y a plusieurs lieux.
8. L'IA associe trop vite une nouvelle information au chantier existant au lieu de clarifier ou créer/rattacher au bon chantier.

## Analyse produit immédiate

Le problème n'est pas seulement la voix.

La chaîne critique est:

1. voix captée correctement,
2. transcription correcte,
3. compréhension métier partielle,
4. résolution d'entité insuffisante,
5. rattachement chantier/projet incorrect,
6. écriture ou affichage UI non fiable.

Donc le chantier prioritaire est **voice-to-action + entity resolution + observabilité admin**.

## P0 — À clarifier / corriger avant de considérer le flux comme fiable

### P0.1 Accès `platform_admin`

Créer un vrai accès plateforme pour Alexandre:

- connexion séparée des comptes client,
- rôle `platform_admin`,
- accès transversal aux tenants / variantes,
- capacité d'observer sans polluer les données client,
- possibilité d'ouvrir la vue N. Marti comme support/admin.

### P0.2 Remplacer le sélecteur de rôle mock

Le menu visible "Changer de rôle (mock)" ne doit pas être présent comme mécanisme de droits réel.

Actions attendues:

- distinguer mode dev/demo et mode prod,
- masquer ou désactiver le mock role switch en production réelle,
- afficher le rôle réel issu de l'auth serveur,
- journaliser tout changement d'impersonation/support.

### P0.3 Console admin live / observabilité métier

Ajouter une vue `platform_admin` permettant de voir en direct:

- transcript reçu,
- intention IA détectée,
- entité résolue,
- chantier/projet choisi,
- action proposée,
- confirmation utilisateur,
- mutation DB,
- succès/erreur,
- audit log.

Objectif: comprendre immédiatement où le flux casse.

### P0.4 Résolution d'entités chantier / client / lieu

Règle métier à ajouter:

- un même client peut avoir plusieurs chantiers,
- un même contact peut être lié à plusieurs lieux,
- un nouveau lieu ne doit pas être fusionné automatiquement avec un chantier existant,
- si l'IA hésite entre plusieurs chantiers, elle doit demander clarification.

Exemple attendu:

> "Nouveau chantier Müller à Lausanne" ne doit pas être automatiquement rattaché au chantier Müller existant à un autre endroit.

## Règle de clarification proposée

Si plusieurs chantiers candidats existent pour un même client/contact:

1. comparer adresse / lieu / nom chantier / date / contexte récent,
2. si confiance faible ou conflit: demander confirmation,
3. proposer: "Je vois déjà un chantier Müller à X. Est-ce un nouveau chantier à Y ou le même ?",
4. ne pas écrire en DB tant que l'utilisateur n'a pas clarifié.

## Tests à créer

| Test | Attendu |
|---|---|
| Deux chantiers même client, lieux différents | L'IA demande clarification ou crée le bon chantier |
| Même contact, nouveau lieu | Pas de fusion automatique |
| Transcript avec lieu ambigu | Clarification obligatoire |
| Mutation IA | Visible dans console admin live |
| Échec DB | Pas de faux succès UI |
| Rôle `platform_admin` | Accès support sans compte client |
| Mock role switch en prod | Absent ou explicitement dev-only |

## Questions à trancher avec Alexandre

1. Le `platform_admin` peut-il modifier les données client ou seulement observer par défaut ?
2. Veut-on une fonction d'**impersonation** client, ou une vue support read-only + actions encadrées ?
3. La console admin live doit-elle être dans l'app principale ou dans une route séparée ?
4. Pour la démo, faut-il masquer totalement le mock role switch ?
5. Quelle règle exacte pour créer un nouveau chantier si le client existe déjà ?

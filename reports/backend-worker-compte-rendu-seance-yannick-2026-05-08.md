# Compte-rendu séance Yannick — 2026-05-08

## Statut

**Retour stratégique / produit / vente à traiter comme input prioritaire.**

Ce document capture les points remontés lors de la séance avec Yannick. Il ne remplace pas `backend-worker-cadrage-officiel-v1.md`, mais il met en évidence des problèmes, manques et opportunités à intégrer au pilotage produit et commercial.

## Synthèse exécutive

La séance montre que l'application a un fort potentiel, mais que plusieurs points doivent être corrigés ou cadrés avant de multiplier les démonstrations:

1. Le discours de vente doit démarrer par les problèmes réels du client, pas par une visite exhaustive de l'application.
2. La page / présentation des rôles doit être revue pour éviter la confusion entre personnes réelles et rôles métier.
3. La sécurité d'accès doit être mieux expliquée et préparée: MFA, session timeout, droits par rôle.
4. Le flux voix fonctionne bien côté transcription, mais la résolution métier échoue encore sur les cas multi-chantiers / même client.
5. L'accès `platform_admin` et l'observabilité live sont indispensables pour diagnostiquer les flux IA.
6. Les swimlanes / React Flow peuvent fortement améliorer la compréhension métier et la discussion client.
7. L'UX de l'assistant doit être simplifiée: micro/photo/note en premier, historique replié, moins de bruit visuel.
8. Le modèle économique doit clarifier les coûts API/LLM et la responsabilité de consommation.
9. La migration/import des données client est un point commercial incontournable.
10. La vente doit être pensée comme une coproduction / audit de flux avec N. Marti, pas comme un produit figé à imposer.

---

## 1. Présentation des rôles: problème de wording et de perception

### Problème relevé

La page semble demander "qui êtes-vous ?" alors que l'intention est de montrer les rôles et droits.

Yannick alerte sur le risque de confusion si la démo affiche des noms de personnes réelles ou fictives: les participants peuvent se demander pourquoi certains noms apparaissent et pas d'autres.

### Recommandation

Remplacer la logique "personnes" par une **carte des rôles**:

- Propriétaire / CEO
- Administrateur organisation
- Manager / chef de projet
- Terrain / technicien
- Finance / comptabilité
- Viewer / externe
- Platform admin / support

### Action produit

Créer une vue "Rôles & droits" sous forme de brainmap / swimlane / cards, où l'on clique sur un rôle pour voir:

- ce qu'il voit,
- ce qu'il peut modifier,
- ce qu'il ne peut pas faire,
- les validations nécessaires.

---

## 2. Sécurité d'accès: MFA, session timeout, droits réels

### Problèmes relevés

- Le PIN seul est jugé insuffisant pour une application contenant des données sensibles.
- Besoin de MFA ou secret link email.
- Besoin de durée de session / auto-déconnexion.
- Le rôle affiché doit être cohérent avec l'auth réelle, pas un mock.

### Options mentionnées

- Secret link par email valable environ 10 minutes.
- MFA email plutôt que SMS pour éviter coût Twilio.
- Configuration MFA dans settings.

### Actions à cadrer

1. Définir le standard d'auth V1 demo.
2. Définir le standard d'auth V2 production.
3. Ajouter session timeout.
4. Supprimer ou encadrer tout rôle mock en prod.

---

## 3. Ordre de démonstration: éviter l'effet "usine à gaz"

### Problème relevé

Montrer tous les menus et toutes les fonctionnalités peut perdre le prospect.

Yannick recommande de ne pas commencer par les détails techniques ou les projets, mais par ce qui parle au gérant:

- dashboard,
- analytics,
- vision d'ensemble,
- flux métier,
- points de blocage,
- gains de temps.

### Recommandation de scénario

1. Discussion ouverte: "qu'est-ce qui vous ralentit aujourd'hui ?"
2. Dashboard / analytics: montrer une vision qu'il n'a pas aujourd'hui.
3. Flux métier: valider avec lui comment son entreprise fonctionne.
4. Assistant voix: montrer l'USP seulement après avoir créé le besoin.
5. Test réel encadré sur un cas connu qui fonctionne.

### À éviter

- Faire une visite exhaustive de tous les menus.
- Montrer trop tôt des sessions/historiques qui polluent l'esprit.
- Lancer un cas IA risqué non répété en direct.

---

## 4. Migration / transition depuis l'existant

### Objection client anticipée

Le client risque de dire:

> "Je vais devoir continuer mon système actuel et en plus remplir votre app."

### Réponse attendue

Il faut prévoir une stratégie de transition:

- import de données existantes,
- reprise des chantiers en cours,
- catalogues produits,
- contacts,
- clients,
- documents.

### Problème actuel

Il n'existe pas encore de vraie fonctionnalité d'import industrialisée.

### Action recommandée

Créer un module ou au moins un processus V1:

- collecte fichiers client,
- mapping champs,
- import Supabase,
- validation avec client,
- contrôle qualité.

---

## 5. Swimlanes / React Flow pour visualiser les flux

### Pourquoi c'est important

Les swimlanes montrent que l'on comprend le processus métier réel:

- d'où vient l'information,
- qui intervient,
- où elle va,
- quels statuts existent,
- quelles validations bloquent,
- quelles étapes sont automatisables.

### Recommandation

Ajouter des vues React Flow / swimlane dans les flux métier, notamment:

- devis,
- chantier,
- facturation,
- réserve,
- commande fournisseur,
- visite terrain,
- assistant IA.

### Effet vente attendu

Permettre au client de dire:

> "Chez nous, ce n'est pas exactement comme ça. Il faut ajouter cette étape."

Cela transforme la démo en atelier de coproduction.

---

## 6. UX assistant IA: simplifier fortement

### Problème relevé

L'assistant IA semble trop chargé: sessions, dictées, résumés, historique visible trop tôt.

### Recommandation

Mettre en avant une interface très simple:

- gros bouton micro,
- bouton photo,
- bouton note,
- historique dans un onglet replié.

Le message à transmettre:

> "Vous parlez, l'app structure et propose."

### Action UI

- Remonter l'assistant dans le menu: c'est le cœur de l'app.
- Revoir le nom "Assistant IA" pour un nom plus commercial / humain / métier.
- Replier les menus latéraux par défaut pendant la démo.

---

## 7. Problème critique: multi-chantiers même client

### Problème observé

Cas testé:

> "Nouveau chantier chez Bernard Müller à Colombier..."

L'IA comprend la voix, mais rattache à un chantier existant / Résidence du Lac au lieu de distinguer nouveau chantier / nouveau lieu.

### Diagnostic

Le problème n'est pas la transcription. Le problème est:

- entity resolution,
- logique multi-chantiers,
- distinction client/contact/projet/lieu,
- clarification insuffisante.

### Règle attendue

Si un même client/contact a plusieurs chantiers ou qu'un nouveau lieu est mentionné:

1. ne pas fusionner automatiquement,
2. comparer lieu/adresse/contexte,
3. demander clarification si doute,
4. proposer explicitement:
   - "Créer un nouveau chantier ?"
   - "Rattacher au chantier existant ?"

### Priorité

**P0 produit** pour rendre le voice-to-action fiable.

---

## 8. Accès platform_admin / mode admin live

### Problème relevé

Alexandre ne peut pas entrer avec un vrai compte `platform_admin` et observer les flux en direct.

### Besoin

Créer une vue support/admin permettant de voir:

- transcript reçu,
- intention détectée,
- entité choisie,
- projet/chantier candidat,
- action proposée,
- confirmation,
- mutation DB,
- erreurs,
- audit trail.

### Recommandation

- Ajouter un accès `platform_admin` réel.
- Ajouter un mode support read-only par défaut.
- Encadrer toute impersonation.
- Journaliser toutes les actions support.

---

## 9. Modèle économique et coûts API/LLM

### Red flag Yannick

Si Les Précurseurs Lab paie tous les coûts LLM/API dans son propre compte, le risque de marge est important.

Services concernés:

- OpenAI,
- Deepgram,
- Supabase,
- Render,
- Vercel,
- Resend,
- Redis,
- autres APIs futures.

### Options commerciales

1. Prix forfaitaire avec quotas stricts.
2. Client apporte ses clés LLM / API.
3. Modèle hybride: forfait inclus + dépassement facturé.
4. Licence app séparée des coûts de consommation.

### À clarifier

- Qui paie OpenAI ?
- Qui paie Deepgram ?
- Quotas par licence ?
- Que se passe-t-il si le quota est dépassé ?
- Comment éviter un blocage client en plein usage ?

---

## 10. Positionnement vente: audit / coproduction / bras droit

### Point stratégique

Yannick recommande de ne pas vendre uniquement l'app.

Il faut potentiellement vendre:

- diagnostic des flux,
- optimisation organisationnelle,
- accompagnement transition,
- paramétrage métier,
- puis app comme outil d'exécution.

### Angle possible

> "J'ai observé vos contraintes terrain et back-office. J'aimerais vous montrer un prototype, mais surtout comprendre avec vous où sont les vrais points de friction pour l'adapter à votre manière de travailler."

### Bénéfice

Si l'app n'est pas parfaitement alignée au départ, cela devient une opportunité d'audit / adaptation, pas un échec.

---

## 11. Appel / prise de rendez-vous avec Nicolas Marti

### Recommandation

Ne pas appeler en laissant penser que c'est pour un chantier personnel.

Créer un teaser:

> "Votre intervention chez moi m'a fait réfléchir à vos challenges de gestion et de suivi. J'ai construit un prototype qui pourrait vous faire gagner du temps. J'aimerais vous le montrer 30 minutes et avoir votre avis métier."

### Objectif de l'appel

Obtenir:

- date,
- heure,
- 30 à 45 minutes,
- bon état d'esprit.

---

## 12. Priorités P0/P1/P2 issues de la séance

### P0 — Avant prochaine démo sérieuse

1. Corriger multi-chantiers même client / lieux différents.
2. Créer accès `platform_admin` réel.
3. Supprimer/encadrer le role switch mock en prod.
4. Préparer scénario démo en 3 actes: problème → dashboard/flux → voix.
5. Simplifier l'écran assistant: micro/photo/note, historique replié.

### P1 — Très important

1. Swimlanes React Flow dans flux métier.
2. Module/process import de données client.
3. Console admin live d'observabilité IA.
4. Script d'appel / rendez-vous Nicolas Marti.
5. Clarification modèle coûts API/LLM.

### P2 — Ensuite

1. Enregistreur réunion intégré.
2. Intégrations avec autres apps client.
3. Automatisation migration catalogues / produits.
4. Packaging commercial final.

## Questions à trancher avec Alexandre

1. Est-ce que la prochaine démo doit être positionnée comme prototype co-construit plutôt que produit fini ?
2. Quel scénario exact montrer à Nicolas Marti pour éviter un cas IA fragile ?
3. Quel nom donner à l'assistant IA ?
4. Est-ce qu'on masque tous les menus non essentiels pendant la démo ?
5. Quel modèle de coûts API est retenu pour le POC ?
6. Est-ce que l'import initial de données est inclus gratuitement dans le pilote ?

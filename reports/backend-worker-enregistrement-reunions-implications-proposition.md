# Proposition — enregistrement et retranscription des réunions / discussions de chantier

## Statut

**Proposition d'analyse — à valider par Alexandre.**

Ce document ne crée pas une décision officielle produit. Il sert à comprendre les implications avant de décider si la fonction doit être ajoutée.

## Fonction envisagée

Permettre à un utilisateur d'enregistrer une réunion, une visite ou une discussion de chantier, puis de produire automatiquement:

- une transcription,
- un résumé,
- des décisions,
- des tâches,
- des réserves / points bloquants,
- des documents rattachés au projet,
- éventuellement un compte-rendu validable.

## Implications principales

### 1. Consentement et information préalable

L'enregistrement d'une conversation implique des données personnelles et peut aussi relever du droit pénal selon le contexte.

Pour une app utilisée en Suisse / Europe, le principe prudent est:

- annoncer clairement l'enregistrement avant de démarrer,
- obtenir le consentement des participants,
- afficher le but de l'enregistrement,
- indiquer qui pourra accéder à l'audio et à la transcription,
- permettre d'arrêter l'enregistrement.

### 2. Produit / UX

Il faut éviter un simple bouton caché "record".

UX recommandée:

1. Bouton: "Démarrer l'enregistrement".
2. Écran de consentement / information.
3. État visible: "Enregistrement en cours".
4. Bouton: "Arrêter".
5. Génération transcription + résumé.
6. Étape de validation utilisateur avant création de tâches / décisions.

### 3. IA et actions

La transcription ne doit pas automatiquement créer ou modifier des objets sensibles sans validation.

Règle recommandée:

- transcription = automatique,
- résumé = automatique,
- suggestions de tâches / décisions = automatiques,
- écriture réelle en DB = seulement après validation.

### 4. Données et stockage

Décision à prendre:

- stocker l'audio complet ou seulement la transcription ?
- durée de rétention ?
- qui peut supprimer/restaurer ?
- rattachement à quel projet / chantier ?
- accès par quels rôles ?

Recommandation V1:

- garder l'audio temporairement,
- garder la transcription validée,
- permettre suppression/archivage selon droits officiels,
- journaliser accès, suppression, restauration.

### 5. Sécurité / droits

La fonction doit respecter les droits officiels V1:

- `field_user`: peut enregistrer ses propres visites/réunions terrain si autorisé.
- `manager`: peut enregistrer/rattacher au projet de son périmètre.
- `owner` / `org_admin`: accès organisation selon politique.
- `platform_admin`: support/urgence, accès encadré.
- `viewer`: lecture seulement si explicitement autorisé.

### 6. Risques

| Risque | Impact | Mitigation |
|---|---|---|
| Enregistrement sans consentement | juridique / confiance | consentement explicite avant start |
| Fuite audio/transcription | confidentialité | RBAC + org isolation + logs |
| Faux résumé IA | mauvaise décision métier | validation humaine avant action |
| Données sensibles captées | RGPD/LPD/projet client | minimisation + rétention limitée |
| Transcript imparfait | tâches erronées | clarification + confirmation |

## Option A/B/C

### Option A — Transcription simple sans stockage audio durable

- Audio utilisé pour transcription puis supprimé rapidement.
- Transcription + résumé stockés après validation.
- Moins risqué pour V1.

### Option B — Audio + transcription stockés

- Plus complet, utile en litige ou compte-rendu.
- Plus sensible légalement et en sécurité.
- Besoin de politique de rétention claire.

### Option C — Compte-rendu assisté sans enregistrement permanent

- L'utilisateur dicte ou résume après réunion.
- Moins risqué, mais moins puissant.

## Recommandation V1

Commencer par **Option A**:

- consentement explicite,
- audio temporaire,
- transcription + résumé,
- validation humaine avant actions,
- rattachement chantier/projet,
- audit trail.

## Questions à valider par Alexandre

1. Veut-on enregistrer l'audio complet ou seulement générer une transcription ?
2. Combien de temps conserver l'audio si on le garde ?
3. Est-ce que `field_user` peut enregistrer seul une discussion de chantier ?
4. Faut-il une bannière/phrase de consentement standard en FR/IT ?
5. Qui peut consulter les transcriptions ?
6. Est-ce que les transcriptions peuvent alimenter la mémoire apprenante ? Si oui, uniquement en mode strictement traçable.

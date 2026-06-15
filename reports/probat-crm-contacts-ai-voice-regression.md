# ProBAT — Régression CRM Contacts voix et assistant

Date de capture : 2026-06-02
Source : retour utilisateur terrain sur écran Contacts
Statut : P0 produit — à corriger avant démo libre sur CRM Contacts

## Résumé exécutif

Sur l'écran Contacts, l'utilisateur ne peut pas utiliser la voix pour modifier un contact, car l'option vocale n'est pas disponible dans le flux de modification. En compensation, il utilise l'assistant IA, mais celui-ci entre dans une boucle de clarification confuse : il identifie parfois une action de modification avec une valeur vide, perd le contexte après confirmation, redemande le contact ou le projet, et ne sait pas rechercher seul le contact demandé. Le résultat est contraire à l'objectif ProBAT : l'assistant complique l'action au lieu de la simplifier.

## Constat utilisateur

Écran concerné : CRM Contacts.

Conversation observée :

```text
Contexte : CRM

Utilisateur : tu fais caca?
Assistant : Je n'ai pas identifié d'action claire. Pouvez-vous préciser ?

Utilisateur : modifier le contact robin bellenot
Assistant : Je n'ai pas compris ce que vous souhaitez modifier. Pouvez-vous préciser l'entité (contact, entreprise, projet ou tâche) et le champ à changer ?

Utilisateur : modifier le nom du contact Robin Bellenot
Assistant : J'ai analysé votre message et identifié 1 action(s) : Modifier contact : "Robin Bellenot" — nom complet → "". Confirmez-vous l'exécution de ces actions ?

Utilisateur : oui il faut remplacer par Alexandre Baratta
Assistant : Quel contact souhaitez-vous renommer en Alexandre Baratta ?

Utilisateur : Robin Bellenot
Assistant : Pouvez-vous préciser le projet ou le chantier auquel Robin Bellenot est associé ?

Utilisateur : a toi de chercher
Assistant : Pouvez-vous préciser le projet ou le client auquel vous faites référence ?

Utilisateur : j'aimerais changer le no de téléphone de François Braghini
Assistant : Modifier contact : "François Braghini" — téléphone direct → "". Confirmez-vous l'exécution de ces actions ?

Utilisateur : oui
Assistant : Pouvez-vous préciser le projet ou le chantier auquel vous faites référence ?
```

## Problèmes identifiés

### P0-A — Voix absente dans Contacts

L'écran Contacts ne propose pas de voie directe pour modifier un contact à la voix. L'utilisateur devrait pouvoir dicter une modification depuis l'écran courant, par exemple :

- `Change le nom de Robin Bellenot en Alexandre Baratta` ;
- `Remplace le téléphone de François Braghini par 079 123 45 67` ;
- `Ajoute le mobile 078 555 12 12 à Sophie Martin`.

### P0-B — Assistant CRM perd le contexte multi-tour

L'assistant identifie une modification, demande confirmation, puis oublie l'objet ou le champ au message suivant. Le `pendingActionToken` / `clarificationToken` n'est pas suffisamment exploité dans le FAB pour continuer la même action.

### P0-C — Valeur cible vide acceptée dans la proposition d'action

L'assistant propose : `nom complet → ""` ou `téléphone direct → ""`. Une modification de contact avec valeur cible vide ne doit jamais être proposée comme action confirmable, sauf si l'utilisateur demande explicitement d'effacer le champ.

### P0-D — Recherche contact insuffisante

Quand l'utilisateur donne un nom exact (`Robin Bellenot`, `François Braghini`), l'assistant devrait chercher dans les contacts CRM au lieu de demander un projet ou un chantier. L'association projet/chantier ne doit être demandée que si plusieurs contacts homonymes existent ou si l'action l'exige réellement.

### P0-E — Réponse aux messages hors sujet trop robotique

Pour un message hors sujet ou vulgaire, l'assistant devrait recadrer brièvement et proposer une action utile dans le contexte CRM, par exemple : `Je peux vous aider à créer, modifier ou rechercher un contact. Que voulez-vous changer ?`

## Comportement attendu

### Flow attendu — modifier nom

```text
Utilisateur : Change le nom de Robin Bellenot en Alexandre Baratta.
Assistant : J'ai trouvé le contact Robin Bellenot. Je vais remplacer le nom complet par Alexandre Baratta. Confirmez-vous ?
Utilisateur : Oui.
Assistant : C'est fait. Le contact s'appelle maintenant Alexandre Baratta.
```

### Flow attendu — modifier téléphone

```text
Utilisateur : Change le téléphone de François Braghini en 079 123 45 67.
Assistant : J'ai trouvé François Braghini. Je vais remplacer le téléphone par 079 123 45 67. Confirmez-vous ?
Utilisateur : Oui.
Assistant : C'est fait. Le téléphone de François Braghini a été mis à jour.
```

### Flow attendu — valeur manquante

```text
Utilisateur : Modifier le téléphone de François Braghini.
Assistant : Quel nouveau numéro souhaitez-vous enregistrer pour François Braghini ?
Utilisateur : 079 123 45 67.
Assistant : Je vais remplacer le téléphone de François Braghini par 079 123 45 67. Confirmez-vous ?
```

## Critères d'acceptation

1. Depuis CRM Contacts, une action vocale ou un micro est accessible pour dicter une modification de contact.
2. Le FAB Assistant garde le contexte de modification entre la demande initiale, la clarification et la confirmation.
3. Aucune action `update_contact` avec valeur cible vide n'est proposée comme confirmable.
4. Un nom exact de contact déclenche une recherche contacts avant toute demande de projet/chantier.
5. Les champs contact supportés au minimum sont : nom complet, téléphone, mobile, email, rôle/fonction, entreprise associée.
6. Les demandes hors sujet sont recadrées avec une aide contextuelle CRM au lieu d'une clarification générique.
7. Les tests couvrent les cas Robin Bellenot et François Braghini, plus au moins 8 phrases génériques de modification contact.

## Fichiers cibles probables

### Frontend

- `src/components/ai/AiAssistantFAB.tsx` : conservation clarification/pending token dans le Sheet.
- `src/services/aiService.ts` : transmission structurée du contexte et des tokens.
- `src/pages/crm/Contacts.tsx` ou équivalent : ajout d'un bouton micro/action IA contextualisée sur Contacts.

### Backend

- `backend-worker/src/routes/public/ai.ts` : NLU update_contact, validation valeur non vide, recherche contact par nom.
- Routes contacts si nécessaire : endpoint de recherche ou lookup contact par nom.
- Tests backend : fixtures d'intention et flows multi-tour contact.

## Prompt CC recommandé

```text
Tu es Claude Code. Objectif : corriger la régression CRM Contacts voix + assistant.

Référence : reports/probat-crm-contacts-ai-voice-regression.md

Problèmes P0 :
1. Sur CRM Contacts, l'utilisateur ne peut pas modifier un contact à la voix.
2. L'assistant perd le contexte multi-tour pendant une modification de contact.
3. Il propose des updates avec valeur cible vide, par exemple nom complet -> "" ou téléphone -> "".
4. Il demande un projet/chantier alors qu'un nom exact de contact devrait déclencher une recherche contact.

Travail demandé en PR séparées si possible :

PR 1 backend — NLU/update_contact robuste
- Fichier probable : backend-worker/src/routes/public/ai.ts.
- Ajouter/renforcer l'intent update_contact.
- Interdire toute action update_contact confirmable si la valeur cible est vide, sauf demande explicite d'effacement.
- Si un nom de contact est présent, chercher d'abord dans les contacts CRM avant de demander projet/chantier.
- Gérer les champs : nom complet, téléphone, mobile, email, rôle/fonction, entreprise.
- Ajouter tests pour :
  - Change le nom de Robin Bellenot en Alexandre Baratta.
  - Remplace le téléphone de François Braghini par 079 123 45 67.
  - Modifier le téléphone de François Braghini. -> clarification demandant le nouveau numéro.
  - Oui il faut remplacer par Alexandre Baratta. -> continue l'action précédente avec token.
  - Hors sujet/vulgaire -> recadrage CRM utile.

PR 2 frontend — FAB multi-tour + voix Contacts
- Fichiers probables : src/components/ai/AiAssistantFAB.tsx, src/services/aiService.ts, src/pages/crm/Contacts.tsx.
- Stocker et renvoyer pendingActionToken / clarificationToken dans le Sheet.
- Ajouter une option micro ou action IA vocale disponible sur CRM Contacts.
- Transmettre pageContext structuré : route, module CRM, entityType contact, selected/contact visible si applicable.
- Le flow doit permettre : demande -> clarification -> réponse utilisateur -> confirmation -> exécution, sans reset.

Critères d'acceptation :
- Depuis Contacts, je peux dire ou taper : "Change le nom de Robin Bellenot en Alexandre Baratta".
- L'assistant trouve Robin Bellenot, propose la bonne modification avec valeur non vide, demande confirmation, puis exécute.
- "Changer le téléphone de François Braghini" demande uniquement le nouveau numéro, pas le projet/chantier.
- Après "oui", l'assistant n'oublie pas l'action en cours.
- Aucun update contact avec champ -> "" n'est confirmable.
- Typecheck + tests passent.
- Smoke mobile/laptop sur /crm/contacts.

Ne fais pas de refactor large. Ne touche pas au pricing ni aux droits. Donne preuves avant/après.
```

## Verdict opérationnel

Ce retour invalide le GO pur pour une démonstration libre du module Contacts. La démo reste possible si le scénario évite les modifications de contacts par IA, mais l'expérience doit être corrigée avant de présenter l'assistant comme copilote CRM fiable.

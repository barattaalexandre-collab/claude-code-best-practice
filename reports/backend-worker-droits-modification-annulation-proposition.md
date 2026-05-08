# Proposition — droits de modification et d'annulation

## Statut

**Proposition à valider par Alexandre.**

Ce document ne remplace pas `backend-worker-cadrage-officiel-v1.md` et ne crée pas de règle officielle tant qu'Alexandre ne l'a pas validé explicitement.

## Principe directeur

Toute modification ou annulation doit respecter quatre niveaux de contrôle:

1. **Identité authentifiée**: l'utilisateur doit être connu côté serveur.
2. **Rôle**: le rôle doit autoriser l'action.
3. **Périmètre organisation**: l'objet doit appartenir à la même organisation/variante.
4. **Confirmation**: toute action sensible doit être confirmée explicitement.

## Rôles proposés

| Rôle | Description |
|---|---|
| `owner` | Pleins droits métier et administration organisation. |
| `admin` | Gestion opérationnelle large, sauf actions de propriété/paramétrage critique. |
| `manager` | Gestion projets, clients, contacts, tâches, documents métier. |
| `field_user` | Actions terrain: notes, photos, visites, tâches assignées. |
| `accountant` | Finance/facturation, lecture métier nécessaire. |
| `viewer` | Lecture seule. |

## Matrice modification / annulation proposée

| Action | owner | admin | manager | field_user | accountant | viewer | Confirmation requise |
|---|---:|---:|---:|---:|---:|---:|---|
| Créer client/contact/projet | ✅ | ✅ | ✅ | ⚠️ limité | ❌ | ❌ | Non, sauf doublon détecté |
| Modifier client/contact/projet | ✅ | ✅ | ✅ | ⚠️ champs terrain uniquement | ❌ | ❌ | Oui si champ critique |
| Annuler/supprimer client/contact/projet | ✅ | ⚠️ soft-delete | ⚠️ demande validation | ❌ | ❌ | ❌ | Oui, toujours |
| Créer note/photo/visite | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | Non |
| Modifier note/photo/visite | ✅ | ✅ | ✅ | ✅ si auteur/assigné | ❌ | ❌ | Oui si déjà validé/client-facing |
| Annuler/supprimer note/photo/visite | ✅ | ✅ | ✅ | ✅ si auteur/assigné | ❌ | ❌ | Oui |
| Créer/modifier tâche | ✅ | ✅ | ✅ | ✅ si assigné/terrain | ❌ | ❌ | Selon impact planning |
| Annuler/supprimer tâche | ✅ | ✅ | ✅ | ⚠️ si assigné | ❌ | ❌ | Oui |
| Classer document | ✅ | ✅ | ✅ | ⚠️ upload terrain | ❌ | ❌ | Oui si rattachement ambigu |
| Supprimer document | ✅ | ⚠️ soft-delete | ❌ | ❌ | ❌ | ❌ | Oui, toujours |
| Modifier facture/finance | ✅ | ⚠️ selon politique | ❌ | ❌ | ✅ | ❌ | Oui si impact montant/statut |
| Annuler facture/paiement | ✅ | ⚠️ double validation | ❌ | ❌ | ✅ selon seuil | ❌ | Oui, toujours |

Légende:
- ✅ autorisé
- ⚠️ autorisé sous condition métier
- ❌ interdit

## Règles non négociables proposées

1. Aucun droit ne doit dépendre d'un rôle envoyé librement par le client.
2. Toute action doit être filtrée par `organization_id`.
3. Aucune suppression physique directe par défaut: préférer soft-delete / statut annulé.
4. Toute annulation doit être journalisée.
5. Toute action IA qui modifie ou annule doit passer par confirmation utilisateur.
6. En cas de doute IA: demander clarification, ne pas agir.
7. L'UI ne doit jamais afficher un succès si la DB n'a pas été modifiée.

## Règle spéciale IA

L'IA ne possède aucun droit propre.
Elle agit uniquement au nom de l'utilisateur authentifié et ne peut jamais dépasser:

- son rôle,
- son organisation,
- les champs autorisés,
- les règles de confirmation.

## Questions à valider par Alexandre

1. Confirmer la liste exacte des rôles.
2. Confirmer si `admin` existe distinctement de `owner`.
3. Confirmer si `field_user` peut modifier uniquement ses propres éléments ou aussi ceux de son équipe.
4. Confirmer les seuils finance nécessitant double validation.
5. Confirmer si les annulations sont toujours des soft-delete.
6. Confirmer qui peut restaurer une action annulée.

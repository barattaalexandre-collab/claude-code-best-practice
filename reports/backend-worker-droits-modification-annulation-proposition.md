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

## Clarifications proposées après retour Alexandre

### 1. Nommer correctement "moi avec tous les droits"

Recommandation: ne pas appeler Alexandre simplement `admin`, car `admin` est ambigu.

Proposition de vocabulaire:

| Rôle | Sens recommandé |
|---|---|
| `platform_admin` ou `super_admin` | Alexandre / Les Précurseurs Lab: accès transversal plateforme, support, maintenance, urgence. |
| `owner` | Propriétaire / CEO / direction de l'entreprise cliente qui achète l'app. |
| `org_admin` | Administrateur interne de l'entreprise cliente, délégué par le owner. |
| `manager` | Chef de projet / responsable opérationnel. |
| `field_user` | Collaborateur terrain. |
| `accountant` ou `finance` | Responsable finance/facturation. |
| `viewer` | Lecture seule. |

Décision recommandée:
- Alexandre = `platform_admin` / `super_admin`.
- Le patron/propriétaire de l'entreprise cliente = `owner`.
- Éviter d'utiliser `admin` seul dans le produit final.

### 2. Droits du `field_user`

Décision proposée selon retour Alexandre:
- `field_user` peut modifier uniquement ses propres éléments.
- Exemples: ses notes, ses photos, ses visites, ses tâches assignées.
- Il ne peut pas modifier les éléments d'un collègue sauf délégation explicite.

### 3. Double validation finance

Réponse prudente: tout ce qui est sensible doit demander validation renforcée.

Proposition de règle simple:

| Action finance | Validation proposée |
|---|---|
| Modifier libellé/commentaire interne | confirmation simple |
| Modifier montant, TVA, statut facture, échéance | confirmation obligatoire |
| Annuler facture, paiement, avoir, ou écriture comptable | double validation |
| Supprimer document financier | interdit ou double validation + soft-delete |

Double validation possible:
- action demandée par `accountant` puis validée par `owner`, ou
- action demandée par `owner` puis confirmée une seconde fois explicitement.

### 4. Soft-delete expliqué simplement

Soft-delete signifie: on ne supprime pas vraiment la donnée de la base.

Au lieu de détruire la ligne définitivement, on marque l'objet comme:
- `deleted`,
- `cancelled`,
- `archived`,
- ou avec un champ `deleted_at`.

Avantages:
- on peut restaurer en cas d'erreur,
- on garde l'historique,
- on peut auditer qui a annulé quoi,
- on évite les pertes de données irréversibles.

Exemple:
- suppression dure: la facture disparaît définitivement de la DB.
- soft-delete: la facture devient "annulée/archivée", invisible dans les vues normales, mais restaurable par un rôle autorisé.

Recommandation:
- utiliser soft-delete par défaut pour tout objet métier important.
- réserver la suppression définitive à des cas exceptionnels et très encadrés.

### 5. Qui peut restaurer une action annulée ?

Proposition alignée avec le retour Alexandre:

| Type d'objet | Peut restaurer |
|---|---|
| Client/contact/projet | `platform_admin`, `owner`, éventuellement `org_admin` |
| Notes/photos/visites/tâches | `platform_admin`, `owner`, `manager` si périmètre projet |
| Documents | `platform_admin`, `owner`, `manager` selon type document |
| Finance/facturation | `platform_admin`, `owner`, `accountant/finance` |

Recommandation:
- Alexandre (`platform_admin`) peut restaurer en support/urgence.
- Le propriétaire client (`owner`) peut restaurer dans son organisation.
- La finance (`accountant/finance`) peut restaurer uniquement les objets financiers.
- Toute restauration doit être journalisée.

### 6. Matrice de rôles recommandée V1

| Rôle recommandé | À garder ? | Commentaire |
|---|---|---|
| `platform_admin` / `super_admin` | Oui | Alexandre / équipe plateforme. |
| `owner` | Oui | Propriétaire/CEO de la société cliente. |
| `org_admin` | Optionnel V1 | Utile si le owner délègue l'administration. |
| `manager` | Oui | Responsable projet/opérations. |
| `field_user` | Oui | Terrain, limité à ses propres éléments. |
| `accountant` / `finance` | Oui | Finance/facturation. |
| `viewer` | Oui | Lecture seule. |

## Décisions encore à valider explicitement

1. Choisir le nom exact: `platform_admin` ou `super_admin`.
2. Décider si `org_admin` existe dès V1 ou plus tard.
3. Valider la règle: `field_user` = uniquement ses propres éléments.
4. Valider la règle finance: double validation pour annulation/suppression/modification sensible.
5. Valider soft-delete par défaut pour objets métier importants.
6. Valider les restaurations par domaine: owner global org, finance uniquement finance, platform admin support/urgence.

# Droits de modification et d'annulation — décision officielle V1

## Statut

**Official-v1 — validé par Alexandre.**

Ce document complète `backend-worker-cadrage-officiel-v1.md` pour le périmètre des droits de modification, d'annulation et de restauration.

## Décisions validées

1. Le rôle plateforme avec tous les droits s'appelle **`platform_admin`**.
2. Le rôle **`owner`** correspond au propriétaire / CEO / direction de l'entreprise cliente.
3. Le rôle **`org_admin`** est ajouté dès la V1 comme administrateur interne délégué par le `owner`.
4. Le rôle **`field_user`** peut modifier uniquement ses propres éléments.
5. Les actions finance sensibles nécessitent une double validation.
6. Le **soft-delete est le comportement par défaut** pour les objets métier importants.
7. La restauration est autorisée par domaine selon rôle.

## Rôles officiels V1

| Rôle | Définition |
|---|---|
| `platform_admin` | Alexandre / Les Précurseurs Lab: accès transversal plateforme, support, maintenance, urgence. |
| `owner` | Propriétaire / CEO / direction de l'entreprise cliente. |
| `org_admin` | Administrateur interne de l'entreprise cliente, délégué par le `owner`. |
| `manager` | Chef de projet / responsable opérationnel. |
| `field_user` | Collaborateur terrain, limité à ses propres éléments. |
| `accountant` / `finance` | Responsable finance/facturation. |
| `viewer` | Lecture seule. |

## Règles officielles V1

### `field_user`

- Peut créer/modifier ses propres notes, photos, visites et tâches assignées.
- Ne peut pas modifier les éléments d'un collègue sans délégation explicite.
- Ne peut pas annuler/supprimer des objets structurants client/projet.

### Finance

Toute action finance sensible nécessite double validation, notamment:

- modification de montant,
- TVA,
- statut facture,
- échéance sensible,
- annulation facture,
- annulation paiement,
- création/annulation avoir,
- écriture comptable,
- suppression/annulation document financier.

### Soft-delete

Le soft-delete est le comportement par défaut pour les objets métier importants.

Cela signifie que l'objet n'est pas détruit physiquement par défaut; il est marqué comme:

- `deleted`,
- `cancelled`,
- `archived`,
- ou via un champ `deleted_at`.

Objectif:

- garder l'historique,
- permettre restauration,
- éviter perte irréversible,
- conserver audit trail.

### Restauration par domaine

| Domaine | Rôles pouvant restaurer |
|---|---|
| Client/contact/projet | `platform_admin`, `owner`, `org_admin` |
| Notes/photos/visites/tâches | `platform_admin`, `owner`, `org_admin`, `manager` si périmètre projet |
| Documents | `platform_admin`, `owner`, `org_admin`, `manager` selon type document |
| Finance/facturation | `platform_admin`, `owner`, `accountant` / `finance` |

Toute restauration doit être journalisée.

## Règle IA officielle

L'IA ne possède aucun droit propre.

Elle agit uniquement au nom de l'utilisateur authentifié et ne peut jamais dépasser:

- le rôle de l'utilisateur,
- son organisation,
- son périmètre métier,
- les champs autorisés,
- les règles de confirmation,
- les règles de double validation.

# Cadrage officiel V1 — décisions validées (Alexandre)

## A. Source de vérité & gouvernance

### Ordre de priorité (officiel)
1. **Code GitHub + migrations + configuration déployée** (vérité exécutable)
2. **Compte-rendu maître projet** (vérité fonctionnelle/produit/historique)
3. **`reports/*`** (preuves, audits, validations, contexte)

### Décision structurante
- **Décision finale: Alexandre uniquement** (après discussion).

### Format obligatoire avant tout changement majeur
- décision à prendre
- options A/B/C
- impact
- risques
- coût/temps
- recommandation
- validation explicite avant exécution

## B. Architecture multi-versions

### Modèle retenu
- **Hybride** avec **cœur applicatif unique**.
- Variantes via branding, seed data, wording, profils démo, micro-flows, variables métier/entreprise.

### Règle de propagation
- Toute amélioration du cœur bénéficie à toutes les variantes,
- sauf adaptation volontaire explicite (métier/langue/entreprise/profil).

### État technique actuel
- Pas de package shared multi-repo type workspace/lib.
- Même base de code, variantes activées par profil/seed/query param/branding.
- Exemples: `?demo=architecte`, `?demo=ingenieur`, `?demo=batiment`, prévu `?demo=garage-fr`, `?demo=garage-it`.

## C. Priorités business (30 jours)

1. Accélérer les ventes
2. Robustesse voix → action
3. Sécuriser la prod
4. Démo verticale garage

Contraintes:
- Démo critique cible: **semaine prochaine**.
- Niveau de risque accepté: **zéro compromis**.

## D. Sécurité V2 & conformité

### Priorités confirmées
- Authentification serveur forte
- Isolation multi-tenant stricte

### Gate de sécurité
- Oui, bloquant pour sujets critiques.

### Compliance / hébergement
- Cible donnée: Suisse et/ou Europe.
- Vercel: provisoire, migration possible ultérieurement.

## E. Voix / IA agentique

### Priorités robustesse
1. Taux de réussite des actions
2. Réduction des faux positifs
3. Réduction des clarifications inutiles
4. Latence

### En cas de doute IA
- Toujours demander clarification.

### Mémoire apprenante
- Niveau autorisé: **strictement traçable** (pas d'apprentissage opaque non contrôlé).

## F. Produit & UX métier

### Top 3 flux non négociables
1. Visite multimodale
2. Edit intelligence
3. Création client/contact/projet

Ensuite:
- Documents entrants
- Planning/Kanban
- Finance

### Modèle UX
- Cœur UX unique + skin + micro-flows spécifiques par verticale.

## G. Ops / Déploiement

### Upstash Redis
- Pas encore obligatoire par défaut.
- Décision: l'installer dès que nécessaire, après explication claire utilité/impact.

### CI/CD
- Oui: smoke tests bloquants post-deploy souhaités.

### Pilotage
- Oui: tableau unique de statut souhaité (incidents, sécurité, variantes, blocs, corrections, priorités).

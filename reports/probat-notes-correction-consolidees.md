# ProBAT — Notes de correction consolidées

Date de capture : 2026-05-31
Statut : backlog produit/UX à prioriser avant élargissement commercial

## Résumé exécutif

Le principal frein identifié est la qualité de la reconnaissance vocale : elle doit devenir suffisamment fiable pour un usage professionnel quotidien, sans que l'utilisateur adapte sa façon de parler. Le deuxième chantier structurant est l'omniprésence de l'assistant IA : il ne doit plus être cantonné à son menu, mais agir comme un copilote accessible depuis tous les écrans. Enfin, la navigation et l'ergonomie doivent être simplifiées au maximum pour donner une impression de produit premium, stable et immédiatement compréhensible.

## 1. Reconnaissance vocale — priorité critique

### Constat

- La reconnaissance vocale n'est pas assez performante.
- L'application ne comprend pas correctement certaines phrases.
- Des mots sont marqués comme inconnus alors qu'ils sont clairement prononcés.
- Le système invente parfois des mots ou interprète mal les phrases.

### Objectif

Atteindre un niveau de compréhension comparable aux meilleurs assistants IA du marché. L'utilisateur doit pouvoir parler naturellement, avec son accent, son vocabulaire métier et des phrases longues, sans adapter sa façon de s'exprimer.

### Attendu

- Excellente gestion des accents.
- Excellente gestion du vocabulaire métier.
- Bonne compréhension des phrases longues.
- Très faible taux d'erreur.
- Compréhension du contexte pour éviter les retranscriptions incohérentes.
- Fiabilité suffisante pour une utilisation professionnelle quotidienne.

### Priorité

**Très haute / critique.**

## 2. Assistant IA disponible partout dans l'application — priorité critique

### Constat

L'assistant IA est actuellement limité à son propre menu.

### Amélioration souhaitée

L'assistant doit être accessible depuis tous les écrans et tous les modules, par exemple avec un bouton flottant permanent ou un point d'entrée global toujours visible.

### Exemples d'actions attendues

Depuis l'écran courant, l'utilisateur doit pouvoir demander :

- une modification ;
- un ajout ;
- une correction ;
- une explication ;
- une création de contenu ;
- une action contextualisée sur le module affiché.

### Objectif

Éviter les allers-retours permanents vers le menu `Assistant IA` et transformer l'IA en véritable copilote intégré à l'application.

### Priorité

**Haute / critique produit.**

## 3. Navigation latérale à améliorer

### Constat

- Le menu latéral manque de fluidité.
- L'expérience visuelle n'est pas suffisamment stable ni professionnelle.
- Certaines transitions donnent une impression de manque de finition.

### Améliorations attendues

- Fluidifier les animations.
- Uniformiser les comportements du menu.
- Améliorer la stabilité visuelle.
- Rendre l'interface plus moderne, propre et robuste.

### Objectif

Donner une sensation de produit premium et fiable.

### Priorité

**Moyenne à haute.**

## 4. Retour arrière et navigation générale

### Constat

- Revenir à l'écran précédent n'est pas toujours intuitif.
- Certaines actions nécessitent trop de manipulations.

### Améliorations attendues

- Ajouter des retours arrière visibles et cohérents.
- Réduire le nombre de clics nécessaires.
- Uniformiser la navigation dans toute l'application.

### Principe directeur

Si un enfant de 5 ans ne comprend pas immédiatement comment revenir en arrière, l'interface doit être simplifiée.

### Priorité

**Haute.**

## 5. Simplicité d'utilisation globale

### Vision produit

Chaque fonctionnalité doit être conçue avec la question suivante :

> Une personne qui découvre l'application pour la première fois comprend-elle immédiatement quoi faire ?

### Objectifs

- Réduire la charge cognitive.
- Supprimer les étapes inutiles.
- Rendre chaque action évidente.
- Favoriser la rapidité d'exécution.

### Principes directeurs

- Simplicité maximale.
- Minimum de clics.
- Maximum de clarté.
- Aucune ambiguïté dans les actions.

## Classement des priorités

| Priorité | Sujet | Niveau |
|---|---|---|
| 🔴 Critique | Reconnaissance vocale | Très haute |
| 🔴 Critique | Assistant IA disponible partout | Haute |
| 🟠 Importante | Navigation retour arrière | Haute |
| 🟠 Importante | Ergonomie générale et simplicité | Haute |
| 🟡 À améliorer | Menu latéral et stabilité visuelle | Moyenne à haute |

## Prochain cadrage recommandé

1. Transformer ces notes en tickets produit séparés : `VOICE-001`, `AI-OMNI-001`, `NAV-001`, `BACK-001`, `UX-SIMPLE-001`.
2. Définir des critères mesurables pour la voix : taux d'erreur acceptable, phrases métier de test, accents, longueur des phrases, bruit ambiant.
3. Prototyper l'assistant IA global avec un bouton flottant et un contexte de page transmis automatiquement.
4. Lancer un audit UX mobile/desktop centré sur le nombre de clics et la compréhension immédiate des retours arrière.
5. Ne pas qualifier l'application de produit commercialement mature tant que les deux points critiques — voix fiable et IA omniprésente — ne sont pas validés par des tests terrain.

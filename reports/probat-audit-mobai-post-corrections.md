# ProBAT — Audit MobAI post-corrections CC

Date de capture : 2026-05-26T22:30Z
Bundle audité : `index-savWZjU2.js`
Méthode : Chrome MCP sur production, probes API directes, 7 modules audités.
Statut : GO sous réserve — deux P0 à corriger avant GO pur.

## Verdict global

> **GO sous réserve.**
>
> L'infrastructure voix, la navigation et la simplification UX atteignent un niveau professionnel, mais l'assistant IA omniprésent présente encore deux réserves P0 : confusion NLU entre `Créer` et `Modifier`, et premier clic intermittent sur le FAB Assistant.

## Synthèse par module

| Module | Voix | IA omniprésente | Navigation / Back | Simplicité | Verdict |
|---|---|---|---|---|---|
| Dashboard | n/a | FAB présent | home sans BackButton | KPI clairs, lignes cliquables | PASS |
| CRM Entreprises | n/a texte | FAB + contexte `CRM` | BackButton OK | A-Z + cartes entreprises | PASS |
| Projets | n/a | FAB + contexte `Projets`, bug NLU create→modify | BackButton OK | badges `À compléter` | WARN |
| Planning | n/a | FAB + contexte `Planning` | BackButton OK | vues Chantiers/Gantt/Calendrier | PASS |
| Notes terrain | bouton Dicter visible | FAB intermittent | BackButton OK | filtres tags + Nouvelle note | WARN |
| Photos | n/a | FAB intermittent | BackButton OK | fallback `Image indisponible`, description IA encore verbose | WARN |
| Devis & Factures | n/a | FAB présent globalement | BackButton OK | filtres Type/Statut + montants à compléter | PASS |

## Voix — audit infrastructure

Le test live micro n'a pas pu être simulé via MCP, mais l'infrastructure backend est validée au niveau configuration :

- Deepgram backend actif avec modèle `nova-2`.
- `numerals=true`, `endpointing=300` et `smart_format=true` actifs.
- 93 keywords métier retournés par le backend, dont vocabulaire chantier, marques et noms clients/projets réels Marti.
- Corpus de 20 phrases métier livré côté frontend avec helper `termsHitRate()`.

Une QA humaine terrain reste nécessaire pour valider le taux réel de reconnaissance sur micro, accents, bruit ambiant et phrases longues.

## P0 — Bloquants avant GO pur

### P0-A — NLU IA confond `create` et `modify`

**Symptôme observé** : depuis le FAB Assistant sur `/projects`, le message `Crée une tâche pour le projet Rochat : Appeler Müller Thomas demain à 10h` déclenche une réponse de clarification formulée comme une modification : `Je n'ai pas compris ce que vous souhaitez modifier...`.

**Impact commercial** : élevé. Une démo libre où l'utilisateur demande de créer une tâche peut immédiatement donner l'impression que l'IA ne comprend pas les actions de base.

**Cause probable** : prompt système backend ou classificateur d'intention qui privilégie l'intent `update` sur `create`, ou mauvaise gestion de l'impératif français `Crée`.

**Fichier cible probable** : `backend-worker/src/routes/public/ai.ts`, zone NLU / prompt template / intent list.

**Effort estimé** : 1 h + retest.

**Critère d'acceptation** : les formulations `Crée une tâche`, `Ajoute une note`, `Nouveau devis`, `Planifie un rendez-vous` sont classées en création et non en modification.

### P0-B — FAB Assistant : premier clic intermittent

**Symptôme observé** : sur plusieurs routes (`/projects`, `/planning`, `/field/notes`, `/field/photos`), le premier clic sur le bouton flottant Assistant ne déclenche pas toujours l'ouverture du Sheet. Le deuxième clic ouvre normalement ; deux clics rapides peuvent ouvrir puis refermer.

**Impact commercial** : moyen à élevé. La promesse `Assistant IA partout` paraît instable si l'entrée globale ne répond pas au premier tap.

**Cause probable** : race condition de focus, toggle trop sensible, double événement pointer/click, ou interaction avec `SidebarProvider` / `Outlet`.

**Fichier cible probable** : `src/components/ai/AiAssistantFAB.tsx`.

**Effort estimé** : 30 min + retest.

**Critère d'acceptation** : un tap/clic unique ouvre toujours le Sheet sur mobile et desktop ; double clic rapide ne ferme pas immédiatement le Sheet.

## P1 — Réserves importantes avant démo commerciale élargie

### P1-A — Description IA Photos trop verbose

La description `La photo montre vraisemblablement...` reste visible. Le sanitizer actuel couvre certains disclaimers, mais pas assez les formulations spéculatives (`vraisemblablement`, `pourrait`, `semble`).

**Fichier cible probable** : `src/pages/field/Photos.tsx`.

**Effort estimé** : 5 à 15 min.

### P1-B — Contexte FAB non transmis comme structure dédiée

Le contexte est concaténé dans le contenu du message, au lieu d'être transmis comme champ structuré `pageContext`. L'IA peut l'ignorer ou mal le pondérer.

**Fichier cible probable** : `src/services/aiService.ts` et backend `ai.ts` si le contrat API doit être étendu.

**Effort estimé** : 30 min à 1 h.

### P1-C — Clarification token absent dans le FAB

Quand le backend répond `needsClarification`, le message suivant ne réutilise pas explicitement le `clarificationToken`. Le contexte peut être perdu entre deux échanges.

**Fichier cible probable** : `src/components/ai/AiAssistantFAB.tsx`.

**Effort estimé** : 1 h.

### P1-D — QA voix humaine à réaliser

Le corpus est présent, mais aucun test audio réel n'a encore été exécuté. Il faut un test terrain humain de 30 min avec le corpus de 20 phrases, sur téléphone et ordinateur.

**Seuil recommandé** : au moins 85 % de reconnaissance correcte des mots métier et noms clients/projets.

## P2 — Polish

- Badge Tâches dépend du rafraîchissement React Query et peut avoir jusqu'à 30 s de latence.
- Audit IA retiré du top-nav mais encore accessible via URL directe `/ai/audit`; futur lien possible depuis l'en-tête Assistant IA.
- BackButton fonctionne mais la détection `history.length` reste imparfaite après entrée directe / refresh.
- Le corpus voix reste manuel tant qu'il n'existe pas de fixtures audio automatisées.

## Recommandation d'exécution immédiate

1. Corriger P0-A dans le backend : forcer la distinction `create` / `update`, ajouter des tests d'intention en français.
2. Corriger P0-B dans le frontend : ouverture idempotente du Sheet, protection contre double toggle et premier clic perdu.
3. Retester ces deux points sur 7 modules : Dashboard, CRM, Projets, Planning, Notes, Photos, Devis.
4. Traiter ensuite P1-A, P1-B et P1-C pour une démo commerciale élargie.
5. Réaliser la QA voix humaine avec le corpus métier avant déploiement terrain.

## Prompt CC recommandé

```text
Tu es Claude Code. Objectif : corriger les deux P0 issus de l'audit MobAI ProBAT post-corrections.

Référence : reports/probat-audit-mobai-post-corrections.md

P0-A — NLU create/modify
- Auditer backend-worker/src/routes/public/ai.ts.
- Corriger la classification d'intention pour que les verbes français de création (`crée`, `ajoute`, `nouveau`, `planifie`, `génère`) soient classés comme create et non update.
- Ajouter tests ou fixtures pour au moins 10 phrases : créer tâche, ajouter note, créer devis, planifier rendez-vous, créer contact.
- Critère d'acceptation : `Crée une tâche pour le projet Rochat : Appeler Müller Thomas demain à 10h` ne doit plus répondre `que souhaitez-vous modifier`.

P0-B — FAB premier clic intermittent
- Auditer src/components/ai/AiAssistantFAB.tsx.
- Corriger l'ouverture du Sheet pour qu'un seul clic/tap ouvre toujours l'assistant.
- Éviter le toggle open→close sur double clic rapide.
- Tester desktop et mobile sur Dashboard, CRM, Projets, Planning, Notes, Photos, Devis.

Ne fais pas de refactor large. Fais PR backend pour P0-A et PR frontend pour P0-B. Lance typecheck/tests pertinents et donne les preuves réseau/UI.
```

## Verdict opérationnel

- Démo guidée : possible.
- Démo client libre : à éviter tant que P0-A et P0-B ne sont pas corrigés.
- GO pur : après correction des deux P0 et retest rapide.

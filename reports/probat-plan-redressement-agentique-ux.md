# ProBAT — Plan de redressement agentique et UX globale

Date de capture : 2026-06-02
Source : retour utilisateur global après régressions IA / voix / navigation
Statut : plan d'action P0 — remplacer les correctifs ponctuels par une refonte contrôlée du moteur agentique et des parcours UX

## Verdict

Les corrections ponctuelles sur un écran ou un intent ne suffisent plus. Le problème est systémique : l'application ne dispose pas encore d'une vraie boucle agentique `comprendre → chercher → raisonner → proposer → confirmer → agir → vérifier`, et l'UX impose trop de manipulations. Il faut suspendre les micro-correctifs isolés et lancer un audit transversal suivi d'une exécution par blocs.

## Problèmes systémiques constatés

### 1. Compréhension métier insuffisante

L'assistant ne comprend pas assez bien les demandes naturelles. Il traite trop souvent les phrases comme des commandes isolées au lieu de les interpréter dans le contexte métier : module courant, entité affichée, historique de conversation, données existantes et intention réelle de l'utilisateur.

### 2. Pas de mémoire de suivi fiable

Le système perd le fil entre une demande, une clarification et une confirmation. Une réponse comme `oui`, `Robin Bellenot` ou `remplace par Alexandre Baratta` devrait poursuivre l'action précédente, pas redémarrer une nouvelle conversation.

### 3. Recherche métier insuffisante

Quand l'utilisateur donne un nom de contact, un client, un chantier ou une facture, l'agent doit chercher dans les données avant de demander des précisions. Les clarifications ne doivent intervenir qu'en cas d'ambiguïté réelle.

### 4. Voix non omniprésente

La voix doit être disponible partout où l'assistant ou une action métier est disponible. Le texte et l'audio doivent passer par la même logique agentique, avec les mêmes capacités de clarification et d'action.

### 5. UX trop lourde et peu plaisante

La navigation latérale et les parcours imposent trop d'actions : ouvrir menu, choisir onglet, refermer manuellement, changer d'écran, revenir. L'app ne donne pas encore une sensation fluide, simple, directe et agréable.

## Décision de méthode

Ne plus corriger écran par écran sans architecture commune. Lancer un plan par blocs :

1. audit transversal agentique et UX ;
2. moteur agentique commun ;
3. voix globale ;
4. simplification navigation mobile/desktop ;
5. validation terrain par scénarios métier.

Chaque bloc doit avoir des critères d'acceptation mesurables et des tests de non-régression.

## Bloc A — Audit transversal obligatoire

### Objectif

Auditer toute l'application pour identifier où l'assistant, la voix et la navigation échouent.

### Modules à couvrir

- Dashboard ;
- CRM Companies ;
- CRM Contacts ;
- CRM Opportunities ;
- Projects ;
- Planning ;
- Process ;
- Supply ;
- Field Notes ;
- Field Photos ;
- Field Tasks ;
- Documents imported ;
- Quotes & Invoices ;
- AI Conversations ;
- AI Audit.

### Sortie attendue

Pour chaque module :

- actions métier possibles ;
- phrases utilisateur naturelles ;
- données à rechercher ;
- clarifications acceptables ;
- erreurs actuelles ;
- nombre de clics actuel ;
- friction mobile ;
- priorité P0/P1/P2.

## Bloc B — Moteur agentique commun

### Objectif

Construire ou refondre la logique commune qui gère toutes les actions métier, au lieu d'empiler des prompts et exceptions.

### Boucle obligatoire

1. **Comprendre** l'intention : créer, modifier, rechercher, expliquer, supprimer/annuler, planifier, résumer.
2. **Extraire** les entités : contact, entreprise, projet, tâche, note, devis, facture, photo, commande.
3. **Chercher** dans la base avant de demander à l'utilisateur.
4. **Résoudre** les ambiguïtés : homonymes, plusieurs projets, champ manquant.
5. **Proposer** une action claire avec ancienne valeur et nouvelle valeur.
6. **Confirmer** si l'action modifie la base ou touche un champ critique.
7. **Exécuter** via un endpoint métier fiable.
8. **Vérifier** que la donnée a changé.
9. **Répondre** en français simple : `C'est fait`, avec lien/objet concerné.

### Interdictions

- Proposer une action avec valeur cible vide, sauf demande explicite d'effacement.
- Demander un projet/chantier si un lookup contact/client suffit.
- Perdre le contexte après `oui`, `non`, ou une précision courte.
- Mélanger `create` et `update`.
- Répondre avec une clarification générique quand une recherche métier est possible.

## Bloc C — Voix globale

### Objectif

La voix doit être disponible dans tous les modules importants et utiliser la même boucle agentique que le texte.

### Règles

- Un bouton micro global doit être disponible dans l'assistant flottant.
- Les écrans métier doivent proposer une action vocale contextuelle quand c'est utile : Contacts, Notes, Tâches, Photos, Devis, Planning.
- La transcription doit être visible, modifiable et confirmable avant exécution si l'action est sensible.
- Le vocabulaire métier et les noms réels doivent être utilisés comme contexte de transcription.

## Bloc D — UX navigation et plaisir d'usage

### Objectif

Rendre l'application directe, fluide et agréable, surtout sur mobile.

### Corrections attendues

- Le menu latéral mobile doit se fermer automatiquement après sélection d'une entrée.
- Les actions principales doivent être accessibles en un clic depuis chaque module.
- Les retours arrière doivent être évidents.
- L'assistant doit éviter les allers-retours vers un menu séparé.
- Les parcours fréquents doivent être mesurés en nombre de taps.
- Les transitions doivent être stables et premium.

### Seuils

- Créer une tâche depuis Dashboard : maximum 2 actions utilisateur avant saisie.
- Modifier un contact depuis Contacts : maximum 2 actions utilisateur avant dictée/saisie.
- Ouvrir l'assistant depuis n'importe quel écran : 1 tap.
- Changer d'onglet via menu mobile : 1 tap + fermeture automatique du menu.

## Bloc E — Scénarios de validation terrain

### Scénarios P0 à passer

1. Modifier le nom d'un contact.
2. Modifier le téléphone d'un contact.
3. Créer une tâche liée à un projet.
4. Ajouter une note chantier par voix.
5. Créer un devis simple.
6. Demander les tâches urgentes.
7. Modifier le statut d'une tâche.
8. Rechercher un projet/client par nom.
9. Résumer une photo ou un document.
10. Naviguer sur mobile sans rester bloqué dans le menu.

### Critère de réussite

Chaque scénario doit passer en texte et, quand applicable, en voix. L'utilisateur ne doit pas devoir reformuler plus d'une fois, sauf ambiguïté réelle.

## Ordre d'exécution recommandé

| Ordre | Ticket | But | Effort estimé |
|---|---|---|---|
| 1 | AUDIT-AGENTIC-001 | Audit transversal 15 modules | 0,5 j |
| 2 | AGENT-CORE-001 | Boucle agentique commune + contrats d'action | 1 à 2 j |
| 3 | AGENT-MEMORY-001 | Mémoire multi-tour, pending/clarification tokens | 0,5 à 1 j |
| 4 | AGENT-LOOKUP-001 | Recherche métier avant clarification | 1 j |
| 5 | VOICE-GLOBAL-001 | Micro global + voix par modules clés | 1 à 2 j |
| 6 | UX-NAV-001 | Menu mobile auto-close + parcours rapides | 0,5 à 1 j |
| 7 | E2E-SCENARIOS-001 | Tests et smoke 10 scénarios terrain | 0,5 à 1 j |

## Prompt CC recommandé

```text
Tu es Claude Code. Stop aux micro-correctifs isolés. Objectif : lancer un plan de redressement global ProBAT sur IA agentique, voix et UX.

Référence : reports/probat-plan-redressement-agentique-ux.md

Constat : l'assistant ne comprend pas assez bien, perd le contexte multi-tour, ne cherche pas assez dans les données, la voix n'est pas disponible partout, et l'UX mobile/menu est trop lourde. Il faut traiter toute l'app, pas seulement Contacts.

Phase 1 — Audit transversal, sans code au début
- Auditer les modules : Dashboard, CRM Companies, CRM Contacts, CRM Opportunities, Projects, Planning, Process, Supply, Field Notes, Field Photos, Field Tasks, Documents imported, Quotes & Invoices, AI Conversations, AI Audit.
- Pour chaque module, produire : actions métier possibles, phrases utilisateur naturelles, données à rechercher, clarifications acceptables, erreurs actuelles, nombre de clics, friction mobile, priorité P0/P1/P2.
- Identifier l'architecture actuelle de l'agent : intent classification, lookup DB, pendingActionToken, clarificationToken, tool/action execution, confirmation, mémoire conversationnelle.
- Identifier pourquoi le texte et la voix ne partagent pas une même boucle fiable.

Phase 2 — Proposer un plan d'implémentation par PR
- PR 1 : AGENT-CORE-001, boucle agentique commune comprendre → chercher → raisonner → proposer → confirmer → agir → vérifier.
- PR 2 : AGENT-MEMORY-001, conservation multi-tour des pendingActionToken / clarificationToken dans FAB et backend.
- PR 3 : AGENT-LOOKUP-001, lookup métier avant clarification sur contacts, entreprises, projets, tâches, devis/factures.
- PR 4 : VOICE-GLOBAL-001, micro global + voix disponible dans Contacts, Notes, Tâches, Photos, Devis, Planning.
- PR 5 : UX-NAV-001, menu mobile auto-close, navigation plus directe, actions principales en 1 tap.
- PR 6 : E2E-SCENARIOS-001, 10 scénarios terrain texte + voix quand applicable.

Contraintes strictes
- Ne pas patcher uniquement Contacts.
- Ne pas ajouter des exceptions sans architecture commune.
- Ne jamais proposer une update avec valeur cible vide.
- Ne pas demander projet/chantier si une recherche contact/client/projet suffit.
- Ne pas perdre le contexte après oui/non/précision courte.
- Ne pas modifier pricing/droits/sécurité hors périmètre.

Critères de succès
- L'utilisateur peut demander naturellement une action sur n'importe quel module clé.
- L'agent cherche dans les données avant de demander une précision.
- Les clarifications sont courtes, utiles et contextuelles.
- Le texte et la voix utilisent la même logique métier.
- Le menu mobile se ferme automatiquement après sélection.
- Les 10 scénarios terrain passent sans tourner en rond.

Livrable attendu maintenant
- Audit transversal complet.
- Diagramme ou description de l'architecture agentique cible.
- Plan PR par PR avec fichiers, risques, tests et critères d'acceptation.
- Ne commence le code qu'après avoir présenté ce plan.
```

## Verdict opérationnel

La démo guidée reste possible, mais il ne faut plus présenter l'assistant comme agent métier autonome tant que ce plan n'est pas exécuté. La priorité n'est plus un bug isolé : c'est la fiabilité globale de la boucle agentique et la simplicité d'usage.

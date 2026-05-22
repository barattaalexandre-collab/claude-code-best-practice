# backend-worker — Option B: priorité corrections Yannick avant prochaine présentation

## Décision opérationnelle

Option B est retenue: **ne pas lancer SEC-001 PR 3 maintenant**.

La suppression du fallback `x-organization-id` reste documentée dans `reports/backend-worker-sec001-pr3-mini-plan.md`, mais elle est mise en attente. La priorité devient la préparation de la prochaine présentation avec une application plus fiable, plus lisible et alignée sur les retours de Yannick.

## Pourquoi ce choix est cohérent

Le compte-rendu Yannick montre que le risque principal avant la prochaine présentation n'est plus le dernier durcissement technique SEC-001, mais la perception produit et la fiabilité de la démo:

- le scénario doit partir des problèmes réels du client,
- les rôles et droits doivent être compréhensibles,
- l'assistant IA doit paraître simple et fiable,
- le cas multi-chantiers / même client doit être sécurisé,
- Alexandre doit pouvoir diagnostiquer ce que fait l'IA,
- les coûts API/LLM et la migration de données doivent être préparés comme objections commerciales.

## Règles de gel sécurité

Pendant Option B:

1. Ne pas supprimer le fallback `x-organization-id`.
2. Ne pas lancer SEC-001 PR 3.
3. Ne pas ouvrir SEC-002..SEC-007 sauf bug bloquant ou validation explicite.
4. Garder les acquis déjà validés:
   - Bearer token applicatif en production,
   - bundle Lovable `BUFNQkkc`,
   - Upstash Redis terminé,
   - tests existants verts selon les rapports d'exécution.
5. Si une correction produit touche l'auth ou les droits, demander un mini-plan séparé avant code.

## Objectif de la prochaine séquence

Livrer un **pack démo fiable** plutôt qu'un hardening technique supplémentaire.

La prochaine présentation doit montrer:

1. une histoire claire: problème client → vision dashboard/flux → assistant voix,
2. une navigation qui ne fait pas "usine à gaz",
3. une carte rôles/droits compréhensible,
4. un assistant IA simple: micro, photo, note, historique replié,
5. un cas voix répété et fiable,
6. un mécanisme de clarification si client/contact/projet/lieu est ambigu,
7. un accès support/admin pour diagnostiquer les erreurs IA,
8. une réponse crédible aux objections migration et coûts API.

## Tickets recommandés avant prochaine présentation

### DEMO-001 — Scénario de démo en 3 actes

**Type:** non-code d'abord, puis éventuel mode démo guidé.

**But:** éviter la visite exhaustive de menus.

**Livrable attendu:** script de démonstration:

1. découvrir les irritants du client,
2. montrer dashboard / analytics / flux métier,
3. montrer l'assistant voix seulement sur un cas maîtrisé.

**Critère de validation:** Alexandre peut dérouler la démo sans improviser un cas IA risqué.

### DEMO-002 — Carte rôles & droits

**Type:** frontend isolé.

**But:** remplacer la perception "qui êtes-vous ?" par une lecture métier des droits.

**Livrable attendu:** vue rôles/droits avec au minimum:

- propriétaire / CEO,
- administrateur organisation,
- manager / chef de projet,
- terrain / technicien,
- finance / comptabilité,
- viewer / externe,
- platform admin / support.

**Critère de validation:** chaque rôle indique ce qu'il voit, ce qu'il peut modifier, ce qu'il ne peut pas faire et quelles validations sont nécessaires.

### DEMO-003 — Assistant IA simplifié pour la démo

**Type:** frontend isolé.

**But:** donner l'impression "vous parlez, l'app structure et propose".

**Livrable attendu:** écran assistant orienté action:

- gros bouton micro,
- bouton photo,
- bouton note,
- historique replié,
- bruit visuel réduit,
- menus non essentiels repliés pendant la démo.

**Critère de validation:** l'assistant est compréhensible en moins de 10 secondes par un prospect.

### DEMO-004 — Fiabiliser le cas multi-chantiers / même client

**Type:** backend + tests IA / métier.

**But:** éviter que l'IA rattache un nouveau chantier au mauvais projet existant.

**Règle métier attendue:** si client/contact existe mais lieu, adresse ou contexte diffère, ne jamais fusionner automatiquement.

**Comportement attendu:** demander clarification ou proposer explicitement:

- créer un nouveau chantier,
- rattacher au chantier existant.

**Critère de validation:** le cas "Bernard Müller à Colombier" ne doit plus être rattaché automatiquement à un autre chantier sans confirmation.

### DEMO-005 — Console support/admin IA minimale

**Type:** backend + frontend admin, scope minimal.

**But:** permettre à Alexandre de diagnostiquer une erreur en direct.

**Livrable attendu:** vue support read-only affichant au minimum:

- transcript reçu,
- intention détectée,
- entités candidates,
- chantier/projet choisi,
- action proposée,
- confirmation,
- erreur éventuelle.

**Critère de validation:** en cas d'erreur IA, Alexandre peut expliquer ce qui s'est passé sans fouiller les logs bruts.

### DEMO-006 — Objections commerciales: migration et coûts API

**Type:** non-code prioritaire.

**But:** répondre aux deux objections attendues:

1. "Je vais devoir remplir votre app en plus de mon système actuel."
2. "Qui paie OpenAI, Deepgram, Supabase, Render, Redis ?"

**Livrable attendu:** une page ou fiche courte avec:

- processus d'import V1 même semi-manuel,
- données importables en premier,
- modèle de coût POC,
- quotas ou limites,
- responsabilité des dépassements.

## Ordre recommandé

1. DEMO-001 — scénario de démo.
2. DEMO-004 — multi-chantiers même client.
3. DEMO-003 — assistant IA simplifié.
4. DEMO-002 — carte rôles & droits.
5. DEMO-005 — console support/admin IA minimale.
6. DEMO-006 — migration et coûts API.

Si le temps est court, ne faire que les quatre premiers avant la présentation.

## Prompt exact à donner à Claude Code maintenant

```text
Option B est validée.

Ne lance pas SEC-001 PR 3.
Ne supprime pas le fallback x-organization-id.
Ne lance pas SEC-002..SEC-007.

Nouvelle priorité: préparer la prochaine présentation selon le compte-rendu Yannick.

Lis d'abord:
- reports/backend-worker-option-b-demo-readiness.md
- reports/backend-worker-compte-rendu-seance-yannick-2026-05-08.md
- reports/backend-worker-correctifs-a-faire.md

Fais uniquement un mini-audit / plan d'exécution, sans modifier le code.

Je veux un plan en tickets courts pour:
1. scénario de démo en 3 actes,
2. correction multi-chantiers même client / nouveau lieu,
3. assistant IA simplifié,
4. carte rôles & droits,
5. console support/admin IA minimale,
6. objections migration et coûts API.

Pour chaque ticket, donne:
- objectif,
- fichiers probables,
- risque,
- tests,
- critère de validation démo,
- rollback.

Stop après le plan. Attends validation avant de coder.
```

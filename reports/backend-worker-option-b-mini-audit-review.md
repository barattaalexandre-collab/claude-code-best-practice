# backend-worker — Revue du mini-audit Option B

## Verdict

Le mini-audit Option B est **validé avec ajustement de périmètre**.

La direction est bonne: préparer la prochaine présentation avant de relancer SEC-001 PR 3 ou SEC-002..SEC-007. Le plan colle aux retours Yannick: scénario, multi-chantiers, assistant simplifié, rôles/droits, console support IA et objections migration/coûts.

## Décision d'exécution

Ne pas valider les 6 tickets d'un coup.

Autoriser uniquement une première séquence courte:

1. **DEMO-001 — Scénario de démo en 3 actes**
2. **DEMO-004 — Multi-chantiers même client / nouveau lieu**
3. **DEMO-003 — Assistant IA simplifié**
4. **DEMO-002 — Carte rôles & droits**

DEMO-005 et DEMO-006 restent en attente tant que les quatre premiers ne sont pas relus et testés à blanc.

## Points validés

### DEMO-001 — scénario

Validé.

- Risque nul car hors app.
- Créer `reports/DEMO-SCRIPT.md` est utile.
- Le script doit être utilisable sans improvisation.
- Chaque acte doit tenir en moins de 3 minutes.

### DEMO-004 — multi-chantiers

Validé, mais à cadrer strictement.

Objectif accepté:

- ajouter un deuxième chantier actif dans les mock data,
- rendre visible le chantier actif,
- permettre un basculement simple pendant la démo.

Ajustement important:

- préférer une implémentation minimale locale si `AppContext` rend le changement trop large,
- ne pas transformer ce ticket en refactor global de contexte,
- ne pas modifier la logique backend ou l'auth,
- ne pas prétendre résoudre toute l'entity resolution IA si le ticket ne fait que préparer une démo mock.

### DEMO-003 — assistant IA simplifié

Validé.

- Changement visuel limité à `VoiceInputBar.tsx` en priorité.
- Ne pas modifier le pipeline IA, la transcription, la confirmation ou les appels API.
- Garder le rollback simple: restaurer le bloc `quickActions.map`.

### DEMO-002 — carte rôles & droits

Validé.

- Page statique acceptée.
- `platform_admin` doit être présenté comme rôle support/admin distinct, pas comme rôle client sélectionnable.
- Ne pas modifier les droits réels sans plan séparé.

## Tickets non validés maintenant

### DEMO-005 — console support/admin IA minimale

À reporter après les quatre premiers tickets.

Raison:

- utile, mais moins critique pour le premier ressenti client,
- peut toucher `AuditLog.tsx`, sidebar et données mock,
- risque de faire dévier la préparation vers l'observabilité au lieu de la démo principale.

### DEMO-006 — objections migration et coûts API

À traiter hors app d'abord, après DEMO-001.

Raison:

- utile commercialement,
- peut être un document de parole plutôt qu'une page in-app,
- ne doit pas bloquer les corrections visuelles et multi-chantiers.

## Règles à rappeler à Claude Code

Pendant cette séquence:

1. Ne pas lancer SEC-001 PR 3.
2. Ne pas supprimer le fallback `x-organization-id`.
3. Ne pas lancer SEC-002..SEC-007.
4. Ne pas modifier l'auth.
5. Ne pas faire de refactor global.
6. Ne pas coder les 6 tickets en une seule fois.
7. Faire un commit/PR par ticket ou par lot très court validé.
8. Après chaque ticket: fournir fichiers modifiés, diff résumé, tests/checks, risques et rollback.

## Prompt exact — première autorisation de code

```text
Mini-audit Option B validé partiellement.

Tu peux coder uniquement la première séquence DEMO, pas les 6 tickets complets.

Périmètre autorisé maintenant:
1. DEMO-001 — créer reports/DEMO-SCRIPT.md avec le scénario de démo en 3 actes.
2. DEMO-004 — préparer le cas multi-chantiers même client / nouveau lieu avec une implémentation minimale.
3. DEMO-003 — simplifier l'assistant IA visuellement, sans toucher au pipeline IA.
4. DEMO-002 — créer une carte rôles & droits statique, sans modifier les droits réels.

Interdictions:
- Ne lance pas SEC-001 PR 3.
- Ne supprime pas le fallback x-organization-id.
- Ne lance pas SEC-002..SEC-007.
- Ne modifie pas l'auth.
- Ne touche pas au backend sauf si DEMO-004 prouve qu'un petit ajustement mock/test est indispensable.
- Ne fais pas DEMO-005 maintenant.
- Ne fais pas DEMO-006 in-app maintenant.
- Ne fais pas de refactor global AppContext si un état local suffit pour la démo.

Ordre obligatoire:
1. DEMO-001 d'abord.
2. DEMO-004 ensuite.
3. DEMO-003 ensuite.
4. DEMO-002 ensuite.

Après chaque ticket, arrête-toi et donne:
- fichiers modifiés,
- résumé du diff,
- tests/checks exécutés,
- capture si changement UI visible,
- risque restant,
- rollback.

Si tu estimes que DEMO-004 nécessite un changement AppContext global, arrête-toi avant de coder ce changement et propose une alternative minimale.
```

## Critère pour passer à DEMO-005 / DEMO-006

Ne passer à DEMO-005 ou DEMO-006 que si:

1. DEMO-001 à DEMO-004 sont implémentés,
2. l'app tourne,
3. la démo à blanc passe sans blocage,
4. Alexandre valide que le temps restant justifie d'ajouter console support ou objections in-app.

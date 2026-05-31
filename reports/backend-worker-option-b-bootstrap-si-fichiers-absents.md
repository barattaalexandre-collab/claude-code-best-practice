# backend-worker — Bootstrap Option B si les 3 fichiers sources sont absents

## Verdict opérationnel

Si Claude Code confirme que ces trois fichiers n'existent nulle part sur le Mac:

- `backend-worker-option-b-demo-readiness.md`
- `backend-worker-compte-rendu-seance-yannick-2026-05-08.md`
- `backend-worker-correctifs-a-faire.md`

alors ne pas bloquer la préparation: **les recréer dans le repo cible à partir du cadrage ci-dessous**, puis demander uniquement un mini-audit / plan sans coder.

## Décision

Option B reste la décision courante:

1. Ne pas lancer SEC-001 PR 3 maintenant.
2. Ne pas supprimer le fallback `x-organization-id`.
3. Ne pas ouvrir SEC-002..SEC-007 sans validation explicite.
4. Prioriser la prochaine présentation et les corrections issues de la séance Yannick.
5. Objectif: pack démo fiable, pas hardening technique large.

## Synthèse Yannick à recréer

Points clés à intégrer dans `reports/backend-worker-compte-rendu-seance-yannick-2026-05-08.md`:

1. La vente doit démarrer par les problèmes réels du client, pas par une visite exhaustive de l'application.
2. La page rôles/personnes crée de la confusion; remplacer par une carte rôles & droits.
3. La sécurité d'accès doit être mieux expliquée: MFA ou magic link, session timeout, droits réels par rôle.
4. Le flux voix transcrit bien, mais la résolution métier échoue sur les cas multi-chantiers / même client.
5. Le cas critique observé est du type: `Nouveau chantier chez Bernard Müller à Colombier...` qui peut être rattaché au mauvais chantier existant.
6. Règle attendue: si même client/contact mais lieu/adresse/contexte différent, ne jamais fusionner automatiquement; demander clarification.
7. Alexandre a besoin d'un accès `platform_admin` ou support pour diagnostiquer les flux IA en direct.
8. L'assistant IA doit être simplifié: micro, photo, note, historique replié, moins de bruit visuel.
9. Les swimlanes / React Flow peuvent aider la discussion client en mode atelier de coproduction.
10. La migration/import des données existantes est une objection commerciale incontournable.
11. Le modèle coûts API/LLM doit être clarifié: OpenAI, Deepgram, Supabase, Render, Redis, quotas et dépassements.
12. La prochaine vente doit être positionnée comme audit / coproduction / prototype adapté, pas produit figé imposé.

## Backlog correctifs à recréer

Points à intégrer dans `reports/backend-worker-correctifs-a-faire.md`:

### P0 avant prochaine présentation

1. **DEMO-001 — Scénario de démo en 3 actes**
   - Problème client.
   - Dashboard / analytics / flux métier.
   - Assistant voix seulement sur un cas répété et maîtrisé.

2. **DEMO-004 — Multi-chantiers même client / nouveau lieu**
   - Distinguer client, contact, chantier/projet et lieu.
   - Comparer adresse, commune, nom de chantier, historique et statut.
   - Ne jamais fusionner automatiquement si le lieu ou le contexte diffère.
   - Proposer `Créer un nouveau chantier` ou `Rattacher au chantier existant`.

3. **DEMO-003 — Assistant IA simplifié**
   - Gros bouton micro.
   - Bouton photo.
   - Bouton note.
   - Historique replié.
   - Menus non essentiels repliés pendant la démo.

4. **DEMO-002 — Carte rôles & droits**
   - Rôles métier, pas personnes.
   - Propriétaire / CEO, admin organisation, manager, terrain, finance, viewer/externe, platform admin/support.
   - Pour chaque rôle: ce qu'il voit, modifie, ne peut pas faire, validations nécessaires.

### P1 important

5. **DEMO-005 — Console support/admin IA minimale**
   - Transcript reçu.
   - Intention détectée.
   - Entités candidates.
   - Projet/chantier choisi.
   - Action proposée.
   - Confirmation.
   - Erreur éventuelle.

6. **DEMO-006 — Migration et coûts API**
   - Processus d'import V1 même semi-manuel.
   - Données importables en premier: clients, contacts, projets/chantiers, catalogues, documents.
   - Modèle de coût POC, quotas, dépassements.

### À reporter

- SEC-001 PR 3.
- SEC-002..SEC-007.
- Gros refactors UX non liés à la démo.
- Swimlanes complètes si le délai est court; garder en P1 sauf si nécessaire pour la présentation.

## Contenu minimal pour `backend-worker-option-b-demo-readiness.md`

Le document doit dire:

- Option B est validée.
- PR 3 est suspendue.
- Priorité: prochaine présentation.
- Ordre recommandé:
  1. DEMO-001 scénario de démo.
  2. DEMO-004 multi-chantiers même client.
  3. DEMO-003 assistant IA simplifié.
  4. DEMO-002 carte rôles & droits.
  5. DEMO-005 console support/admin IA minimale.
  6. DEMO-006 migration et coûts API.
- Si temps court: faire uniquement les quatre premiers.
- Claude Code doit produire un mini-audit / plan avant tout code.

## Prompt à donner à Claude Code pour recréer les fichiers

```text
Les trois fichiers Option B n'existent pas sur ce Mac. Tu dois les recréer dans /Users/alexandrebaratta/backend-worker/reports/ à partir du cadrage ci-dessous.

Ne code rien dans l'application.
Ne lance pas SEC-001 PR 3.
Ne supprime pas le fallback x-organization-id.
Ne lance pas SEC-002..SEC-007.

Crée ou remplace uniquement ces fichiers markdown:
- reports/backend-worker-option-b-demo-readiness.md
- reports/backend-worker-compte-rendu-seance-yannick-2026-05-08.md
- reports/backend-worker-correctifs-a-faire.md

Contenu à intégrer:
- décision Option B: priorité prochaine présentation, PR 3 en attente,
- synthèse Yannick: problèmes client d'abord, rôles/droits, sécurité d'accès, assistant IA trop chargé, multi-chantiers même client, platform_admin, observabilité IA, migration de données, coûts API/LLM,
- backlog: DEMO-001 scénario, DEMO-004 multi-chantiers, DEMO-003 assistant simplifié, DEMO-002 rôles/droits, DEMO-005 console support/admin, DEMO-006 migration/coûts,
- ordre recommandé: DEMO-001, DEMO-004, DEMO-003, DEMO-002, DEMO-005, DEMO-006,
- si temps court: uniquement les quatre premiers.

Après création, vérifie que les trois fichiers existent, puis arrête-toi. Ne fais pas encore le mini-audit.
```

## Prompt à donner après recréation réussie

```text
Les 3 fichiers Option B sont maintenant présents dans reports/.

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

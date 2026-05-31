# backend-worker — Index des livrables `reports/`

Ce document sert de point d'entrée unique.

## Fichiers clés

1. `backend-worker-audit-preliminary.md`
   - Audit préliminaire, risques, priorisation P0/P1/P2.
2. `backend-worker-cloud-code-handoff.md`
   - Plan opérationnel pour Cloud/Claude Code.
3. `backend-worker-github-issues-prompts.md`
   - Templates détaillés SEC-001..SEC-007.
4. `backend-worker-issues-created.md`
   - Suivi des issues créées et ordre recommandé.
5. `backend-worker-deployment-status-and-next-step.md`
   - Statut déploiement + étape Redis Upstash restante.
6. `backend-worker-compte-rendu-seance-yannick-2026-05-08.md`
   - Retours séance Yannick: vente, scénario démo, sécurité perçue, UX assistant et arbitrages à préparer.
7. `backend-worker-correctifs-a-faire.md`
   - Backlog explicite des correctifs sécurité, IA, UX, support, données, infra et vente à valider avant Cloud Code.
8. `backend-worker-plan-execution-cloud-code.md`
   - Mode d'emploi concret: décisions préalables, sprints, tickets EXEC-001..014 et prompts Cloud Code prêts à lancer.
9. `backend-worker-sprint-1-launch.md`
   - Prompt et critères d'acceptation pour lancer immédiatement Sprint 1 Cloud Code.
10. `backend-worker-a-donner-a-claude-code-maintenant.md`
   - Version courte et directement actionnable: quoi ouvrir, quoi donner, quoi refuser et quel prompt copier-coller.
11. `backend-worker-apres-creation-handoff-claude-code.md`
   - Suite immédiate après création du handoff dans le vrai repo: prompt pour lancer Redis/Upstash, CI et SEC-001 phase 2.
12. `backend-worker-etapes-transmission-claude-code.md`
   - Déroulé étape par étape de ce qu'il faut faire, transmettre, vérifier et valider avec Claude Code.
13. `backend-worker-github-sync-reality-check.md`
   - Correction post-synchronisation: PR locale introuvable, commit réel `e86a9b6`, 19 fichiers réels et handoff Sprint 2 à utiliser.
14. `backend-worker-sprint-2-status-ci-sec001-upstash.md`
   - Statut Sprint 2 réel: CI terminée (`363682c`), SEC-001 phase 2 bloqué par frontend headers, Upstash credentials requis.
15. `backend-worker-message-simple-pour-claude-code.md`
   - Message minimal à utiliser maintenant: ne plus envoyer l'historique, traiter seulement Upstash Redis / pending actions.
16. `backend-worker-message-simple-pour-claude-code.txt`
   - Contenu brut à copier/créer si le fichier markdown est absent du repo cible.
17. `backend-worker-action-immediate-pas-a-pas.md`
   - Prochaine action unique avec prompt exact: Claude Code/Chrome configure Upstash Redis puis vérifie pending actions.
18. `backend-worker-option-b-demo-readiness.md`
   - Décision Option B: suspendre PR 3 et prioriser les corrections Yannick pour la prochaine présentation.
19. `backend-worker-prochaine-action-sec001-phase2.md`
   - Statut SEC-001 phase 2: complet en prod, bundle Lovable `BUFNQkkc`; PR 3 seulement après validation explicite.
20. `backend-worker-sec001-pr3-mini-plan.md`
   - Mini-plan PR 3 formalisé, mais mis en attente pendant Option B.
21. `backend-worker-option-b-files-a-fournir.md`
   - Guide de transfert des trois fichiers Option B manquants vers `/Users/alexandrebaratta/backend-worker/reports/`.
22. `backend-worker-option-b-bootstrap-si-fichiers-absents.md`
   - Plan de recréation minimal si les trois fichiers Option B n'existent nulle part sur le Mac.
23. `backend-worker-option-b-mini-audit-review.md`
   - Revue du mini-audit Option B: validation partielle, ordre d'exécution et prompt pour coder uniquement DEMO-001..004.
24. `backend-worker-option-b-demo-001-004-status.md`
   - Statut après exécution DEMO-001..004 et décision: répétition à blanc avant DEMO-005/006.
25. `probat-notes-correction-consolidees.md`
   - Notes ProBAT consolidées: priorité critique sur reconnaissance vocale, assistant IA omniprésent, retours arrière et simplification UX.

## Option prompt direct

- `backend-worker-claude-code-exact-prompt.txt` (copier-coller brut)
- `backend-worker-claude-code-exact-prompt.md` (lecture GitHub)
- `backend-worker-claude-code-master-handoff.md` (version compacte)

## Lecture recommandée maintenant

Pour répondre au "alors ?" opérationnel: si le repo cible ne contient pas les fichiers Option B, commencer par `backend-worker-option-b-files-a-fournir.md`. Si la recherche confirme qu'ils n'existent nulle part sur le Mac, utiliser `backend-worker-option-b-bootstrap-si-fichiers-absents.md` pour les recréer minimalement. Une fois le mini-audit reçu, lire `backend-worker-option-b-mini-audit-review.md`: coder uniquement DEMO-001..004, pas DEMO-005/006 ni SEC-001 PR 3. Après exécution DEMO-001..004, lire `backend-worker-option-b-demo-001-004-status.md` et faire une répétition à blanc avant tout nouveau code.

# Registre de statut documentaire — backend-worker

## Règle officielle (validée)

- **Seul** `reports/backend-worker-cadrage-officiel-v1.md` est la référence officielle V1.
- Aucun autre document ne peut redéfinir priorité, statut commercial, ou GO/NO-GO sans validation explicite d'Alexandre.
- Les autres documents sont classés en **draft / proposition / backlog hardening**.

## Classification des documents

| Fichier | Statut |
|---|---|
| `backend-worker-cadrage-officiel-v1.md` | **official-v1** |
| `backend-worker-droits-modification-annulation-officiel-v1.md` | **official-v1** |
| `backend-worker-audit-preliminary.md` | draft |
| `backend-worker-action-immediate-pas-a-pas.md` | action-immediate-pas-a-pas |
| `backend-worker-apres-creation-handoff-claude-code.md` | suite-operationnelle-immediate |
| `backend-worker-a-donner-a-claude-code-maintenant.md` | prompt-action-immediate |
| `backend-worker-cloud-code-handoff.md` | proposition |
| `backend-worker-claude-code-compact-checklist.md` | backlog-hardening |
| `backend-worker-claude-code-exact-prompt.md` | proposition |
| `backend-worker-claude-code-master-handoff.md` | proposition |
| `backend-worker-compte-rendu-seance-yannick-2026-05-08.md` | input-prioritaire-à-arbitrer |
| `backend-worker-correctifs-a-faire.md` | backlog-explicite-à-valider |
| `backend-worker-deployment-status-and-next-step.md` | proposition |
| `backend-worker-etapes-transmission-claude-code.md` | guide-transmission-etape-par-etape |
| `backend-worker-final-status.md` | draft |
| `backend-worker-github-sync-reality-check.md` | source-verite-github-corrigee |
| `backend-worker-github-issues-prompts.md` | backlog-hardening |
| `backend-worker-issues-created.md` | backlog-hardening |
| `backend-worker-message-simple-pour-claude-code.md` | message-minimal-action-immediate |
| `backend-worker-message-simple-pour-claude-code.txt` | contenu-brut-a-creer-si-absent |
| `backend-worker-message-for-claude.md` | proposition |
| `backend-worker-pack-a-transmettre-a-claude-code.md` | proposition |
| `backend-worker-plan-execution-cloud-code.md` | plan-execution-à-valider |
| `backend-worker-option-b-demo-readiness.md` | decision-operationnelle-option-b |
| `backend-worker-option-b-files-a-fournir.md` | guide-transfert-option-b |
| `backend-worker-option-b-bootstrap-si-fichiers-absents.md` | guide-recreation-option-b |
| `backend-worker-option-b-mini-audit-review.md` | validation-partielle-option-b |
| `backend-worker-option-b-demo-001-004-status.md` | statut-execution-demo-001-004 |
| `backend-worker-prompts-readme.md` | draft |
| `probat-notes-correction-consolidees.md` | backlog-produit-ux-a-valider |
| `probat-audit-mobai-post-corrections.md` | audit-post-corrections-go-sous-reserve |
| `probat-p0-nlu-fab-execution-status.md` | statut-execution-p0-go-avec-qa-fab |
| `probat-crm-contacts-ai-voice-regression.md` | regression-p0-crm-contacts-ai-voice |
| `probat-plan-redressement-agentique-ux.md` | plan-redressement-p0-agentique-ux-global |
| `backend-worker-prochaine-action-sec001-phase2.md` | prochaine-action-mini-audit-sec001 |
| `backend-worker-sec001-pr3-mini-plan.md` | proposition-execution-controlee |
| `backend-worker-propagation-verification.md` | proposition |
| `backend-worker-render-deploy-incident-lockfile-invalid-version.md` | draft |
| `backend-worker-render-deploy-incident-rate-limit.md` | draft |
| `backend-worker-reports-index.md` | draft |
| `backend-worker-START-HERE.md` | proposition |
| `backend-worker-sprint-1-launch.md` | lancement-sprint-1 |
| `backend-worker-sprint-2-status-ci-sec001-upstash.md` | statut-sprint-2-reel |
| `backend-worker-variants-rollout-checklist.md` | backlog-hardening |
| `backend-worker-verification-brief-for-claude.md` | proposition |

## Politique d'orientation structurante

- Toute orientation structurante sécurité/infra doit attendre validation explicite d'Alexandre.
- Interdiction de publier un NO-GO global sans validation explicite.

## Clarification ajoutée après retour séance Yannick

Le compte-rendu Yannick du 2026-05-08 est classé **input-prioritaire-à-arbitrer**: il doit alimenter la préparation démo et les choix produit/vente, mais il ne devient officiel qu'après validation explicite d'Alexandre.
Le document `backend-worker-correctifs-a-faire.md` est le backlog explicite à discuter avant lancement Cloud Code; il ne remplace pas le cadrage officiel V1 tant qu'il n'est pas validé.
Le document `backend-worker-plan-execution-cloud-code.md` décrit comment exécuter les changements par sprints Cloud Code après validation humaine.
Le document `backend-worker-sprint-1-launch.md` est le support opérationnel pour lancer immédiatement Cloud Code sur le premier lot sécurité.
Le document `backend-worker-a-donner-a-claude-code-maintenant.md` est la version la plus directe à copier-coller pour lancer Sprint 1 dans Claude Code.
Le document `backend-worker-apres-creation-handoff-claude-code.md` prend le relais une fois le handoff créé dans le dépôt réel `backend-worker`.
Le document `backend-worker-etapes-transmission-claude-code.md` est le guide détaillé à suivre pour transmettre les tâches à Claude Code sans ouvrir de chantier hors périmètre.
Le document `backend-worker-github-sync-reality-check.md` corrige la source de vérité après constat que la PR/commit local temporaire n'est pas présent sur GitHub; l'exécution doit repartir du commit réel `e86a9b6` dans `backend-worker`.
Le document `backend-worker-sprint-2-status-ci-sec001-upstash.md` devient le point de suivi immédiat: CI OK au commit `363682c`, SEC-001 phase 2 séparé, Upstash à fournir par Alexandre.
Le document `backend-worker-message-simple-pour-claude-code.md` est désormais le message minimal recommandé pour éviter la confusion: uniquement Upstash Redis/pending actions, SEC-001 phase 2 séparé.
Le document `backend-worker-action-immediate-pas-a-pas.md` est le guide à utiliser maintenant: une seule action, Upstash Redis via Claude Code/Chrome, avant tout autre chantier.
Le document `backend-worker-prochaine-action-sec001-phase2.md` remplace l’action Upstash une fois terminée: demander un mini-audit SEC-001 phase 2 avant tout code.
Le document `backend-worker-prochaine-action-sec001-phase2.md` contient maintenant la décision après mini-audit: autoriser PR 1 backend uniquement, sans frontend ni suppression fallback.
Le document `backend-worker-prochaine-action-sec001-phase2.md` indique maintenant que PR 1 est terminée au commit `f90a00c`; la prochaine décision est PR 2 Bearer app-token avec `APP_TOKEN_SECRET`.
Le document `backend-worker-prochaine-action-sec001-phase2.md` précise maintenant la préparation PR 2: générer `APP_TOKEN_SECRET`, le configurer dans Render, puis lancer PR 2 uniquement en gardant le fallback.
Le document `backend-worker-prochaine-action-sec001-phase2.md` indique maintenant que PR 2 est commitée (`a0fe745`, `16d34a1`); la prochaine action est push + vérification production, sans PR 3.
Le document `backend-worker-prochaine-action-sec001-phase2.md` indique maintenant que PR 2 backend est live mais que Lovable sert encore l’ancien bundle; prochaine action: Publish/Deploy Lovable manuel puis vérification, sans PR 3.
Le document `backend-worker-prochaine-action-sec001-phase2.md` indique maintenant que Publish/Deploy Lovable seul repousse l’ancien bundle; il faut coller `config.ts` dans Lovable ou pull GitHub depuis Lovable, puis vérifier.
Le document `backend-worker-prochaine-action-sec001-phase2.md` indique maintenant que SEC-001 phase 2 est complet en production avec bundle Lovable `BUFNQkkc`; PR 3 nécessite seulement un mini-plan avant code.
Le document `backend-worker-sec001-pr3-mini-plan.md` formalise le mini-plan PR 3 de retrait du fallback `x-organization-id`; il reste une proposition d'exécution contrôlée tant qu'Alexandre n'a pas validé le passage au code.
Le document `backend-worker-option-b-demo-readiness.md` formalise la décision Option B: suspendre PR 3 et prioriser les corrections issues du compte-rendu Yannick pour fiabiliser la prochaine présentation.
Le document `backend-worker-sec001-pr3-mini-plan.md` intègre maintenant l'audit complémentaire PR 3: ne pas toucher au bootstrap `_fetchAppToken`, corriger les headers manuels frontend avant retrait backend, et refuser l'ordre backend-first pour éviter une fenêtre de 401 en production.
Le document `backend-worker-option-b-files-a-fournir.md` indique comment fournir au repo cible les trois fichiers Option B manquants avant de relancer le prompt de mini-audit/demo readiness.
Le document `backend-worker-option-b-bootstrap-si-fichiers-absents.md` fournit un cadrage minimal pour recréer les trois fichiers Option B si la recherche locale confirme qu'ils n'existent nulle part sur le Mac.
Le document `backend-worker-option-b-mini-audit-review.md` valide partiellement le mini-audit Option B: autoriser DEMO-001..004 seulement, reporter DEMO-005/006 et maintenir le gel SEC-001 PR 3 / SEC-002..SEC-007.
Le document `backend-worker-option-b-demo-001-004-status.md` constate DEMO-001..004 terminés et recommande une répétition à blanc avant d'autoriser DEMO-005 ou DEMO-006.
Le document `probat-notes-correction-consolidees.md` capture les retours produit ProBAT du 2026-05-31: voix fiable, assistant IA omniprésent et navigation ultra-simple; il reste un backlog à valider et ne modifie pas le cadrage officiel V1.
Le document `probat-audit-mobai-post-corrections.md` capture l'audit MobAI post-corrections CC: GO sous réserve, avec deux P0 à corriger avant GO pur (NLU create/modify et FAB premier clic intermittent); il ne remplace pas le cadrage officiel V1 sans validation explicite.
Le document `probat-p0-nlu-fab-execution-status.md` capture l'exécution des deux P0: backend #14 validé E2E pour le NLU create intent, frontend #15 livré pour le FAB, avec QA humaine courte recommandée sur le premier clic.
Le document `probat-crm-contacts-ai-voice-regression.md` capture une nouvelle régression P0 sur CRM Contacts: voix absente pour modifier un contact, assistant multi-tour confus, recherche contact insuffisante et propositions d'update à valeur vide.
Le document `probat-plan-redressement-agentique-ux.md` élargit le constat: les régressions ne sont pas limitées aux contacts; il faut un audit transversal et une refonte contrôlée de la boucle agentique, de la voix globale et de l'UX mobile/menu.

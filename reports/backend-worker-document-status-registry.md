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
| `backend-worker-prompts-readme.md` | draft |
| `backend-worker-prochaine-action-sec001-phase2.md` | prochaine-action-mini-audit-sec001 |
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

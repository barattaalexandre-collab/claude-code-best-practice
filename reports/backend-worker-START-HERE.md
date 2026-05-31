# START HERE — gouvernance documentaire

## Référence officielle V1

- `reports/backend-worker-cadrage-officiel-v1.md` (**seule source officielle V1**)

## Important

- Les autres documents `reports/backend-worker-*` sont des drafts/propositions/backlog hardening.
- Aucun document ne redéfinit priorité, statut commercial, ou GO/NO-GO sans validation explicite d'Alexandre.


## Alors — prochaine action recommandée

1. **Option B retenue: priorité prochaine présentation.** Ne pas lancer SEC-001 PR 3 maintenant; ne pas supprimer le fallback `x-organization-id`.
2. **Traiter d'abord les corrections issues de Yannick.** Le plan opérationnel est `reports/backend-worker-option-b-demo-readiness.md`.
3. **Objectif court terme: pack démo fiable.** Priorités: scénario de démo, multi-chantiers même client, assistant IA simplifié, carte rôles/droits, console support/admin minimale, objections migration/coûts.
4. **Reporter le hardening large SEC-001..SEC-007.** Les tickets sécurité restent importants, mais ne doivent pas écraser la préparation commerciale immédiate sans validation.
5. **Garder le mini-plan PR 3 en attente.** `reports/backend-worker-sec001-pr3-mini-plan.md` reste disponible, mais seulement après nouvelle validation explicite.

## Documents à lire en premier

- `reports/backend-worker-cadrage-officiel-v1.md` — décisions validées.
- `reports/backend-worker-compte-rendu-seance-yannick-2026-05-08.md` — retours produit / vente à arbitrer.
- `reports/backend-worker-correctifs-a-faire.md` — liste explicite des correctifs à valider avant Cloud Code.
- `reports/backend-worker-plan-execution-cloud-code.md` — mode d'emploi concret pour lancer les changements par sprints Cloud Code.
- `reports/backend-worker-sprint-1-launch.md` — document de lancement immédiat de la première étape Cloud Code.
- `reports/backend-worker-a-donner-a-claude-code-maintenant.md` — réponse courte: quoi faire et quoi copier-coller dans Claude Code maintenant.
- `reports/backend-worker-apres-creation-handoff-claude-code.md` — prochaine action après création du fichier dans le vrai repo: prompt court à donner à Claude Code.
- `reports/backend-worker-etapes-transmission-claude-code.md` — guide étape par étape: quoi faire, quoi transmettre, quoi vérifier avant Sprint 2.
- `reports/backend-worker-github-sync-reality-check.md` — correction de source de vérité: PR locale introuvable, commit réel `e86a9b6`, handoff Sprint 2 sur GitHub.
- `reports/backend-worker-sprint-2-status-ci-sec001-upstash.md` — statut réel Sprint 2: CI faite, SEC-001 phase 2 bloqué, Upstash à créer.
- `reports/backend-worker-message-simple-pour-claude-code.md` — version ultra-simple à copier-coller: uniquement Upstash Redis maintenant, pas SEC-001 ni UX.
- `reports/backend-worker-message-simple-pour-claude-code.txt` — version brute à créer/copier si le fichier `.md` est absent dans le repo cible.
- `reports/backend-worker-action-immediate-pas-a-pas.md` — prochaine action unique, pas à pas, avec le prompt exact à coller dans Claude Code/Chrome.
- `reports/backend-worker-option-b-demo-readiness.md` — décision Option B: priorité corrections Yannick et prochaine présentation.
- `reports/backend-worker-prochaine-action-sec001-phase2.md` — historique SEC-001 phase 2 et décision: PR 3 seulement après validation explicite.
- `reports/backend-worker-sec001-pr3-mini-plan.md` — mini-plan en attente pour retirer le fallback `x-organization-id` plus tard.
- `reports/backend-worker-document-status-registry.md` — statut officiel/draft/proposition de chaque document.

## Prompt opérationnel (proposition)

`Lis reports/backend-worker-option-b-demo-readiness.md et prépare uniquement le mini-audit/plan demandé, sans coder.`

> Ce prompt reste une proposition opérationnelle, pas une décision stratégique validée.

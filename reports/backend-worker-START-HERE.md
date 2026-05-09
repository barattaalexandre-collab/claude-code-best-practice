# START HERE — gouvernance documentaire

## Référence officielle V1

- `reports/backend-worker-cadrage-officiel-v1.md` (**seule source officielle V1**)

## Important

- Les autres documents `reports/backend-worker-*` sont des drafts/propositions/backlog hardening.
- Aucun document ne redéfinit priorité, statut commercial, ou GO/NO-GO sans validation explicite d'Alexandre.


## Alors — prochaine action recommandée

1. **Faire une seule action maintenant.** Utiliser `reports/backend-worker-action-immediate-pas-a-pas.md`: ouvrir Claude Code dans `/Users/alexandrebaratta/backend-worker`, coller le prompt unique, et laisser Claude Code/Chrome configurer Upstash Redis puis vérifier les pending actions.
2. **Décider explicitement du statut de la séance Yannick.** Le compte-rendu du 2026-05-08 est un input prioritaire, mais pas une décision officielle tant qu'Alexandre ne l'a pas validé.
3. **Transformer les retours en 3 tickets maximum avant la prochaine démo:**
   - scénario de démo orienté problèmes client,
   - clarification rôles/droits et sécurité d'accès,
   - fiabilisation du flux voix sur les cas multi-chantiers / même client.
4. **Reporter le hardening large SEC-001..SEC-007 après arbitrage.** Les tickets sécurité restent importants, mais ne doivent pas écraser la préparation commerciale immédiate sans validation.

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
- `reports/backend-worker-document-status-registry.md` — statut officiel/draft/proposition de chaque document.

## Prompt opérationnel (proposition)

`Lis reports/backend-worker-claude-code-compact-checklist.md et exécute-le.`

> Ce prompt reste une proposition opérationnelle, pas une décision stratégique validée.

# Prompt Claude Code — checkup complet pré-démo N. Marti

## Message exact à envoyer à Claude Code

```txt
Tu dois faire un checkup complet pré-démo de l'application N. Marti avant la présentation de vendredi.

Contexte important:
- Ne change rien au code sans le signaler et sans validation explicite d'Alexandre, sauf si tu trouves un bug bloquant évident et que tu proposes d'abord le correctif.
- L'objectif est d'obtenir un diagnostic complet, factuel, avec preuves, pas d'improviser une nouvelle stratégie.
- La source officielle de gouvernance est `reports/backend-worker-cadrage-officiel-v1.md`.
- Les autres documents `reports/backend-worker-*` sont des références, propositions ou backlog hardening.

## 1) Lire d'abord
- `reports/backend-worker-cadrage-officiel-v1.md`
- `reports/backend-worker-document-status-registry.md`
- `reports/backend-worker-status-board-live.md`
- `reports/backend-worker-deployment-status-and-next-step.md`
- `reports/backend-worker-variants-rollout-checklist.md`
- `reports/backend-worker-sec002-audit-fixes-summary.md`
- `reports/backend-worker-render-deploy-incident-rate-limit.md`
- `reports/backend-worker-render-deploy-incident-lockfile-invalid-version.md`

## 2) Vérifications obligatoires backend
Exécute et colle les résultats:
- `npm run typecheck`
- `npm test`
- `npm run lint` (si présent)
- audit multi-tenant / SEC-002 si un script existe
- test de boot serveur local si possible

Vérifie aussi:
- package versions Fastify / @fastify/rate-limit compatibles
- package-lock sans entrée invalide sans `version`
- migrations attendues présentes / appliquées si vérifiable
- variables nécessaires documentées: Supabase, Deepgram, LLM, Resend, Redis/Upstash

## 3) Vérifications prod / Render
Depuis l'environnement disponible, teste:
- healthcheck backend: `https://nmarti-backend-worker.onrender.com/health`
- endpoint API simple non destructif si disponible
- absence de 5xx sur les endpoints nécessaires à la démo
- logs Render récents si accessibles
- dernier commit déployé / SHA si accessible

## 4) Vérifications front / N. Marti
Si tu as accès au frontend:
- ouvrir `https://app.lesprecurseurslab.ai`
- vérifier branding N. Marti
- vérifier qu'aucune donnée de démo externe ne fuite dans N. Marti
- vérifier dashboard / CRM / projets / documents / terrain
- vérifier console navigateur: pas d'erreurs bloquantes
- vérifier mobile/tablette si possible

## 5) Flux démo non négociables à tester
Teste réellement ou indique pourquoi impossible:
1. Création client/contact/projet
2. Visite multimodale: voix + photo + note + tâche
3. Edit intelligence: modifier une donnée existante + confirmation + reload
4. Documents entrants / classement si prévu en démo
5. Planning/Kanban si prévu en démo

Pour chaque flux:
- statut: OK / PARTIEL / KO / NON TESTABLE
- étapes testées
- résultat attendu vs obtenu
- preuve: fichier/ligne, log, capture, URL, ou sortie console
- risque pour la démo de vendredi

## 6) Voix / IA agentique
Vérifie spécifiquement:
- Deepgram est bien moteur primaire si configuré
- fallback voix explicite si Deepgram indisponible
- transcript imparfait => clarification plutôt qu'action dangereuse
- pas de faux succès: si DB non écrite, l'UI ne doit pas prétendre succès
- actions sensibles demandent confirmation

## 7) Redis / pending actions
Vérifie:
- Redis Upstash configuré ou non en prod
- si non configuré: confirmer fallback in-memory et impact exact pour la démo
- tester si possible: token pending single-use, expiration, comportement après restart (si non destructif)

## 8) Variantes / propagation coeur
Pour N. Marti en priorité:
- confirmer que le coeur déployé contient les correctifs récents
- confirmer que les variantes reposent bien sur coeur unique / profil / seed / branding
- ne pas conclure que toutes les variantes sont OK sans preuve

## 9) Rapport final attendu
Rends exactement ce format:

### Verdict pré-démo N. Marti
- Statut: PRÊT / PRÊT AVEC RÉSERVES / PAS PRÊT
- Raisons principales
- Risques vendredi
- Décisions nécessaires Alexandre

### Tableau checkup
| Zone | Statut | Preuves | Risque démo | Action avant vendredi |
|---|---|---|---|---|
| Backend health |  |  |  |  |
| Typecheck/tests/lint |  |  |  |  |
| Front N. Marti |  |  |  |  |
| Voix -> action |  |  |  |  |
| Création client/contact/projet |  |  |  |  |
| Visite multimodale |  |  |  |  |
| Edit intelligence |  |  |  |  |
| Documents |  |  |  |  |
| Planning/Kanban |  |  |  |  |
| Redis/pending actions |  |  |  |  |
| Sécurité tenant |  |  |  |  |

### Questions / réponses à renvoyer à Codex
Liste tout ce que Codex doit savoir pour décider de la suite:
- erreurs exactes
- logs
- captures ou URLs
- commandes exécutées
- résultats
- recommandations classées P0/P1/P2

Ne conclus pas à un GO commercial global sans validation explicite d'Alexandre. Donne seulement un statut pré-démo factuel.
```

## Utilisation

Envoyer ce prompt à Claude Code depuis le repo `backend-worker`, puis coller ici son rapport complet pour analyse et priorisation.

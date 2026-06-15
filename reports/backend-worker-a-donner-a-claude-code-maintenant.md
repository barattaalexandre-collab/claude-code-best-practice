# backend-worker — quoi faire maintenant et quoi donner à Claude Code

## Réponse directe

Tu dois donner à Claude Code **un seul objectif maintenant**: lancer le **Sprint 1 sécurité**.

Ne lui demande pas encore de corriger l'UX, les swimlanes, l'import client, le pricing ou toute l'application.

Tu lui donnes:

1. le dépôt réel `backend-worker`,
2. le prompt prêt à copier-coller ci-dessous,
3. si possible, ces documents de contexte:
   - `reports/backend-worker-sprint-1-launch.md`,
   - `reports/backend-worker-correctifs-a-faire.md`,
   - `reports/backend-worker-plan-execution-cloud-code.md`,
   - `reports/backend-worker-audit-preliminary.md`,
   - `reports/backend-worker-cadrage-officiel-v1.md`.

Si Claude Code n'a pas accès aux fichiers `reports/`, copie-colle seulement le prompt complet de ce document. Il contient déjà l'essentiel.

---

## Ce que tu fais concrètement

### 1. Ouvre Claude Code sur le repo `backend-worker`

Il faut être dans le vrai repo applicatif, pas dans ce repo de rapports.

```bash
cd /chemin/vers/backend-worker
git checkout main
git pull
git checkout -b hardening/sprint-1-security-foundations
```

### 2. Lance ou demande à Claude Code de lancer l'état initial

```bash
npm install
npm run typecheck
npm test
npm run lint
```

Si `npm run lint` n'existe pas, ce n'est pas bloquant: Claude Code doit juste le documenter.

### 3. Copie-colle le prompt ci-dessous dans Claude Code

---

## Prompt exact à donner à Claude Code maintenant

```text
Tu travailles sur le repo backend-worker.

Nous lançons uniquement le Sprint 1 sécurité.

Objectif: corriger les fondations auth / multi-tenant / rate limiting avant toute autre feature.

Important: ne corrige pas encore l'UX, les swimlanes, l'import client, le pricing, le mode démo complet, ni le chantier platform_admin complet. Ces sujets viendront après.

Tu dois traiter uniquement ces 3 sujets:

1. Auth serveur vérifiée et suppression de la confiance dans les headers client.
2. Isolation multi-tenant et garde-fous Supabase.
3. Rate limiting minimal sur /api/ai/message et routes sensibles.

Contexte sécurité:
- Le backend ne doit pas faire confiance à x-user-role, x-user-id ou x-organization-id comme source de vérité.
- Le rôle, l'utilisateur et l'organisation doivent venir d'une identité vérifiée côté serveur et/ou de la DB membership.
- Une organisation A ne doit jamais pouvoir lire ou modifier les données d'une organisation B.
- Les routes user-facing doivent être tenant-safe.
- Si la service-role Supabase est utilisée, elle doit être limitée ou entourée de garde-fous obligatoires.

Avant de modifier le code, fais un mini-audit et donne-moi un plan avec:
- les fichiers auth que tu vas inspecter,
- les routes qui utilisent x-user-role, x-user-id ou x-organization-id,
- les endroits où organization_id est utilisé,
- les usages Supabase service-role,
- les endpoints les plus risqués,
- les tests que tu vas ajouter,
- l'ordre exact des changements.

Ensuite, implémente en PRs ou commits séparés:

PR/commit 1 — Auth:
- vérifier l'identité côté serveur,
- centraliser request.user / request.organization / request.role,
- ignorer les headers client non vérifiés,
- ajouter tests JWT absent/invalide => 401,
- ajouter test header forgery refusé.

PR/commit 2 — Multi-tenant:
- imposer membership user -> organization,
- vérifier toutes les lectures/écritures sensibles,
- empêcher cross-org read/write,
- réduire ou encadrer service-role Supabase,
- ajouter tests org A ne lit/modifie pas org B.

PR/commit 3 — Rate limiting minimal:
- ajouter rate limit sur /api/ai/message,
- ajouter rate limit sur routes sensibles si pertinent,
- limiter par IP et si possible par user/org,
- ajouter tests ou preuves de 429 quand limite dépassée.

Commandes obligatoires à exécuter:
- npm run typecheck
- npm test
- npm run lint si disponible

À la fin, donne-moi un rapport clair avec:
- résumé des changements,
- fichiers modifiés,
- tests exécutés et résultats,
- preuves que les headers forgés sont refusés,
- preuves que le cross-org est refusé,
- preuves que le rate limit fonctionne,
- risques restants,
- rollback précis,
- verdict: GO ou NO-GO pour lancer Sprint 2.
```

---

## Ce que tu dois lui refuser pour l'instant

Si Claude Code propose de partir sur autre chose, tu réponds non pour l'instant.

À refuser dans Sprint 1:

- refaire toute l'interface,
- ajouter les swimlanes,
- travailler sur import client,
- changer le pricing,
- faire toute la console `platform_admin`,
- refondre tout l'assistant IA,
- faire une PR énorme avec sécurité + UX + produit mélangés.

---

## Ce que tu dois obtenir avant de passer à l'étape suivante

Tu ne passes au Sprint 2 que si Claude Code te donne:

- `npm run typecheck` OK,
- `npm test` OK,
- `npm run lint` OK ou absent documenté,
- JWT absent/invalide => 401,
- header forgery refusé,
- user hors org => 403,
- test cross-org lecture/écriture OK,
- rate limit `/api/ai/message` OK,
- rollback clair.

Si ces points ne sont pas cochés, on reste sur Sprint 1.

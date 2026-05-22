# backend-worker — lancement Sprint 1 Cloud Code

## Décision

On lance la **première étape d'exécution**: Sprint 1 sécurité minimale obligatoire.

Objectif: sécuriser les fondations avant d'empiler les corrections produit/UX.

---

## Périmètre Sprint 1

Cloud Code doit traiter uniquement ces 3 tickets:

1. **EXEC-001 — Auth serveur vérifiée et suppression trust headers**
2. **EXEC-002 — Isolation multi-tenant et garde-fous Supabase**
3. **EXEC-003 — Rate limiting minimal IA et routes sensibles**

Tout le reste est hors périmètre pour cette première étape:

- pas de refonte UX,
- pas de swimlanes,
- pas d'import client,
- pas de modèle économique,
- pas de gros chantier `platform_admin`, sauf si nécessaire pour ne pas casser l'auth.

---

## Résultat attendu à la fin du Sprint 1

À la fin, on veut pouvoir dire:

- le backend ne fait plus confiance à `x-user-role`, `x-user-id`, `x-organization-id` comme vérité,
- l'identité utilisateur est vérifiée côté serveur,
- le rôle vient d'une source serveur fiable ou de la DB membership,
- une organisation A ne peut pas lire ou modifier les données d'une organisation B,
- les routes sensibles et `/api/ai/message` ont un rate limit minimal,
- les tests de sécurité passent,
- chaque PR contient un rollback clair.

---

## Préparation dans le repo `backend-worker`

À faire avant de demander les modifications à Cloud Code:

```bash
git checkout main
git pull
git checkout -b hardening/sprint-1-security-foundations
npm install
npm run typecheck
npm test
npm run lint
```

Si `npm run lint` n'existe pas, Cloud Code doit l'indiquer et continuer avec typecheck + tests.

Si un check échoue avant modification, Cloud Code doit documenter l'état initial avant de modifier le code.

---

## Prompt exact à envoyer à Cloud Code

Copier-coller le bloc suivant dans Cloud Code depuis le dépôt `backend-worker`:

```text
Tu travailles sur le repo backend-worker.

Nous lançons Sprint 1: sécurité minimale obligatoire.

Objectif: corriger les fondations auth / multi-tenant / rate limiting avant toute autre feature.

Lis d'abord ces documents de contexte s'ils sont présents dans le repo ou fournis dans le prompt:
- reports/backend-worker-correctifs-a-faire.md
- reports/backend-worker-plan-execution-cloud-code.md
- reports/backend-worker-audit-preliminary.md
- reports/backend-worker-cadrage-officiel-v1.md
- reports/backend-worker-cloud-code-handoff.md

Tu dois traiter uniquement ces tickets:
1. EXEC-001 Auth serveur vérifiée et suppression trust headers
2. EXEC-002 Isolation multi-tenant et garde-fous Supabase
3. EXEC-003 Rate limiting minimal IA et routes sensibles

Règles strictes:
- Ne fais pas une grosse PR fourre-tout.
- Fais une PR par ticket si possible; sinon sépare clairement les commits et sections.
- Ne travaille pas sur UX, swimlanes, import, pricing, platform_admin complet ou refonte assistant dans ce sprint.
- Ajoute ou mets à jour les tests automatisés pour chaque correction critique.
- Ne fais pas confiance à x-user-role, x-user-id, x-organization-id comme source de vérité.
- Le rôle et l'organisation doivent venir d'une identité serveur vérifiée et/ou de la DB membership.
- Toute route user-facing doit être tenant-safe.
- Ajoute des tests d'attaque cross-org.
- Ajoute un rate limit minimal sur /api/ai/message et routes sensibles.

Avant de modifier le code, produis un mini-plan avec:
- fichiers que tu vas inspecter,
- fonctionnement auth actuel supposé,
- endroits où les headers client sont utilisés,
- endpoints à risque multi-tenant,
- stratégie de tests,
- ordre des changements.

Implémentation attendue:
- remplacer ou encapsuler l'auth basée headers par une auth serveur vérifiée,
- centraliser request.user / request.organization / request.role,
- supprimer ou ignorer les rôles et orgs client non vérifiés,
- imposer les contrôles membership user -> organization,
- limiter les accès Supabase service-role sur routes user-facing ou ajouter garde-fous obligatoires,
- ajouter des tests 401/403, header forgery, JWT invalide, cross-org read/write,
- ajouter rate limiting minimal sur /api/ai/message et routes sensibles.

Commandes obligatoires à exécuter:
- npm run typecheck
- npm test
- npm run lint si disponible

À la fin, donne:
- résumé des PRs/commits,
- fichiers modifiés,
- tests exécutés avec résultats,
- preuves que header forgery et cross-org sont refusés,
- risques restants,
- rollback précis,
- recommandation GO / NO-GO pour passer au Sprint 2.
```

---

## Critères d'acceptation Sprint 1

Sprint 1 est accepté seulement si:

- [ ] les checks initiaux ont été documentés,
- [ ] les headers client ne sont plus source de vérité auth/rôle/org,
- [ ] JWT invalide ou absent donne 401 sur routes protégées,
- [ ] user hors organisation donne 403,
- [ ] les tests cross-org lecture/écriture passent,
- [ ] `/api/ai/message` a un rate limit minimal,
- [ ] `npm run typecheck` passe,
- [ ] `npm test` passe,
- [ ] `npm run lint` passe ou est documenté comme absent,
- [ ] rollback documenté.

---

## Après Sprint 1

Si Sprint 1 est validé, on lance Sprint 2:

- voice-to-action multi-chantiers même client,
- confirmations / annulation-correction,
- observabilité IA minimale.

Si Sprint 1 n'est pas validé, on ne lance pas Sprint 2.

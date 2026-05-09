# backend-worker — plan d'exécution pour faire les changements

## Réponse courte

Pour faire tous les changements, il ne faut pas tout donner à Cloud Code en une seule fois.

Il faut procéder comme ceci:

1. **Valider le backlog** `backend-worker-correctifs-a-faire.md`.
2. **Choisir le niveau d'urgence**: démo rapide sécurisée ou durcissement production complet.
3. **Préparer le dépôt `backend-worker`**: branche dédiée, env local, tests qui passent avant changement.
4. **Découper en PR atomiques**: une PR = un problème = tests = rollback.
5. **Lancer Cloud Code lot par lot**, en commençant par les fondations sécurité et les cas voix critiques.
6. **Relire chaque PR avant merge**, surtout sécurité, auth, multi-tenant et IA.
7. **Faire une répétition de démo** sur données connues avant de montrer au client.

---

## Ce qu'il faut faire maintenant, concrètement

### Étape 1 — Décider ce qu'on veut livrer en premier

Avant Cloud Code, il faut répondre à ces 6 décisions:

| Décision | Option recommandée pour avancer |
|---|---|
| Accès démo V1 | magic link email ou MFA email + session courte |
| Accès production V2 | auth forte + rôles DB + isolation tenant stricte |
| Redis / Upstash | oui pour pending actions et rate limiting si multi-instance |
| Démo client | scénario court, pas visite exhaustive des menus |
| Assistant | interface simple micro/photo/note, historique replié |
| Platform admin | rôle support séparé des rôles métier client |

**Sortie attendue:** Alexandre valide ou modifie ces choix.

### Étape 2 — Préparer une branche de travail

Dans le dépôt réel `backend-worker`, créer une branche dédiée:

```bash
git checkout main
git pull
git checkout -b hardening/backend-worker-v1
```

Puis vérifier l'état initial:

```bash
npm install
npm run typecheck
npm test
npm run lint
```

Si un de ces checks échoue déjà avant changement, Cloud Code doit d'abord documenter l'échec et corriger le minimum nécessaire ou isoler le test cassé.

### Étape 3 — Créer les tickets d'exécution

Créer les tickets dans cet ordre:

1. `EXEC-001 Auth serveur vérifiée et suppression trust headers`
2. `EXEC-002 Isolation multi-tenant et garde-fous Supabase`
3. `EXEC-003 Rate limiting minimal IA et routes sensibles`
4. `EXEC-004 Fiabiliser voice-to-action multi-chantiers même client`
5. `EXEC-005 Confirmations, annulation/correction et observabilité IA minimale`
6. `EXEC-006 UX démo: carte rôles/droits`
7. `EXEC-007 UX assistant simplifiée micro/photo/note`
8. `EXEC-008 Platform admin et console support`
9. `EXEC-009 Redis pending actions single-use TTL`
10. `EXEC-010 Upload hardening et limites body/Zod`
11. `EXEC-011 Audit logs et runbooks incident`
12. `EXEC-012 Import données client V1`
13. `EXEC-013 Swimlanes / React Flow métier`
14. `EXEC-014 Coûts IA, quotas et packaging commercial`

Ne pas demander à Cloud Code de traiter les 14 tickets dans une seule PR.

---

## Ordre d'exécution recommandé

### Sprint 0 — cadrage rapide avant code

**But:** éviter que Cloud Code parte dans la mauvaise direction.

À faire:

- valider les décisions de l'étape 1,
- confirmer que le repo cible est bien accessible,
- confirmer les variables d'environnement disponibles hors secrets,
- confirmer la stack réelle: Node, Fastify/Express, Supabase, frontend, CI.

**Livrable:** une note courte `docs/execution-decisions.md` dans le repo cible ou un commentaire de ticket.

### Sprint 1 — sécurité minimale obligatoire

**Tickets:** EXEC-001, EXEC-002, EXEC-003.

**Pourquoi d'abord:** si l'identité, les rôles et l'organisation ne sont pas fiables, tout le reste peut être faux.

**Résultat attendu:**

- le backend ne fait plus confiance aux headers client pour rôle/user/org,
- l'app dérive identité et rôles côté serveur,
- les routes sensibles sont protégées,
- les tests prouvent qu'une org ne lit/modifie pas une autre,
- `/api/ai/message` et routes sensibles ont des limites anti-abus minimales.

**Checks obligatoires:**

```bash
npm run typecheck
npm test
npm run lint
```

### Sprint 2 — fiabilité voix vers action

**Tickets:** EXEC-004, EXEC-005.

**Pourquoi ensuite:** c'est le cœur de la valeur produit; le cas même client / plusieurs chantiers est critique.

**Résultat attendu:**

- l'IA distingue client, contact, chantier/projet et lieu,
- si doute, elle demande clarification,
- elle propose clairement créer un nouveau chantier ou rattacher à l'existant,
- les actions sont confirmables,
- Alexandre peut voir transcript, intention, entités, action proposée et action finale.

**Tests minimum:**

- cas `Bernard Müller / Colombier / nouveau chantier`,
- cas même client mais chantier existant,
- cas lieu ambigu => clarification,
- cas action destructive => confirmation obligatoire.

### Sprint 3 — UX démo immédiate

**Tickets:** EXEC-006, EXEC-007.

**Pourquoi:** la démo ne doit pas ressembler à une usine à gaz.

**Résultat attendu:**

- page rôles/droits claire, sans confusion avec des personnes réelles,
- assistant mis en avant,
- micro/photo/note visibles immédiatement,
- historique replié,
- scénario de démo court.

**Contrôle humain obligatoire:** Alexandre doit regarder l'UI avant merge si possible.

### Sprint 4 — support et robustesse production

**Tickets:** EXEC-008, EXEC-009, EXEC-010, EXEC-011.

**Résultat attendu:**

- vrai rôle `platform_admin`,
- console support sécurisée,
- pending actions en Redis avec TTL et single-use,
- upload photo durci,
- audit logs exploitables,
- runbooks incident.

### Sprint 5 — vente, migration et industrialisation

**Tickets:** EXEC-012, EXEC-013, EXEC-014.

**Résultat attendu:**

- procédure ou module d'import V1,
- swimlanes métier pour atelier client,
- modèle de coûts IA et quotas présentables.

---

## Prompt à envoyer à Cloud Code — Sprint 1

Copier-coller ceci dans Cloud Code après avoir ouvert le dépôt `backend-worker`:

```text
Tu travailles sur le repo backend-worker.

Objectif Sprint 1: sécurité minimale obligatoire avant toute démo sérieuse.

Lis d'abord ces documents de contexte si disponibles:
- reports/backend-worker-correctifs-a-faire.md
- reports/backend-worker-audit-preliminary.md
- reports/backend-worker-cadrage-officiel-v1.md
- reports/backend-worker-cloud-code-handoff.md

Tu dois traiter uniquement ces tickets:
1. EXEC-001 Auth serveur vérifiée et suppression trust headers
2. EXEC-002 Isolation multi-tenant et garde-fous Supabase
3. EXEC-003 Rate limiting minimal IA et routes sensibles

Règles:
- Ne fais pas une grosse PR fourre-tout.
- Fais une PR par ticket si possible.
- Ajoute ou mets à jour les tests automatisés.
- Ne fais pas confiance à x-user-role, x-user-id, x-organization-id comme source de vérité.
- Le rôle et l'organisation doivent venir d'une identité serveur vérifiée et/ou de la DB membership.
- Toute route user-facing doit être tenant-safe.
- Ajoute des tests d'attaque cross-org.
- Ajoute un rate limit minimal sur /api/ai/message et routes sensibles.

Avant de commencer, produis un mini-plan avec:
- fichiers que tu vas inspecter,
- hypothèses sur l'auth actuelle,
- risques,
- ordre des changements.

Après chaque PR, donne:
- résumé,
- fichiers modifiés,
- tests exécutés,
- risques restants,
- rollback.

Commandes obligatoires:
- npm run typecheck
- npm test
- npm run lint si disponible
```

---

## Prompt à envoyer à Cloud Code — Sprint 2

À utiliser seulement après Sprint 1:

```text
Objectif Sprint 2: fiabiliser le voice-to-action.

Traite uniquement:
1. EXEC-004 Fiabiliser voice-to-action multi-chantiers même client
2. EXEC-005 Confirmations, annulation/correction et observabilité IA minimale

Cas critique à corriger:
- Un utilisateur dit: "Nouveau chantier chez Bernard Müller à Colombier..."
- Si Bernard Müller existe déjà avec un autre chantier, l'IA ne doit pas rattacher automatiquement au mauvais chantier.
- Elle doit comparer client/contact/projet/lieu/adresse/contexte.
- Si doute: demander clarification.
- Elle doit proposer explicitement: créer un nouveau chantier ou rattacher à un chantier existant.

Ajoute tests pour:
- même client + nouveau lieu => proposition nouveau chantier ou clarification,
- même client + chantier existant clair => rattachement correct,
- doute => pas d'action automatique,
- action sensible => confirmation obligatoire,
- action IA hors tenant => refus.

Ajoute observabilité minimale:
- transcript reçu,
- intention détectée,
- entités candidates,
- action proposée,
- confirmation,
- action finale.

Commandes obligatoires:
- npm run typecheck
- npm test
- npm run lint si disponible
```

---

## Prompt à envoyer à Cloud Code — Sprint 3

À utiliser après Sprint 2 ou en parallèle si frontend séparé:

```text
Objectif Sprint 3: rendre la démo claire et non confuse.

Traite uniquement:
1. EXEC-006 UX démo: carte rôles/droits
2. EXEC-007 UX assistant simplifiée micro/photo/note

Pour la page rôles/droits:
- Ne pas afficher une liste de personnes qui fait croire "qui êtes-vous ?".
- Afficher des rôles métier: Propriétaire/CEO, Admin organisation, Manager, Terrain/Technicien, Finance, Viewer/Externe, Platform admin/Support.
- Pour chaque rôle: ce qu'il voit, ce qu'il peut modifier, ce qu'il ne peut pas faire, validations nécessaires.

Pour l'assistant:
- Mettre micro/photo/note en premier.
- Replier historique/sessions/résumés par défaut.
- Réduire le bruit visuel.
- Garder la logique métier existante.

Ajoute tests UI si la stack le permet.
Fournis captures ou description visuelle avant/après.
```

---

## Critères de validation avant démo

La démo peut être considérée prête seulement si:

- auth serveur et rôles réels OK,
- test cross-org OK,
- rate limit minimal OK,
- cas voice-to-action multi-chantiers testé OK,
- clarification en cas de doute OK,
- UX assistant simplifiée visible,
- page rôles/droits compréhensible,
- scénario de démo répété avec 3 cas maximum,
- fallback prévu si l'IA se trompe.

---

## Ce qu'il ne faut pas faire

- Ne pas demander à Cloud Code de "tout corriger" en une seule fois.
- Ne pas merger une PR sans tests.
- Ne pas lancer une démo avec un cas IA non répété.
- Ne pas mélanger `platform_admin` avec les rôles client.
- Ne pas repousser l'isolation multi-tenant si la démo utilise de vraies données.
- Ne pas présenter le PIN seul comme sécurité production.

---

## Décision pratique proposée

Si on veut avancer vite:

1. Valider les 6 décisions de l'étape 1.
2. Envoyer le prompt Sprint 1 à Cloud Code.
3. Faire relire les PR Sprint 1.
4. Envoyer le prompt Sprint 2.
5. Faire une répétition interne de démo.
6. Envoyer le prompt Sprint 3 si l'UX reste confuse.
7. Garder les sprints 4 et 5 pour consolidation production/commerciale.

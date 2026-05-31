# backend-worker — liste explicite des correctifs à faire

## Objectif de ce document

Ce document répond à la question: **"qu'est-ce qu'on doit corriger concrètement dans l'application avant de relancer Cloud Code ?"**

Il consolide:

- le cadrage officiel V1,
- l'audit sécurité préliminaire,
- les retours de séance Yannick du 2026-05-08,
- les sujets déjà préparés dans les tickets SEC-001 à SEC-007,
- les besoins produit / vente / démo remontés oralement.

Ce n'est pas un nouveau cadrage stratégique. C'est une **liste de travail explicite à valider point par point** avant d'envoyer à Cloud Code.

---

## Résumé très simple

À faire, dans l'ordre:

1. **Sécuriser l'accès réel**: plus de rôles ou organisations envoyés par le client comme vérité.
2. **Clarifier les rôles et droits**: remplacer la page confuse de sélection de personnes par une vraie carte des rôles.
3. **Fiabiliser la voix vers action**: surtout le cas critique même client / plusieurs chantiers / nouveau lieu.
4. **Simplifier l'UX assistant**: micro, photo, note en premier; historique et bruit visuel repliés.
5. **Préparer une démo orientée problèmes client**: ne pas faire une visite de tous les menus.
6. **Ajouter une vue support / platform admin**: voir ce que l'IA a compris et pourquoi elle propose une action.
7. **Prévoir migration/import client**: sinon le prospect dira qu'il doit maintenir deux systèmes.
8. **Mettre des limites anti-abus et coûts IA**: rate limits, quotas, logs.
9. **Durcir uploads et actions IA**: images, prompts, confirmations, audit logs.
10. **Décider ce qui est V1 démo et ce qui est V2 production** avant de lancer Cloud Code.

---

## A. Correctifs bloquants sécurité / accès

### A1 — Remplacer l'auth basée sur headers client par une auth serveur vérifiée

**Problème:** si l'application fait confiance à `x-user-role`, `x-user-id` ou `x-organization-id` envoyés par le client, un utilisateur peut potentiellement se faire passer pour owner/admin ou changer d'organisation.

**Correctif attendu:**

- vérifier un JWT côté serveur,
- dériver `user_id`, `organization_id` et `role` depuis l'identité vérifiée et la base,
- ignorer les rôles ou organisations envoyés librement par le frontend,
- centraliser le contrôle d'appartenance `user -> organization` dans un middleware.

**Priorité:** P0 sécurité.

**Cloud Code:** oui, en premier.

### A2 — Clarifier le standard d'accès V1 démo et V2 production

**Problème:** le PIN seul n'est pas assez rassurant pour une app contenant des données sensibles.

**Correctif attendu:**

- décider ce qui est acceptable pour la démo V1: magic link email, MFA email, session courte, ou autre,
- décider ce qui sera obligatoire en V2 production,
- ajouter une durée de session et auto-déconnexion,
- retirer ou encadrer tout rôle mock en production.

**Priorité:** P0 pour la confiance client, P1 technique selon choix.

**Cloud Code:** seulement après décision du standard.

### A3 — Réduire l'usage de la clé Supabase service-role sur les routes utilisateur

**Problème:** la service-role contourne RLS. Si un filtre `organization_id` manque quelque part, risque de fuite cross-tenant.

**Correctif attendu:**

- éviter service-role pour les routes user-facing,
- utiliser RLS et identité utilisateur quand possible,
- si service-role indispensable: garde-fou centralisé + tests d'isolation obligatoires.

**Priorité:** P0 sécurité.

**Cloud Code:** oui, après A1 ou en même lot si le dépôt est prêt.

### A4 — Tests automatiques d'isolation multi-tenant

**Problème:** sans tests d'attaque, on ne prouve pas qu'une organisation ne peut pas lire ou modifier les données d'une autre.

**Correctif attendu:**

- tests HTTP: user org A ne lit pas org B,
- tests mutations: user org A ne modifie pas org B,
- tests IA: une action IA ne peut pas agir hors organisation,
- tests rôle: un viewer ne peut pas faire une action admin.

**Priorité:** P0/P1.

**Cloud Code:** oui, dans chaque PR de sécurité.

---

## B. Correctifs IA / voix / actions métier

### B1 — Corriger le cas critique même client / plusieurs chantiers / nouveau lieu

**Problème:** l'IA transcrit correctement, mais peut rattacher une demande à un mauvais chantier existant au lieu de comprendre qu'il s'agit d'un nouveau chantier ou d'un autre lieu.

**Correctif attendu:**

- distinguer clairement client, contact, projet/chantier et lieu,
- ne jamais fusionner automatiquement si le lieu ou contexte ne correspond pas,
- comparer adresse, commune, nom de chantier, historique et statut,
- demander clarification en cas de doute,
- proposer explicitement: `Créer un nouveau chantier` ou `Rattacher au chantier existant`.

**Priorité:** P0 produit.

**Cloud Code:** oui, juste après les décisions sécurité minimales.

### B2 — Rendre les actions IA confirmables, traçables et annulables

**Problème:** si l'IA peut modifier la base, il faut savoir ce qu'elle va faire, qui confirme, et pouvoir annuler ou corriger.

**Correctif attendu:**

- avant toute modification: afficher un résumé clair de l'action proposée,
- confirmation explicite utilisateur,
- journaliser transcript, intention, entités, action proposée, action confirmée,
- prévoir annulation ou correction selon les droits,
- ne pas exécuter d'action destructive sans confirmation forte.

**Priorité:** P0/P1.

**Cloud Code:** oui.

### B3 — Remplacer `pendingActionsMap` mémoire par un stockage durable court terme

**Problème:** un stockage en mémoire casse au redémarrage, ne marche pas bien en multi-instance et rend les confirmations fragiles.

**Correctif attendu:**

- stocker les actions pendantes dans Redis ou équivalent,
- TTL court,
- token single-use,
- liaison à `user_id`, `organization_id`, `session_id`, action et horodatage,
- invalidation après consommation.

**Priorité:** P1 technique, P0 si multi-instance ou démo sensible.

**Cloud Code:** oui après validation Upstash/Redis.

### B4 — Protéger le LLM contre prompt injection et actions non autorisées

**Problème:** du contenu utilisateur peut contenir des instructions qui ne doivent pas devenir des ordres système.

**Correctif attendu:**

- séparer données utilisateur et instructions système,
- imposer les règles d'autorisation côté tool/backend, pas dans le prompt seulement,
- allowlist des actions et champs modifiables,
- refus automatique des actions hors droits,
- tests avec prompts malveillants.

**Priorité:** P1 sécurité IA.

**Cloud Code:** oui.

---

## C. Correctifs UX / produit pour la démo

### C1 — Remplacer la page confuse personnes/rôles par une carte des rôles et droits

**Problème:** la page actuelle peut donner l'impression qu'on demande "qui êtes-vous ?" ou qu'on affiche des personnes réelles/fictives de façon arbitraire.

**Correctif attendu:**

- montrer des rôles métier, pas des personnes,
- rôles minimum: propriétaire/CEO, admin organisation, manager, terrain/technicien, finance, viewer/externe, platform admin/support,
- pour chaque rôle: ce qu'il voit, ce qu'il peut modifier, ce qu'il ne peut pas faire, quelles validations sont nécessaires.

**Priorité:** P0 démo/confiance.

**Cloud Code:** oui, ticket frontend isolé.

### C2 — Simplifier l'assistant IA

**Problème:** trop d'historique, sessions, dictées et résumés visibles donnent une impression d'usine à gaz.

**Correctif attendu:**

- interface principale avec gros bouton micro,
- bouton photo,
- bouton note,
- historique replié dans un onglet secondaire,
- menus latéraux repliés par défaut pendant la démo,
- renommer éventuellement "Assistant IA" avec un nom plus métier/commercial.

**Priorité:** P0 démo.

**Cloud Code:** oui, ticket frontend isolé.

### C3 — Revoir le scénario de démonstration

**Problème:** montrer tous les menus perd le prospect.

**Correctif attendu:**

- commencer par les problèmes du client,
- montrer dashboard/analytics et vision d'ensemble,
- montrer le flux métier et demander au client de corriger le processus,
- montrer l'assistant voix seulement après avoir créé le besoin,
- ne tester en direct que des cas répétés et fiables.

**Priorité:** P0 vente, pas forcément code.

**Cloud Code:** non, sauf si besoin de créer un mode démo guidé.

### C4 — Ajouter swimlanes / React Flow pour visualiser les flux métier

**Problème:** le client doit voir qu'on comprend son processus réel, pas seulement une liste d'écrans.

**Correctif attendu:**

- vues flux pour devis, chantier, facturation, réserve, commande fournisseur, visite terrain, assistant IA,
- étapes, acteurs, validations, points de blocage,
- possibilité d'adapter le flux pendant l'atelier client.

**Priorité:** P1 vente/produit, P0 si la démo dépend de cette compréhension.

**Cloud Code:** oui, mais après C1/C2/B1.

---

## D. Correctifs support / observabilité / admin

### D1 — Créer un vrai accès `platform_admin`

**Problème:** Alexandre doit pouvoir diagnostiquer en direct ce que l'application et l'IA font.

**Correctif attendu:**

- compte ou rôle `platform_admin` réel,
- accès sécurisé,
- vue support séparée des rôles client,
- interdiction de mélanger ce rôle avec les rôles métier du client.

**Priorité:** P0 support démo.

**Cloud Code:** oui, mais dépend de A1/A2.

### D2 — Ajouter une console d'observabilité IA

**Problème:** quand l'IA se trompe, il faut voir pourquoi.

**Correctif attendu:**

- transcript reçu,
- intention détectée,
- entités candidates,
- chantier/projet choisi,
- score ou raison du choix si disponible,
- action proposée,
- confirmation utilisateur,
- action finale en base,
- erreurs et refus.

**Priorité:** P0/P1 pour debug et confiance.

**Cloud Code:** oui.

### D3 — Audit logs exploitables

**Problème:** il faut savoir qui a demandé quoi, qui a validé quoi, et ce qui a été écrit en base.

**Correctif attendu:**

- journaliser les actions sensibles,
- inclure user, org, rôle, route, action, cible, timestamp,
- ne pas stocker de secrets,
- pouvoir filtrer par client/projet/session.

**Priorité:** P1.

**Cloud Code:** oui.

---

## E. Correctifs migration / données client

### E1 — Préparer une stratégie d'import des données existantes

**Problème:** objection attendue: "je vais devoir garder mon ancien système et remplir le vôtre en plus".

**Correctif attendu:**

- processus d'import V1 même semi-manuel,
- collecte fichiers client,
- mapping champs,
- import clients, contacts, projets/chantiers, catalogues, documents si possible,
- validation qualité avec le client,
- rapport d'import.

**Priorité:** P0 commercial, P1 technique.

**Cloud Code:** oui si on crée un script/importer; sinon procédure manuelle d'abord.

### E2 — Clarifier les données de démo et les variantes métier

**Problème:** les variantes architecte/ingénieur/bâtiment/garage doivent partager le cœur sans diverger n'importe comment.

**Correctif attendu:**

- seed data propres par verticale,
- wording adapté,
- profils de démo contrôlés,
- pas de duplication incontrôlée du cœur applicatif.

**Priorité:** P1.

**Cloud Code:** oui après stabilisation V1.

---

## F. Correctifs coûts, limites et robustesse infra

### F1 — Rate limiting sur `/api/ai/message` et routes sensibles

**Problème:** sans limite, risque de coûts LLM, spam, brute force, déni de service.

**Correctif attendu:**

- limite par IP,
- limite par user,
- limite par organisation,
- quotas journaliers,
- messages d'erreur propres,
- logs et alertes si dépassement.

**Priorité:** P1, P0 si démo publique.

**Cloud Code:** oui.

### F2 — Durcir upload photo / `photoBase64`

**Problème:** contrôler seulement la taille ne suffit pas.

**Correctif attendu:**

- taille stricte au niveau body parser et validation métier,
- vérifier type MIME réel et magic bytes,
- dimensions max,
- stripping metadata si nécessaire,
- timeout de décodage,
- rejet propre des fichiers invalides.

**Priorité:** P1.

**Cloud Code:** oui.

### F3 — Aligner les limites body parser et Zod

**Problème:** si Express/body parser accepte 12MB mais Zod n'accepte que 1.5MB, le serveur consomme trop avant rejet.

**Correctif attendu:**

- même ordre de grandeur entre parser et validation,
- rejet tôt,
- tests payload trop gros.

**Priorité:** P1.

**Cloud Code:** oui.

### F4 — Smoke tests post-déploiement

**Problème:** il faut savoir rapidement si le déploiement est cassé.

**Correctif attendu:**

- `/health`, `/ready`, routes auth de base,
- endpoint protégé retourne 401 sans auth,
- endpoint protégé fonctionne avec auth valide,
- smoke tests bloquants en CI/CD si possible.

**Priorité:** P1 ops.

**Cloud Code:** oui.

---

## G. Correctifs business / vente / packaging

### G1 — Clarifier le modèle économique API/LLM

**Problème:** le client peut demander qui paie la consommation IA et comment elle est plafonnée.

**Correctif attendu:**

- expliquer coûts inclus / non inclus,
- quotas par offre,
- dépassements,
- garde-fous de consommation,
- visibilité admin sur usage.

**Priorité:** P0 vente.

**Cloud Code:** partiellement: usage dashboard plus tard; décision business d'abord.

### G2 — Transformer la vente en atelier de coproduction

**Problème:** si on impose un produit figé, le prospect va comparer aux habitudes existantes et aux manques.

**Correctif attendu:**

- présenter l'app comme base adaptable,
- demander au client de corriger le flux,
- noter les écarts métier,
- conclure avec un plan de reprise données + pilote.

**Priorité:** P0 vente.

**Cloud Code:** non, sauf support UI pour flux.

### G3 — Préparer une checklist de démo courte

**Problème:** il ne faut pas improviser un cas IA risqué devant le prospect.

**Correctif attendu:**

- 3 cas de démo maximum,
- données connues,
- scripts de phrases testées,
- fallback si IA échoue,
- ordre de présentation validé.

**Priorité:** P0 vente.

**Cloud Code:** non.

---

## Ordre recommandé des lots à envoyer à Cloud Code

### Lot 0 — Validation humaine avant Cloud Code

À valider ensemble avant exécution:

1. standard d'accès V1 démo,
2. standard d'accès V2 production,
3. priorité exacte entre sécurité stricte et urgence démo,
4. nom et forme de l'assistant,
5. périmètre de la vue `platform_admin`,
6. choix Redis/Upstash pour actions pendantes et rate limits.

### Lot 1 — Sécurité minimale non négociable

- A1 auth serveur vérifiée,
- A3 réduction service-role / garde-fous,
- A4 tests isolation multi-tenant,
- F1 rate limiting minimal.

### Lot 2 — Fiabilité voice-to-action

- B1 multi-chantiers même client,
- B2 confirmations et annulation/correction,
- D2 observabilité IA minimale.

### Lot 3 — UX démo

- C1 carte rôles/droits,
- C2 assistant simplifié,
- C3 mode ou script de démo si besoin.

### Lot 4 — Support et robustesse

- D1 platform admin,
- D3 audit logs,
- B3 Redis pending actions,
- B4 prompt injection hardening,
- F2/F3 uploads et body limits.

### Lot 5 — Vente / migration / industrialisation

- E1 import données,
- C4 swimlanes React Flow,
- G1 coûts IA,
- E2 variantes métier propres.

---

## Décision proposée

Avant de lancer Cloud Code, il faut valider cette liste comme backlog de correction.

Proposition concrète:

1. On valide ou retire chaque point A à G.
2. On transforme les points validés en tickets Cloud Code atomiques.
3. On lance Cloud Code d'abord sur **Lot 1**, puis **Lot 2**, puis **Lot 3**.
4. On garde les lots 4 et 5 pour consolidation après démo ou juste avant production selon urgence.

## Document d'exécution associé

Pour passer de cette liste de correctifs à l'exécution Cloud Code, utiliser `reports/backend-worker-plan-execution-cloud-code.md`. Ce document donne l'ordre des sprints, les tickets EXEC-001..014 et les prompts prêts à copier-coller.

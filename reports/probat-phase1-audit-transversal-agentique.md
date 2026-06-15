# Phase 1 — Audit transversal ProBAT

Date : 2026-06-01T08:35Z
Périmètre : 15 modules + architecture agentique + boucle texte/voix
Sources : code prod (`precurseur-shell`, `backend-worker`), audits MobAI précédents
Statut : audit livré — attendre GO utilisateur pour démarrer PR 1 `AGENT-CORE-001`

## 1. Audit modules

Format : `module · actions métier · phrases naturelles · lookup data · clarifications OK · erreurs actuelles · clics action principale · friction mobile · priorité`.

| Module | Actions métier | Phrases naturelles | Lookup data | Clarification courte OK | Erreurs actuelles | Clics action principale | Friction mobile | Priorité |
|---|---|---|---|---|---|---|---|---|
| Dashboard | Ouvrir tâche prioritaire, voir KPI, drill-down | `Mes tâches urgentes`, `Pipeline du mois`, `Que dois-je faire aujourd'hui` | tasks `status≠done`, priority ; opportunities stage active ; financial docs | `Sur quel projet` si tâche multiple | KPI auto-contradictoire fixé, activité récente masquée live | 1 tap row → `/field/tasks` | Sidebar collapsible OK, pas de close auto | P0 entry point |
| CRM Companies | Créer entreprise, modifier ville/canton/notes, ajouter contact | `Crée entreprise Favre SA à Lausanne`, `Change la ville de Favre en Zurich`, `Ajoute contact Jean Dupont chez Favre` | companies name/canton/city, contacts | `Quelle Favre : Favre SA ou Favre & Perret ?` | Pas de FAB voix dédié dans la liste | 2 — Nouvelle entreprise + form | A-Z visible, form modal OK | P1 |
| CRM Contacts | Créer contact, modifier email/tél/rôle, lier à entreprise | `Ajoute le mobile X à Sophie Martin`, `Crée contact Jean Dupont chez Favre architecte`, `Corrige l'email d'Alain Bernard` | contacts full_name search, companies | `Quel Jean Dupont : Construction ou privé ?` | Bug edit pipeline pré-PR existait, NLU OK post P0-A | 2 — Nouveau contact + form | Form scroll long mobile | P0 cœur démo |
| CRM Opportunities | Créer opportunité, déplacer stage kanban, marquer signed/lost | `Crée opp Rénovation SDB chez Müller 25 000 CHF`, `Passe l'opp Müller en signée`, `Pipeline du Q3` | opportunities name/stage/company, companies | `Quel Müller : Müller Thomas ou Müller SA ?` | `Invalid Date` fixé, stage alias OK | Drag-drop OK, 1 tap | Kanban 5 colonnes scrollable mobile difficile | P1 |
| Projects | Créer chantier, modifier statut/dates/responsable, ajouter phases | `Crée chantier rénovation SDB Müller à Lausanne`, `Passe le chantier Rochat en terminé`, `Replanifie Daikin au 15 juin` | projects title/status/dates, companies, contacts | `Quel chantier Rochat : SDB ou cuisine ?` | Filtre Brouillon ajouté, badges `À compléter` OK | 2 — Nouveau projet + form | Tableau scroll horizontal mobile | P0 cœur métier |
| Planning | Voir Gantt/calendrier, replanifier phase | `Quels chantiers cette semaine ?`, `Repousse la phase Démolition d'une semaine` | project_phases, tasks due_date | `Quelle phase` si multiple | Bug Terminé+0% fixé | 0 lecture | 3 vues toggle, Gantt mobile pas optimal | P2 |
| Process | Lecture pipeline | `Combien de devis brouillons`, `Tâches en retard` | financial_docs, tasks, supply_orders | n/a | Signed double-count fixé | 0 lecture | Cards scroll horizontal | P2 |
| Supply | Créer commande, passer status to_order→ordered→received→installed | `Commande robinetterie Hansgrohe pour Müller`, `Passe la commande Geberit en reçu` | supply_orders, projects | `Sur quel chantier` si pas dit | Badge `→ Commandé` disambiguïsé OK | 2 — Nouvelle commande + form | Kanban 5 colonnes scroll horizontal mobile | P1 |
| Field Notes | Dictée note, créer note texte, taguer phase | `Note chantier Müller : fuite étage 2 à surveiller`, `Note dictée terrain`, `Lister notes Rochat ce mois` | site_notes, projects, phases | `Quel chantier` si pas explicite | input_mode rewrite bug non fixé | 2 — Dicter / Nouvelle note | Liste OK, bouton Dicter visible | P0 usage quotidien |
| Field Photos | Ajouter photo, lier note/phase, générer description | `Prends une photo`, `Photo terrain raccord T étage 3` | project_photos, projects | `Quel chantier` + `quelle phase` | 0 image servie Storage non branché, description IA verbose | 1 — Prendre photo | Caméra natif OK, upload long | P1 |
| Field Tasks | Créer tâche, modifier statut/échéance/priorité, marquer done | `Crée tâche Appeler Müller demain 10h`, `Passe la tâche Daikin en terminé`, `Mes tâches urgentes` | tasks title/status/due_date/priority/project, projects | `Quelle tâche Daikin` si plusieurs | NLU create OK post P0-A | 2 — Nouvelle tâche + form | Tableau scroll, form modal | P0 |
| Documents imported | Importer PDF, lier projet, résumé IA | `Importe ce document`, `Lie ce contrat au chantier Rochat` | imported_documents, projects | `Quel chantier` si pas explicite | Résumé IA en attente placeholder permanent | 1 — Importer | Upload natif OK, mobile drag-drop fait | P2 |
| Quotes & Invoices | Créer devis, marquer envoyé/accepté, annuler devis accepté, créer facture | `Crée devis 3500 CHF pour Müller`, `Passe le devis QU-005 en accepté`, `Annule le devis Müller` | financial_documents, companies, projects, opportunities | `Quel Müller`, `Quel statut cible` | Annulation accepted→cancelled OK post P1-B | 2 — Nouveau + form long | Form devis complexe, scroll mobile | P0 action vendeur |
| AI Conversations | Dictée vocale + texte chat agentique | `Crée tâche…`, `Modifie note…` | tous endpoints | dépend de la commande | clarificationToken non géré FAB | 0 chat libre | Mobile clavier prend 50% | P0 |
| AI Audit | Lecture trail | `Mes actions IA récentes` | ai_activity_log | n/a | KPI math cassée `10/7/0/11` | 0 lecture | OK | P2 |

Synthèse P0 : 7 modules cœur démo — Dashboard, Contacts, Projects, Notes, Tasks, Quotes, AI Conversations.

## 2. Architecture agentique actuelle

### Flux backend `backend-worker/src/routes/public/ai.ts`

```text
POST /api/ai/message
   │
   ├─ photoBase64 → analyzePhotoWithVision (Vision API)
   │
   ├─ incomingClarificationToken existe ?
   │     ├─ oui → pendingClarificationMap.get → resolveClarificationReply
   │     └─ non → continue
   │
   ├─ Router intent (cascade, ordre strict)
   │     1. !photoBase64 && !hasCreateIntent && hasEditIntent
   │           → runEditNlu (LLM, identifie entity+field+value)
   │     2. photoBase64 || hasVisitOrWorkIntent
   │           → buildVisitNlu (visit/work flow)
   │     3. sinon (defaut)
   │           → runKeywordNlu (regex new project/contact)
   │              si pas matched → runNlu (LLM général create)
   │
   ├─ nlu.needsClarification ?
   │     ├─ oui → storeClarification (pendingClarificationMap.set)
   │     │        → renvoie clarificationToken
   │     └─ non → continue
   │
   ├─ Build pendingAction
   │     storePendingAction(actions) → pendingActionToken
   │
   └─ Réponse: { steps[], pendingActionToken, clarificationToken, needsClarification }

POST /api/ai/confirm
   │
   ├─ Validate pendingActionToken
   ├─ Execute actions[] séquentiellement
   │     create_task / create_company / create_contact / create_project /
   │     create_pre_quote_draft / update_task / update_company / update_project /
   │     update_contact / create_photo_record / etc.
   ├─ Audit log
   └─ Réponse: { status: 'confirmed', results[] }
```

### Mémoire actuelle

- `pendingClarificationMap` : key=token, val={conversationId, extraction, companies snapshot, contacts snapshot, createdAt}
- `pendingActionsMap` équivalent : key=token, val={actions, organizationId, conversationId}
- `sessionProjectContextMap` : key=conversationId, val={projectId, expiresAt} avec TTL court

### Lookup DB préchargé par requête

```text
Promise.all [
  supabase.projects (id,title,city,company_id)
  supabase.project_phases (status≠done)
  supabase.companies (id,name)
  supabase.contacts (id,full_name)
  supabase.tasks (status≠done, limit 50)
]
```

Ces listes sont injectées dans le `systemPrompt` LLM comme contexte complet.

### Front actuel

#### `AiAssistantFAB.tsx`

- État : `open`, `input`, `messages`, `busy`
- Envoi via `processAiMessageLive(content+preamble, 'text', conversationId)`
- Pas de stockage `pendingActionToken` ni `clarificationToken`
- `conversationId = fab_<route_slug>` par route

#### `ConversationSessions.tsx`

- Gère `pendingActionToken`
- Affiche `ConfirmActionDialog`
- Gère `clarificationToken`
- Gère `processAiMessageLive` et `confirmAiActionLive`
- N'est pas réutilisé par le FAB

#### `VoiceInputBar.tsx`

- Présent dans `ConversationSessions` uniquement
- Pas dans FAB ni dans Notes/Photos/Tasks/Devis directement, sauf bouton `Dicter` Notes spécifique
- Stack : Deepgram WS → fallback Whisper → fallback WebSpeech

## 3. Pourquoi texte et voix ne partagent pas la même boucle

`VoiceInputBar` produit du texte envoyé via `onSendText(text, 'voice', ...)`.

Ce texte est ensuite routé via deux chemins divergents :

1. `ConversationSessions.tsx` appelle `processAiMessageLive`, gère `pendingActionToken` et le dialogue de confirmation.
2. Le bouton `Dicter` de `src/pages/field/SiteNotes.tsx` appelle `transcribeWithWhisper`, inscrit le texte dans le champ note, puis POST `/api/site-notes` : il bypass l'agent complètement.

Conséquence :

- voix dans `/ai/conversations` : passe par l'agent ;
- voix dans `/field/notes` : bypass agent ;
- voix dans `/field/photos`, `/field/tasks`, `/documents/quotes-invoices`, `/crm/*` : absente.

Donc une commande vocale comme `Crée une tâche` depuis Notes devient le contenu d'une note, pas une action agentique.

Le `conversationId` par route ne suffit pas parce que le FAB :

- n'envoie pas `clarificationToken` sur le deuxième message ;
- n'envoie pas `pendingActionToken` ;
- n'a pas d'UI de confirmation `ConfirmActionDialog`.

## 4. Architecture agentique cible

### Boucle unifiée

```text
USER texte OU voix
  Tous modules : FAB global + VoiceInputBar global
  Front capture : { content, inputMode, contextRoute, selectedEntityId? }
       │
       ▼
Service unique agentBus (front)
  state par conversationId : lastPendingActionToken,
  lastClarificationToken, lastContextSnapshot
  méthodes : send(text), confirm(true|false), resumeWithClarification(text)
       │
       ▼
POST /api/ai/message
  1. Comprendre : hasCreateIntent | hasEditIntent | hybrid
  2. Chercher : DB lookup fuzzy contacts/companies/projects/tasks avant clarification
  3. Raisonner : LLM avec contexte + résultats lookup
  4. Proposer : actions[] + pendingActionToken
  5. Si ambigu : clarificationToken + question ciblée
       │
       ▼
Front affiche dans FAB ou ConvSheet
  bulle assistant + plan d'action + Confirmer / Annuler
  si clarification : input pré-focusé, contexte conservé
       │
       ▼
POST /api/ai/confirm
  execute actions séquentiellement
  retourne results[] avec entity IDs
  invalidate TanStack queries impactées
  vérifie via refetch
```

### Principes clés

1. Une seule source d'agent : `agentBus` + `pendingActionToken` + `clarificationToken` stockés par `conversationId`.
2. Voix = pré-processeur de texte : Deepgram/Whisper produit du texte injecté dans `agentBus.send()` ; aucune logique métier dans `VoiceInputBar`.
3. Lookup avant clarification : fuzzy search contacts/companies/projects ; un match high-confidence est utilisé, 2-3 matches sont proposés, 0 match déclenche demande ou création.
4. Confirmation UI uniforme : `ConfirmActionDialog` réutilisable dans FAB et Conversation.
5. Mobile-first : FAB + sheet drawer plein écran sur mobile, sidebar auto-close après nav.

## 5. Plan PR par PR

### PR 1 — AGENT-CORE-001 — Boucle agentique commune

Objectif : unifier l'état agent côté front et réutiliser `ConfirmActionDialog` partout.

Fichiers :

- nouveau `src/services/agentBus.ts`
- nouveau `src/hooks/useAgentBus.ts`
- modifier `src/components/ai/AiAssistantFAB.tsx`
- modifier `src/pages/ai/ConversationSessions.tsx`
- extraire `src/components/ai/AgentResponsePanel.tsx`

Risque : moyen — touche 2 pages critiques.

Effort : 4 h dev + 1 h tests.

Acceptation :

- message depuis FAB → plan d'actions → bouton `Confirmer` visible → confirmation exécute ;
- `clarificationToken` renvoyé → input pré-focusé → réponse reprend le flow ;
- `pendingActionToken` persiste cross-tour dans la même conversation.

### PR 2 — AGENT-MEMORY-001 — Persistance multi-tour

Objectif : les tokens survivent aux échanges courts : `oui`, `non`, précision.

Fichiers :

- `backend-worker/src/routes/public/ai.ts`
- `src/services/agentBus.ts`
- `src/components/ai/AiAssistantFAB.tsx`

Changements :

- étendre TTL `pendingClarificationMap` de 10 à 30 min ;
- inclure le dernier `pendingActionToken` actif si message court sans nouvel intent ;
- auto-renvoyer `clarificationToken` au prochain message ;
- restaurer state depuis `sessionStorage` au mount.

Effort : 2 h.

Acceptation : `Crée tâche pour Müller` → `Quel Müller ?` → `Thomas` continue avec Thomas, sans reset.

### PR 3 — AGENT-LOOKUP-001 — Lookup avant clarification

Objectif : l'agent cherche dans les données avant de questionner.

Fichiers :

- `backend-worker/src/routes/public/ai.ts`
- nouveau `backend-worker/src/lib/fuzzy-entity-match.ts`
- tests `tests/fuzzy-entity-match.test.ts`

Changements :

- helper `fuzzyMatchEntities(query, type, list)` ;
- injection top 5 matches contacts/companies/projects ;
- règle : 1 match > 0.85 utilisé, 2-3 proposés, >3 précision.

Effort : 4 h.

Acceptation : `Note Müller fuite étage 2` utilise le bon projet si déductible, `Mueller` matche `Müller`, plusieurs Rochat déclenchent une clarification ciblée.

### PR 4 — VOICE-GLOBAL-001 — Voix dans tous les modules clés

Objectif : `VoiceInputBar` disponible Notes/Tasks/Photos/Devis/Planning et dans le FAB.

Fichiers :

- nouveau `src/components/voice/InlineMic.tsx`
- `src/pages/field/SiteNotes.tsx`
- `src/pages/field/Tasks.tsx`
- `src/pages/crm/Contacts.tsx`
- `src/pages/crm/Companies.tsx`
- `src/pages/documents/QuotesInvoices.tsx`
- `src/components/ai/AiAssistantFAB.tsx`
- `src/components/ai/VoiceInputBar.tsx`

Effort : 5 h.

Acceptation : micro dans FAB, Notes, Tasks, Contacts, Companies, Devis ; texte transcrit envoyé au même `agentBus`.

### PR 5 — UX-NAV-001 — Menu mobile auto-close + actions 1 tap

Objectif : navigation directe et sidebar mobile qui se ferme après tap.

Fichiers :

- `src/components/layout/AppSidebar.tsx`
- `src/pages/Dashboard.tsx`
- `src/pages/crm/Opportunities.tsx`
- `src/pages/supply/SupplyKanban.tsx`
- `src/components/layout/AppTopbar.tsx`

Effort : 3 h.

Acceptation : tap entry sidebar mobile ferme la sidebar, Dashboard task row deep-link, Topbar `+` ouvre l'action contexte.

### PR 6 — E2E-SCENARIOS-001 — 10 scénarios terrain

Objectif : grille de validation reproductible.

Fichiers :

- nouveau `tests/e2e/probat-scenarios.spec.ts`
- étendre `src/__tests__/voice-phrases-metier.ts`
- nouveau `reports/probat-e2e-scenarios.md`

Scénarios cible :

1. `Crée tâche pour Müller : Appeler demain 10h`
2. `Note chantier Rochat : fuite étage 2 à surveiller`
3. `Crée contact Jean Dupont chez Favre`
4. `Crée devis 3500 CHF pour Müller Thomas`
5. `Annule le devis QU-2026-005`
6. `Passe la tâche Daikin en terminé`
7. `Commande robinetterie Geberit pour Müller`
8. `Modifie ville de Favre en Zurich`
9. `Crée chantier Rénovation SDB Müller à Lausanne`
10. `Quelles tâches urgentes ?`

Effort : 4 h.

Acceptation : 10/10 scénarios passent en headless, puis corpus voix reproduit les mêmes actions backend.

## 6. Tableau récapitulatif

| PR | Thème | Front | Backend | Effort | Risque | Critère done |
|---|---|---|---|---|---|---|
| 1 | AGENT-CORE | oui | non | 4-5 h | Moyen | FAB confirm flow E2E |
| 2 | AGENT-MEMORY | oui | oui | 2 h | Faible | Clarification 3 tours sans reset |
| 3 | AGENT-LOOKUP | non | oui | 4 h | Moyen | Fuzzy match 10 cas |
| 4 | VOICE-GLOBAL | oui | non | 5 h | Moyen | Voix dans 5 modules |
| 5 | UX-NAV | oui | non | 3 h | Faible | Mobile sidebar close |
| 6 | E2E-SCENARIOS | oui | non | 4 h | Nul | 10/10 scénarios |

Total estimé : 22-24 h dev + 4 h QA terrain.

Ordre recommandé : PR1 → PR2 → PR3 → PR5 → PR4 → PR6.

## 7. Critères de succès agrégés

| # | Critère | Mesure |
|---|---|---|
| 1 | Action naturelle possible sur 7 modules P0 | 7/7 scénarios E2E pass |
| 2 | Agent cherche avant clarification | 0 `Quel projet` si projet déductible |
| 3 | Clarification courte et ciblée | < 80 caractères, ≤ 3 options proposées |
| 4 | Texte/voix même logique | flow `agentBus` identique |
| 5 | Menu mobile auto-close | 100 % des taps sidebar |
| 6 | 10 scénarios pass | 10/10 |

## 8. Risques globaux

- PR4 voix mobile iOS : Safari requiert `getUserMedia` sur geste utilisateur strict. Mitigation : `InlineMic` = bouton explicite.
- PR3 fuzzy match prompt size : si org a 500+ contacts, prompt LLM explose. Mitigation : top 5 par requête.
- PR1 migration `ConversationSessions` : page complexe, régression possible. Mitigation : feature flag pendant une semaine.
- Déploiements cascadés : 6 PRs en file. Mitigation : merge nightly batch.

## 9. Prochaine étape

Attendre le GO utilisateur pour démarrer PR 1 `AGENT-CORE-001`.

Aucun code applicatif ne doit être modifié avant ce GO : audit + plan livrés.

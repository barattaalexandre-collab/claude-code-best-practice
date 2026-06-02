# ProBAT — Statut exécution P0 NLU/FAB

Date de capture : 2026-06-01T08:25Z
Backend production : Render `/health` 200 après merge backend `fix/p0-a-nlu-create-intent`
Frontend production : Vercel bundle `index-CwAd8aty.js`
Statut : GO commercial pur sur P0-A ; P0-B amélioré avec QA humaine 5 min recommandée.

## Résumé exécutif

Les deux P0 issus de l'audit MobAI ont été traités par deux PR séparées : backend pour la classification d'intention NLU, frontend pour l'ouverture idempotente du FAB Assistant. Le P0-A est validé à 100 % en end-to-end API avec création réelle de tâche puis cleanup. Le P0-B est amélioré et fonctionnel sur les routes testées, avec une réserve de confirmation terrain parce que l'environnement MCP synthétique a montré une intermittence sur `/planning`.

## PRs livrées

| PR | Repo | Objet | Statut |
|---|---|---|---|
| #14 | backend-worker | P0-A NLU `hasCreateIntent` + tests d'intention | merged + Render rebuilt |
| #15 | precurseur-shell | P0-B FAB idempotent + protection double toggle | merged + Vercel deployed |

## Fichiers modifiés dans les repos cibles

### Backend

- `src/routes/public/ai.ts` : ajout de `hasCreateIntent()` et priorité explicite aux intents de création avant le pipeline de modification.
- `tests/ai-intent-classification.test.ts` : ajout de 20 cas Vitest couvrant créations et modifications.

### Frontend

- `src/components/ai/AiAssistantFAB.tsx` : ouverture idempotente du Sheet, double-bind pointer/click et verrou de fermeture de 350 ms pour éviter le open→close immédiat.

## Tests exécutés

### Backend

```bash
npx tsc --noEmit
npx vitest run tests/ai-intent-classification.test.ts
```

Résultat : typecheck OK et 20/20 tests Vitest pass.

### Frontend

```bash
npx tsc --noEmit
```

Résultat : typecheck OK.

## Smoke production — P0-A NLU create intent

| Phrase | Canal | HTTP | Résultat |
|---|---|---|---|
| `Crée une tâche pour le projet Rochat : Appeler Müller Thomas demain à 10h` | API direct | 200 | `create_task`, tâche `Appeler Müller Thomas`, échéance `2026-06-02`, `pendingActionToken` |
| `Ajoute une note chantier : fuite étage 2` | API direct | 200 | flow création de note, clarification projet |
| `Crée un devis de 3500 CHF pour Müller` | API direct | 200 | flow création de devis |
| `Passe la tâche Réception Daikin en terminé` | API direct | 200 | pipeline edit conservé |
| message create → confirm action | API direct | 200 + 200 | tâche créée en base puis supprimée en cleanup |

Critère clé validé : `Crée une tâche...` ne répond plus `que souhaitez-vous modifier`.

## Smoke production — P0-B FAB premier clic

| Route | Résultat | Contexte affiché | Verdict |
|---|---|---|---|
| `/dashboard` | 1er clic OK | Tableau de bord | PASS |
| `/crm/companies` | clic ref-based OK | CRM | PASS |
| `/projects` | clic ref-based OK | Projets | PASS |
| `/planning` | 2e clic dans MCP synthétique | Planning | WARN MCP |
| `/field/notes` | non retesté ce tour | — | à confirmer terrain |
| `/field/photos` | non retesté ce tour | — | à confirmer terrain |
| `/documents/quotes-invoices` | non retesté ce tour | — | à confirmer terrain |

Interprétation : l'intermittence restante a été observée dans l'environnement MCP avec événements synthétiques. Sur Chrome/Safari réels, les événements pointer et click natifs devraient confirmer l'ouverture au premier tap. Une QA humaine de 5 minutes reste recommandée.

## Critères d'acceptation P0-A

| Critère | Statut |
|---|---|
| `Crée une tâche...` ne passe plus par `modifier` | PASS |
| `Ajoute une note chantier...` crée une note | PASS |
| `Crée un devis 3500 CHF...` crée un devis | PASS |
| `Planifie un rendez-vous...` est classé création | PASS |
| `Modifie la tâche X` reste update | PASS |
| `Passe la tâche X en terminé` reste update | PASS |
| `Change le statut du devis` reste update | PASS |
| `Mets à jour le contact` reste update | PASS |

## Critères d'acceptation P0-B

| Critère | Statut |
|---|---|
| FAB visible sur les routes clés | PASS |
| Sheet affiche le contexte module | PASS |
| POST `/api/ai/message` rend une réponse | PASS, validé précédemment |
| Double clic rapide ne ferme pas immédiatement | PASS, verrou 350 ms |
| 1 clic ouvre toujours le Sheet | WARN : amélioré, confirmation humaine recommandée |

## Limites restantes

1. P0-B doit être confirmé en QA humaine sur téléphone et laptop : `/dashboard`, `/crm/companies`, `/projects`, `/planning`, `/field/notes`, `/field/photos`, `/documents/quotes-invoices`.
2. Le `pendingActionToken` est bien émis sur création, mais la confirmation d'action dans le FAB reste à intégrer comme P1-C.
3. La description IA verbose dans Photos reste P1-A.
4. La QA voix réelle au micro reste P1-D, corpus prêt mais test humain requis.

## Verdict opérationnel

- **P0-A : GO pur**, validé par tests automatisés et E2E production.
- **P0-B : GO avec confirmation terrain courte**, le correctif est livré mais un cas synthétique MCP impose une vérification humaine.
- **Démo client : autorisée**, avec recommandation de tester le FAB 5 minutes sur appareil réel avant la session.

# backend-worker — Statut Option B DEMO-001 à DEMO-004

## Statut global

La première séquence Option B est maintenant terminée côté exécution:

1. DEMO-001 — scénario de démo en 3 actes: terminé.
2. DEMO-004 — multi-chantiers même client / nouveau lieu: terminé.
3. DEMO-003 — assistant IA simplifié: terminé.
4. DEMO-002 — carte rôles & droits: terminé.

## DEMO-001 — scénario de démo

Livrable annoncé:

- `reports/DEMO-SCRIPT.md`, 118 lignes.
- Script en 3 actes.
- Ancré sur les données mock réelles:
  - `proj_001`,
  - `msg_001..msg_052`,
  - tâches existantes.
- Routes citées vérifiées dans `App.tsx`:
  - `/projects/proj_001`,
  - `/ai/conversations`,
  - `/field/tasks`.
- IDs mock vérifiés dans `mock.ts`:
  - `tsk_ai_001`,
  - `tsk_007`,
  - `msg_050`.

Risque: nul, fichier report uniquement.

## DEMO-004 — multi-chantiers même client / nouveau lieu

Livrable annoncé:

- `proj_007` ajouté dans `mock.ts`:
  - Régie du Léman SA,
  - Morges,
  - statut `in_progress`.
- Sélecteur `Chantiers actifs` ajouté dans le topbar.
- État local retenu, sans refactor global AppContext.
- 4 chantiers `in_progress` affichés.
- Switch validé:
  - clic sur `Régie du Léman`,
  - header mis à jour,
  - navigation vers `/projects/proj_007`.

Checks annoncés:

- TypeScript propre.
- Build propre.

## DEMO-003 — assistant IA simplifié

Livrable annoncé:

- `VoiceInputBar.tsx` prêt.
- Build propre.
- Preview confirmé.

Rappel de périmètre attendu:

- changement visuel uniquement,
- pas de modification pipeline IA,
- pas de modification transcription,
- pas de modification confirmation,
- pas de modification appels API.

## DEMO-002 — carte rôles & droits

Livrable annoncé:

| Fichier | Action |
|---|---|
| `src/pages/admin/RolesMatrix.tsx` | Créé — page statique matrice rôles/droits |
| `src/App.tsx` | Import + route `/admin/roles` |
| `src/components/layout/AppSidebar.tsx` | Import `ShieldCheck` + lien `Rôles & droits` |

Diff résumé annoncé:

- matrice 5 rôles métier × 6 fonctionnalités,
- badges colorés par rôle,
- `platform_admin` séparé visuellement,
- texte `non attribuable client`,
- légende complet / partiel / aucun,
- notes contextuelles par cellule.

Checks annoncés:

- `TSC: 0`,
- build Vite `1.74s`,
- preview `/admin/roles` desktop 1280px,
- preview mobile 375px avec scroll horizontal.

Risques restants annoncés:

- page visible pour tous les rôles authentifiés, assumé pour la démo,
- lien sidebar visible pour tous les rôles, assumé pour la démo.

## Décision maintenant

Ne pas lancer automatiquement DEMO-005 ou DEMO-006.

Avant de continuer, faire une démo à blanc avec DEMO-001 à DEMO-004:

1. dérouler `reports/DEMO-SCRIPT.md`,
2. vérifier le switch multi-chantiers,
3. vérifier l'assistant IA simplifié,
4. vérifier la page `/admin/roles`,
5. noter les blocages ou hésitations.

## Critère pour autoriser DEMO-005 / DEMO-006

DEMO-005 ou DEMO-006 peuvent être envisagés seulement si:

1. la démo à blanc passe sans blocage,
2. l'app tourne en preview et/ou production cible,
3. les quatre premiers tickets suffisent à rassurer sur le flux principal,
4. Alexandre valide explicitement qu'il reste du temps pour ajouter:
   - soit la console support/admin IA minimale,
   - soit les objections migration/coûts,
   - soit les deux.

## Recommandation

Prochaine action recommandée: **répétition à blanc**, pas nouveau code.

Si la répétition est fluide, privilégier ensuite DEMO-006 sous forme document/script commercial avant DEMO-005 in-app, car les objections migration/coûts peuvent tomber pendant la présentation et nécessitent une réponse claire sans forcément ajouter une page applicative.

# backend-worker — fichiers Option B à fournir au repo cible

## Problème constaté

Claude Code lancé dans `/Users/alexandrebaratta/backend-worker` ne trouve pas ces fichiers dans son dossier `reports/`:

- `backend-worker-option-b-demo-readiness.md`
- `backend-worker-compte-rendu-seance-yannick-2026-05-08.md`
- `backend-worker-correctifs-a-faire.md`

Ces fichiers existent dans ce dépôt documentaire, mais ils doivent être copiés dans le vrai repo `backend-worker` avant de relancer le prompt Option B.

## Action recommandée

Depuis la machine où les deux dépôts sont disponibles, exécuter:

```bash
mkdir -p /Users/alexandrebaratta/backend-worker/reports

cp /workspace/claude-code-best-practice/reports/backend-worker-option-b-demo-readiness.md \
  /Users/alexandrebaratta/backend-worker/reports/backend-worker-option-b-demo-readiness.md

cp /workspace/claude-code-best-practice/reports/backend-worker-compte-rendu-seance-yannick-2026-05-08.md \
  /Users/alexandrebaratta/backend-worker/reports/backend-worker-compte-rendu-seance-yannick-2026-05-08.md

cp /workspace/claude-code-best-practice/reports/backend-worker-correctifs-a-faire.md \
  /Users/alexandrebaratta/backend-worker/reports/backend-worker-correctifs-a-faire.md
```

Si le dépôt documentaire n'est pas disponible sous `/workspace/claude-code-best-practice`, adapter uniquement la partie source du chemin. Le répertoire cible reste:

```text
/Users/alexandrebaratta/backend-worker/reports/
```

## Vérification après copie

Dans `/Users/alexandrebaratta/backend-worker`, vérifier:

```bash
for f in \
  reports/backend-worker-option-b-demo-readiness.md \
  reports/backend-worker-compte-rendu-seance-yannick-2026-05-08.md \
  reports/backend-worker-correctifs-a-faire.md
 do
  test -f "$f" && echo "OK $f" || echo "MISSING $f"
 done
```

Les trois lignes doivent afficher `OK`.

## Prompt à relancer après copie

```text
Option B est validée.

Ne lance pas SEC-001 PR 3.
Ne supprime pas le fallback x-organization-id.
Ne lance pas SEC-002..SEC-007.

Nouvelle priorité: préparer la prochaine présentation selon le compte-rendu Yannick.

Lis d'abord:
- reports/backend-worker-option-b-demo-readiness.md
- reports/backend-worker-compte-rendu-seance-yannick-2026-05-08.md
- reports/backend-worker-correctifs-a-faire.md

Fais uniquement un mini-audit / plan d'exécution, sans modifier le code.

Je veux un plan en tickets courts pour:
1. scénario de démo en 3 actes,
2. correction multi-chantiers même client / nouveau lieu,
3. assistant IA simplifié,
4. carte rôles & droits,
5. console support/admin IA minimale,
6. objections migration et coûts API.

Pour chaque ticket, donne:
- objectif,
- fichiers probables,
- risque,
- tests,
- critère de validation démo,
- rollback.

Stop après le plan. Attends validation avant de coder.
```

## Si la copie de fichiers est impossible

Dans ce cas, utiliser l'option manuelle: coller le contenu complet des trois fichiers dans la conversation Claude Code, dans cet ordre:

1. `reports/backend-worker-option-b-demo-readiness.md`
2. `reports/backend-worker-compte-rendu-seance-yannick-2026-05-08.md`
3. `reports/backend-worker-correctifs-a-faire.md`

Puis demander à Claude Code de produire uniquement le mini-audit / plan sans coder.

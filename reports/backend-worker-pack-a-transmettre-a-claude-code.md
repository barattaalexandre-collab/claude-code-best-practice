# Pack complet à transmettre à Claude Code

## 1) Message exact à copier-coller à Claude Code

```txt
Tu dois auditer et vérifier l'implémentation sécurité de backend-worker depuis ce GitHub.

Lis obligatoirement ces fichiers dans `reports/`:
- backend-worker-audit-preliminary.md
- backend-worker-cloud-code-handoff.md
- backend-worker-github-issues-prompts.md
- backend-worker-issues-created.md
- backend-worker-deployment-status-and-next-step.md
- backend-worker-variants-rollout-checklist.md
- backend-worker-claude-code-exact-prompt.txt

Objectif:
1) Vérifier que SEC-001..SEC-007 sont bien implémentées dans le code.
2) Vérifier que les tests de sécurité existent et passent.
3) Vérifier que les migrations DB ont été appliquées.
4) Vérifier les variables d'environnement critiques (Render/Supabase/Redis).
5) Vérifier qu'aucune variante applicative n'est oubliée.

Checklist obligatoire de vérification:
- SEC-001 JWT serveur: plus aucune confiance headers client pour authz
- SEC-002 Isolation tenant: filtres `organization_id` partout + tests cross-org
- SEC-003 IA hardening: validation stricte output NLU + anti prompt injection
- SEC-004 Pending actions Redis: TTL + single-use + binding user/org/session
- SEC-005 Rate limits/quotas: IP + user + org + budget tokens
- SEC-006 Upload hardening: magic bytes, MIME réel, limites alignées, anti traversal
- SEC-007 Audit/observabilité: logs sécurité + dashboards + runbooks

Sortie attendue:
- Un rapport final par SEC-00x:
  - statut: OK / PARTIEL / KO
  - preuves (fichiers + lignes)
  - tests exécutés + résultats
  - risques restants
- Un statut global Go/No-Go production
- Un tableau final par variante: N. Marti SA / Demo Garage / Demo Bâti / Demo Ing / Demo Archi

Si une vérification n'est pas possible, expliquer précisément pourquoi et ce qu'il faut pour la compléter.
```

---

## 2) Fichiers à lui donner (minimum)

1. `reports/backend-worker-audit-preliminary.md`
2. `reports/backend-worker-cloud-code-handoff.md`
3. `reports/backend-worker-github-issues-prompts.md`
4. `reports/backend-worker-issues-created.md`
5. `reports/backend-worker-deployment-status-and-next-step.md`
6. `reports/backend-worker-variants-rollout-checklist.md`
7. `reports/backend-worker-claude-code-exact-prompt.txt`

---

## 3) Ce que tu dois lui demander explicitement

- "Vérifie **dans le code**, pas seulement dans les docs."
- "Donne des preuves avec chemins de fichiers + numéros de lignes."
- "Exécute les tests et colle les résultats."
- "Confirme variante par variante."
- "Donne un verdict final GO / NO-GO."

# backend-worker — Brief orienté vérification à transmettre à Claude Code

## Message exact (copier-coller)

```txt
Tu dois faire une vérification complète de l'état SEC-001..SEC-007 sur backend-worker (pas implémenter de nouvelles features tant que le diagnostic n'est pas terminé).

1) Lis ces fichiers:
- reports/backend-worker-audit-preliminary.md
- reports/backend-worker-cloud-code-handoff.md
- reports/backend-worker-github-issues-prompts.md
- reports/backend-worker-issues-created.md
- reports/backend-worker-deployment-status-and-next-step.md
- reports/backend-worker-variants-rollout-checklist.md

2) Vérifie dans le code (preuves obligatoires fichier + lignes):
- SEC-001 JWT/auth serveur
- SEC-002 isolation tenant
- SEC-003 hardening IA/prompt injection
- SEC-004 pending actions Redis
- SEC-005 rate limits/quotas
- SEC-006 upload hardening
- SEC-007 audit logs/observabilité

3) Exécute et colle les sorties:
- npm run typecheck
- npm test
- npm run lint (si présent)

4) Pour chaque ticket SEC-00x, rends ce format:
- Statut: OK / PARTIEL / KO
- Preuves code: chemins + lignes
- Tests: commandes + output synthétique
- Risques restants
- Action suivante recommandée

5) Donne un verdict final:
- GO/NO-GO global
- Tableau final par ticket (SEC-001..SEC-007)
- Tableau final par variante (N. Marti SA, Demo Garage, Demo Bâti, Demo Ing, Demo Archi)

Si une vérification est impossible, expliquer exactement pourquoi et ce qu'il manque.
```

## Format de sortie attendu (résumé)

| Ticket | Statut | Preuves code | Tests exécutés | Risques restants | Action suivante |
|---|---|---|---|---|---|
| SEC-001 |  |  |  |  |  |
| SEC-002 |  |  |  |  |  |
| SEC-003 |  |  |  |  |  |
| SEC-004 |  |  |  |  |  |
| SEC-005 |  |  |  |  |  |
| SEC-006 |  |  |  |  |  |
| SEC-007 |  |  |  |  |  |

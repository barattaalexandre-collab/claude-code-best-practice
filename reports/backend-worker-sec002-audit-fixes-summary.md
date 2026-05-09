# SEC-002 — Résumé correctifs audit multi-tenant

## Constat

Audit détecte des requêtes non filtrées org.

## Analyse

- Certains signaux étaient des faux positifs (INSERT avec `organization_id` déjà présent).
- Des correctifs réels étaient nécessaires sur des lookups sans filtre org.
- Un rollback delete a été durci avec filtre org (defense-in-depth).

## Correctifs appliqués (selon exécution rapportée)

1. Ajout filtre org sur lookups `crm.ts` (correctif réel).
2. Ajout filtre org sur rollback delete `financial_documents` (durcissement).
3. Mise à jour script audit pour ignorer opérations INSERT (réduction faux positifs).

## Résultat attendu

- Audit SEC-002 passe (`exit 0`).
- Signal plus fiable: moins de faux positifs, meilleure détection de vraies fuites inter-tenant.

## Référence commits mentionnés

- `0dc147d`: correctifs sécurité + script audit
- `0178f0a`: mise à jour live status board

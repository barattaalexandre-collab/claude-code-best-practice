# backend-worker — après création du handoff Claude Code

## État confirmé

Le fichier opérationnel a été créé dans le dépôt réel:

`/Users/alexandrebaratta/backend-worker/reports/backend-worker-a-donner-a-claude-code-maintenant.md`

D'après le retour fourni, ce fichier contient maintenant:

- l'état complet production,
- les URLs utiles,
- l'état CORS actuel,
- les 3 prochaines tâches,
- les commandes de vérification,
- les incidents à éviter.

Donc l'étape suivante n'est plus de rédiger un nouveau plan. L'étape suivante est de **faire exécuter ce fichier par Claude Code dans le repo `backend-worker`**.

---

## Ce que tu donnes concrètement à Claude Code maintenant

Dans Claude Code, ouvrir le dépôt réel:

```bash
cd /Users/alexandrebaratta/backend-worker
```

Puis donner ce prompt court:

```text
Lis `reports/backend-worker-a-donner-a-claude-code-maintenant.md`.

Exécute uniquement les 3 prochaines tâches qui y sont listées, dans cet ordre:

1. Redis / Upstash pour les pending actions et/ou rate limiting.
2. CI / vérifications automatisées.
3. SEC-001 phase 2.

Contraintes:
- Ne pars pas sur une refonte globale.
- Ne touche pas à l'UX, aux swimlanes, à l'import client ou au pricing.
- Ne mélange pas plusieurs chantiers dans une seule grosse PR si ce n'est pas nécessaire.
- Avant toute modification, résume-moi le plan d'action en 5 à 10 lignes.
- Après modification, donne les fichiers changés, les commandes exécutées, les résultats et le rollback.

Commandes de vérification attendues:
- npm run typecheck
- npm test
- npm run lint si disponible

Si une commande échoue, arrête-toi, explique la cause probable et propose la correction minimale.
```

---

## Ordre des 3 tâches

### 1. Redis / Upstash

But: supprimer le risque de perte des pending actions au restart et préparer rate limiting robuste.

Résultat attendu:

- variables Upstash documentées/configurées,
- fallback mémoire clairement limité au dev si conservé,
- pending action TTL + single-use vérifiés,
- smoke test de confirmation IA documenté.

### 2. CI / vérifications automatisées

But: éviter de dépendre de vérifications manuelles.

Résultat attendu:

- typecheck lancé en CI,
- tests lancés en CI,
- lint lancé si disponible,
- échec bloquant sur PR si sécurité/tests cassés.

### 3. SEC-001 phase 2

But: poursuivre le durcissement auth après la première phase.

Résultat attendu:

- plus de dépendance à des headers client comme source de vérité,
- rôle/org dérivés d'une identité serveur fiable ou membership DB,
- tests auth 401/403/header forgery,
- risques résiduels documentés.

---

## Point de contrôle avant de continuer

On ne passe pas aux sujets produit/UX tant que Claude Code n'a pas rendu:

- les PRs ou commits associés,
- `npm run typecheck` OK,
- `npm test` OK,
- `npm run lint` OK ou absent documenté,
- preuve Redis/pending action ou explication claire si bloqué,
- preuve CI,
- preuve SEC-001 phase 2,
- rollback.

---

## Réponse courte à utiliser en réunion

"Le fichier de handoff est créé dans `backend-worker`. Maintenant on ouvre Claude Code sur ce repo et on lui demande de lire ce fichier puis d'exécuter uniquement les 3 tâches suivantes: Redis/Upstash, CI, SEC-001 phase 2. On refuse toute refonte UX ou chantier produit tant que ces trois points ne sont pas validés."

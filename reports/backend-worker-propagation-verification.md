# Vérifier si les modifications du "coeur" se propagent automatiquement aux variantes

## Réponse

Tu as raison sur le principe: si l'architecture est bien factorisée (core partagé + variantes), alors une modif core doit se propager automatiquement.

Mais pour le confirmer, il faut vérifier le mécanisme réel utilisé dans votre codebase.

## 3 cas possibles

1. **Monorepo avec package core partagé**
   - Chaque variante dépend du même package core (workspace/package manager).
   - Une mise à jour core se propage au prochain build/install.

2. **Template/génération (scaffold)**
   - Les variantes sont générées à partir d'un template.
   - Les changements ne se propagent que si on relance la génération/sync.

3. **Copie manuelle de code**
   - Chaque variante a son propre code dupliqué.
   - Rien ne se propage automatiquement.

## Vérification concrète à faire (dans le vrai repo backend-worker)

1. Rechercher où est défini le "core" (package/module central).
2. Vérifier les dépendances des variantes vers ce core.
3. Vérifier le pipeline (scripts CI/CD) qui synchronise/génère les variantes.
4. Choisir 2-3 fichiers modifiés récemment dans le core (ex: auth, rate-limit, pending-actions) et confirmer qu'ils sont utilisés au runtime des 5 variantes.

## Commandes utiles

```bash
# 1) identifier workspaces/packages
cat package.json

# 2) localiser les imports du core dans les variantes
rg "from '@app-core|from '../core|from \"../core"" .

# 3) localiser scripts de sync/génération
rg "sync|generate|scaffold|template|workspace" package.json .github scripts

# 4) vérifier présence des commits sécurité dans chaque variante
# (à adapter selon vos repos/branches)
git log --oneline --decorate -n 50
```

## Critère de confirmation

On peut répondre "oui, propagation automatique" uniquement si:
- les variantes importent réellement le core au build/runtime,
- et le pipeline déploie toutes les variantes depuis la même révision du core,
- et les vérifications smoke-tests par variante passent.

Sinon, il faut considérer que la propagation n'est pas garantie.

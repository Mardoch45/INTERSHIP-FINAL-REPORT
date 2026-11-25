# Publication sur GitHub

Le dépôt a été préparé et initialisé localement. Aucun dépôt distant n'a été créé et aucun fichier n'a été envoyé à GitHub pendant ce travail.

Le nom proposé est `Mardoch45/Networkwalks-Mediroza-Pentest`. Utilise les commandes suivantes depuis la racine de ce dépôt lorsque tu souhaites le publier.

1. Vérifier les fichiers et exécuter les tests :

   ```bash
   git status
   git ls-files
   python3 -m unittest discover -s tests -v
   ```

2. Réactiver la connexion GitHub si nécessaire :

   ```bash
   gh auth login --hostname github.com --git-protocol https --web
   gh auth status
   ```

3. Créer le dépôt public et envoyer la branche locale :

   ```bash
   gh repo create Mardoch45/Networkwalks-Mediroza-Pentest \
     --public \
     --description "Networkwalks Week 4 — rapport de pentest anonymisé et analyse SQL de démonstration" \
     --source=. \
     --remote=origin \
     --push
   ```

Si ce nom existe déjà sur ton compte, choisis un autre nom avant cette étape. Le dossier `rapport_final` du projet principal contient le rapport complet destiné à l'instructeur ; il ne fait pas partie du dépôt public.

Après avoir modifié un texte ou un document public :

```bash
git add README.md docs
git commit -m "Mettre à jour le rapport public"
git push
```

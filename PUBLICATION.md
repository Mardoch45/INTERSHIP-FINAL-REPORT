# Publication sur GitHub

La copie locale est initialisée sur `main` et reliée au dépôt indiqué : [Mardoch45/INTERSHIP-FINAL-REPORT](https://github.com/Mardoch45/INTERSHIP-FINAL-REPORT). Aucun fichier n'a été envoyé pendant ce travail ; l'environnement de préparation ne pouvait pas résoudre github.com et sa connexion GitHub enregistrée était invalide.

Utilise les commandes suivantes depuis la racine de la copie locale pour terminer l'envoi depuis ton terminal.

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

3. Vérifier l'adresse distante et récupérer les éventuelles branches :

   ```bash
   git remote -v
   git fetch origin
   git branch -r
   git log --oneline --graph --all
   ```

4. Envoyer la branche locale :

   ```bash
   git push -u origin main
   ```

Si Git refuse l'envoi parce que la branche distante contient déjà des commits, conserve la sortie de `git fetch` et de `git log` pour intégrer cet historique avant de réessayer. N'utilise pas un envoi forcé pour remplacer un contenu distant que tu n'as pas examiné.

Le dossier `rapport_final` du projet principal contient le rapport complet destiné à l'instructeur ; il ne fait pas partie du dépôt public. Le commit local utilise une adresse GitHub noreply pour son auteur.

Après avoir modifié un texte ou un document public :

```bash
git add README.md docs
git commit -m "Mettre à jour le rapport public"
git push
```

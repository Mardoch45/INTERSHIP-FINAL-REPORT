# Mediroza — Vérification de la refonte du rapport public

Date : 25 novembre 2026. Version du nouveau rapport : 2.0.

## Livrables

- `Mediroza_Penetration_Testing_Report_Professional.pdf` : rapport public final de 18 pages.
- `Mediroza_Penetration_Testing_Report_Professional.docx` : source éditable correspondante, avec tableaux natifs, images et sommaire Word.
- `professional_report_evidence.json` : correspondance entre les identifiants E-01 à E-13, les sources publiques et les findings.
- `professional_report_verification.json` : résultats des contrôles automatisés et empreintes des nouveaux livrables.
- `professional_report_source_checks.json` : synthèse sans données sensibles des vérifications locales complémentaires.

Le PDF est exporté directement depuis le DOCX enregistré, après actualisation du sommaire et des champs de pagination. Les 243 paragraphes de plus de 20 caractères du corps du DOCX ont été retrouvés dans le texte extrait du PDF, après normalisation des espaces, des césures et des points de conduite du sommaire.

## Sources et conservation

Le README actuel du dépôt a été lu avant la refonte et utilisé comme référence éditoriale. Il n’a pas été modifié.

Le PDF public source est `Public_Report_Mardochee_BONOU_B084.pdf` : 11 pages. Son contenu a été extrait et sa couverture ainsi qu’une page de preuves ont été examinées visuellement. Son DOCX correspondant était disponible. Les autres rapports et les traces locales ont servi à vérifier la provenance et les limites des résultats, sans importer les annexes confidentielles dans la version publique.

Les deux anciens fichiers publics restent à leur emplacement initial. Des copies supplémentaires sont conservées dans :

- `archive/Public_Report_Mardochee_BONOU_B084_original.pdf`
- `archive/Public_Report_Mardochee_BONOU_B084_original.docx`

L’identité binaire entre chaque copie et son ancien livrable est contrôlée. Les 53 PDF et images préexistants recensés au début de l’intervention ont également été comparés à leur empreinte initiale : aucun n’a été modifié. Aucun rapport antérieur n’a été supprimé.

## Changements éditoriaux et structurels

Le nouveau rapport distingue résumé exécutif, engagement, résultats techniques, quatre fiches de vulnérabilité, analyse des risques, plan de remédiation, conclusion et annexes. Les fiches comportent toutes les rubriques demandées : identifiant, titre, sévérité, composant affecté, description, preuve technique, impact, recommandation, critères de retest et statut de validation.

Les réflexions personnelles, instructions Git/GitHub, détails de fabrication du dépôt, documentation interne des scripts et résultats de démonstration sans valeur probante ont été retirés du rapport. Les outils sont décrits par leur rôle dans l’évaluation, sans tutoriel prolongé.

L’augmentation du nombre de pages sert principalement à isoler les quatre findings et à afficher les captures dans leur contexte technique. Le registre d’annexe ne duplique pas les images.

## Cohérence avec le README

| Élément | Référence conservée dans le nouveau rapport |
|---|---|
| Auteur | Mardochée BONOU |
| Organisation / programme | Networkwalks — Cybersecurity & Ethical Hacking |
| Projet / batch | Mediroza — Final Internship Project / B084 |
| Période | 22–25 November 2026 |
| Périmètre | Application web, portail patient, trois PDF originaux, stockage web et backup SQL analysé localement |
| F-01 | High (provisional) — Partially documented |
| F-02 | High — Verified |
| F-03 | Low — Verified |
| F-04 | High — Verified |
| Risque global | HIGH ; qualification qualitative, sans score CVSS inventé |
| Résultats PDF | Trois mots de passe récupérés et trois documents originaux ouverts |
| Résultats SQL | Deux tables, 30 employés et 10 actionnaires |
| Limite temporelle SQL | En-tête du 27 août 2019 et trois dates d’emploi ultérieures ; aucune affirmation de salaires actuels |
| Outils | Même ensemble que le README, regroupé par fonction |
| Recommandations | Contrôle des requêtes et des téléchargements, protection des documents, nettoyage des métadonnées, retrait et protection des backups |
| Priorités | Les priorités « Critical » du plan ne deviennent pas des sévérités Critical |

Les sévérités et statuts des quatre fiches, les outils, l’auteur, le batch et la période sont comparés automatiquement au README. Les autres éléments ont fait l’objet d’une vérification éditoriale.

### Limites explicitement maintenues

- **F-01 :** la saisie et la page de téléchargement sont deux captures séparées. La première contient aussi « Username not found ». Elles ne prouvent pas à elles seules une transition réussie. La requête HTTP complète, sa réponse et la requête SQL côté serveur ne sont pas archivées. Le finding reste partiellement documenté.
- **F-02 :** le succès concerne les mots de passe et l’ouverture des trois originaux, pas une récupération indépendante de la clé de chiffrement. Les copies réexportées ne remplacent pas les originaux.
- **F-03 :** le commentaire opérationnel est présent dans les métadonnées du troisième PDF original. Aucune capture publique de cette étape n’est disponible ; aucune n’a été fabriquée.
- **F-04 :** les fichiers SQL fournis correspondent, les en-têtes conservés indiquent HTTP 200 et l’analyse locale est vérifiée. L’absence de session lors de la récupération reste rapportée par le stagiaire : les seuls en-têtes de réponse ne permettent pas de reconstruire la requête d’origine.
- Aucune modification de base de données, prise de contrôle administratif du serveur ou interruption de service n’a été démontrée. Aucun nouveau test réseau de la cible n’a été réalisé pour cette refonte.
- Aucune remédiation ni aucun retest réussi n’est prétendu. Les critères de retest décrivent les vérifications à effectuer ultérieurement.

## Preuves et confidentialité

Les neuf captures publiques existantes ont été examinées. Leurs octets sont inchangés, leur intégrité correspond au manifeste existant et les neuf fichiers sont intégrés dans le DOCX. Elles apparaissent dans les résultats, avec identifiant, titre, légende et lien interne vers le finding pertinent. E-01 à E-04 servent de contexte de reconnaissance ; aucun finding artificiel ne leur est attribué.

E-04 fait uniquement l’objet d’un recadrage d’affichage du fond vide à droite pour améliorer la lisibilité. Le PNG source et les masquages sont conservés ; ce recadrage est indiqué dans sa légende et dans le registre JSON.

E-10 à E-13 sont des références narratives à des artefacts restreints, clairement distinguées des captures. Aucun document patient, enregistrement SQL individuel, mot de passe récupéré ou hash original n’est joint ou reproduit.

Des vérifications locales complémentaires ont confirmé l’ouverture des trois PDF originaux et la présence du commentaire opérationnel. Les seuls INSERT des deux tables ont été réimportés dans une base SQLite en mémoire : 30 employés et 10 actionnaires ont été retrouvés. Les commandes administratives MySQL n’ont pas été exécutées. Les deux copies de backup sont identiques.

Une recherche portant sur 134 valeurs sensibles issues des sources locales — identités, coordonnées et identifiants d’employés, noms d’actionnaires, URL d’origine et empreintes originales — n’a trouvé aucune correspondance dans le texte du PDF ou les XML du DOCX. Ce contrôle ciblé complète la revue des neuf captures déjà masquées ; il ne constitue pas une garantie universelle de détection de données personnelles.

## Contrôle du rendu final

Les 18 pages ont été rendues et inspectées visuellement. Les pages de captures agrandies ont été réexaminées après ajustement. Aucun tableau débordant, image coupée involontairement, titre isolé en fin de page, page blanche ou caractère de remplacement n’a été constaté.

- Format A4, typographie Lato, palette marine et turquoise ; accent ambre réservé aux sévérités High.
- En-têtes et pieds de page cohérents ; couverture sans numéro apparent.
- Pagination effective de 18 pages et champs PAGE / NUMPAGES corrects.
- Sommaire natif, actualisé, contenant neuf entrées principales avec pages imprimées et destinations concordantes.
- Quatre liens de navigation directe vers les fiches depuis la page du sommaire.
- 48 liens internes du DOCX avec signets résolus ; 85 annotations de liens internes du PDF pointant vers des pages existantes. Plusieurs annotations peuvent correspondre à un seul lien logique.
- Texte extrait à l’intérieur des limites de page ; captures contrôlées visuellement en complément.
- Le rapport ne contient pas de lien externe actif à vérifier. Les adresses GitHub sont présentées comme références textuelles ; leur disponibilité réseau n’a pas été testée.

## Reconstruction et contrôle

Depuis la racine du dépôt `github_mediroza`, dans cet environnement Linux disposant de Python 3, Pillow, LibreOffice avec UNO et Poppler :

```bash
python3 scripts/build_professional_report.py --export
python3 scripts/verify_professional_report.py
```

L’export utilise le moteur LibreOffice intégré pour éviter de dépendre d’un service réseau ou d’un processus Word actif. Les contrôles des sources confidentielles ont été exécutés séparément dans l’espace de travail local ; les données sensibles ne sont pas nécessaires pour reconstruire le rapport public.

La reconstruction recrée les nouveaux livrables à partir du générateur. Pour des modifications manuelles de contenu, le DOCX peut aussi être édité directement ; il faut alors exporter de nouveau le PDF et actualiser le sommaire avant diffusion.

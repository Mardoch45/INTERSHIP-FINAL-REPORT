-- DEMONSTRATION : toutes les données sont fictives.
-- Aucun enregistrement du projet confidentiel n’est reproduit.
CREATE TABLE `staff` (`id` INTEGER PRIMARY KEY, `full_name` TEXT, `job_title` TEXT, `department` TEXT, `monthly_salary_zar` INTEGER);
INSERT INTO `staff` (`id`,`full_name`,`job_title`,`department`,`monthly_salary_zar`) VALUES
(1,'Employé fictif 001','Fonction de démonstration','Support',26000),
(2,'Employé fictif 002','Fonction de démonstration','IT',27000),
(3,'Employé fictif 003','Fonction de démonstration','Finance',28000),
(4,'Employé fictif 004','Fonction de démonstration','Laboratoire',29000),
(5,'Employé fictif 005','Fonction de démonstration','Accueil',30000),
(6,'Employé fictif 006','Fonction de démonstration','Support',31000),
(7,'Employé fictif 007','Fonction de démonstration','IT',32000),
(8,'Employé fictif 008','Fonction de démonstration','Finance',33000),
(9,'Employé fictif 009','Fonction de démonstration','Laboratoire',34000),
(10,'Employé fictif 010','Fonction de démonstration','Accueil',35000),
(11,'Employé fictif 011','Fonction de démonstration','Support',36000),
(12,'Employé fictif 012','Fonction de démonstration','IT',37000),
(13,'Employé fictif 013','Fonction de démonstration','Finance',38000),
(14,'Employé fictif 014','Fonction de démonstration','Laboratoire',39000),
(15,'Employé fictif 015','Fonction de démonstration','Accueil',40000),
(16,'Employé fictif 016','Fonction de démonstration','Support',41000),
(17,'Employé fictif 017','Fonction de démonstration','IT',42000),
(18,'Employé fictif 018','Fonction de démonstration','Finance',43000),
(19,'Employé fictif 019','Fonction de démonstration','Laboratoire',44000),
(20,'Employé fictif 020','Fonction de démonstration','Accueil',45000),
(21,'Employé fictif 021','Fonction de démonstration','Support',46000),
(22,'Employé fictif 022','Fonction de démonstration','IT',47000),
(23,'Employé fictif 023','Fonction de démonstration','Finance',48000),
(24,'Employé fictif 024','Fonction de démonstration','Laboratoire',49000),
(25,'Employé fictif 025','Fonction de démonstration','Accueil',50000),
(26,'Employé d''exemple 026','Fonction de démonstration','Support',51000),
(27,'Employé fictif 027','Fonction de démonstration','IT',52000),
(28,'Employé fictif 028','Fonction de démonstration','Finance',53000),
(29,'Employé fictif 029','Fonction de démonstration','Laboratoire',54000),
(30,'Employé fictif 030','Fonction de démonstration','Accueil',55000);

CREATE TABLE `shareholders` (`id` INTEGER PRIMARY KEY, `shareholder_name` TEXT, `share_percent` NUMERIC, `shares_held` INTEGER, `share_class` TEXT);
INSERT INTO `shareholders` (`id`,`shareholder_name`,`share_percent`,`shares_held`,`share_class`) VALUES
(1,'Organisation fictive 001',10,1000,'Démonstration'),
(2,'Organisation fictive 002',10,1000,'Démonstration'),
(3,'Organisation fictive 003',10,1000,'Démonstration'),
(4,'Organisation fictive 004',10,1000,'Démonstration'),
(5,'Organisation fictive 005',10,1000,'Démonstration'),
(6,'Organisation fictive 006',10,1000,'Démonstration'),
(7,'Organisation fictive 007',10,1000,'Démonstration'),
(8,'Organisation fictive 008',10,1000,'Démonstration'),
(9,'Organisation fictive 009',10,1000,'Démonstration'),
(10,'Organisation fictive 010',10,1000,'Démonstration');

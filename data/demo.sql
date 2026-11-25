-- DEMONSTRATION: all records are entirely synthetic.
-- No confidential assessment record is reproduced.
CREATE TABLE `staff` (`id` INTEGER PRIMARY KEY, `full_name` TEXT, `job_title` TEXT, `department` TEXT, `monthly_salary_zar` INTEGER);
INSERT INTO `staff` (`id`,`full_name`,`job_title`,`department`,`monthly_salary_zar`) VALUES
(1,'Synthetic Employee 001','Demonstration Role','Support',26000),
(2,'Synthetic Employee 002','Demonstration Role','IT',27000),
(3,'Synthetic Employee 003','Demonstration Role','Finance',28000),
(4,'Synthetic Employee 004','Demonstration Role','Laboratory',29000),
(5,'Synthetic Employee 005','Demonstration Role','Reception',30000),
(6,'Synthetic Employee 006','Demonstration Role','Support',31000),
(7,'Synthetic Employee 007','Demonstration Role','IT',32000),
(8,'Synthetic Employee 008','Demonstration Role','Finance',33000),
(9,'Synthetic Employee 009','Demonstration Role','Laboratory',34000),
(10,'Synthetic Employee 010','Demonstration Role','Reception',35000),
(11,'Synthetic Employee 011','Demonstration Role','Support',36000),
(12,'Synthetic Employee 012','Demonstration Role','IT',37000),
(13,'Synthetic Employee 013','Demonstration Role','Finance',38000),
(14,'Synthetic Employee 014','Demonstration Role','Laboratory',39000),
(15,'Synthetic Employee 015','Demonstration Role','Reception',40000),
(16,'Synthetic Employee 016','Demonstration Role','Support',41000),
(17,'Synthetic Employee 017','Demonstration Role','IT',42000),
(18,'Synthetic Employee 018','Demonstration Role','Finance',43000),
(19,'Synthetic Employee 019','Demonstration Role','Laboratory',44000),
(20,'Synthetic Employee 020','Demonstration Role','Reception',45000),
(21,'Synthetic Employee 021','Demonstration Role','Support',46000),
(22,'Synthetic Employee 022','Demonstration Role','IT',47000),
(23,'Synthetic Employee 023','Demonstration Role','Finance',48000),
(24,'Synthetic Employee 024','Demonstration Role','Laboratory',49000),
(25,'Synthetic Employee 025','Demonstration Role','Reception',50000),
(26,'Example Employee''s Record 026','Demonstration Role','Support',51000),
(27,'Synthetic Employee 027','Demonstration Role','IT',52000),
(28,'Synthetic Employee 028','Demonstration Role','Finance',53000),
(29,'Synthetic Employee 029','Demonstration Role','Laboratory',54000),
(30,'Synthetic Employee 030','Demonstration Role','Reception',55000);

CREATE TABLE `shareholders` (`id` INTEGER PRIMARY KEY, `shareholder_name` TEXT, `share_percent` NUMERIC, `shares_held` INTEGER, `share_class` TEXT);
INSERT INTO `shareholders` (`id`,`shareholder_name`,`share_percent`,`shares_held`,`share_class`) VALUES
(1,'Synthetic Organization 001',10,1000,'Demonstration'),
(2,'Synthetic Organization 002',10,1000,'Demonstration'),
(3,'Synthetic Organization 003',10,1000,'Demonstration'),
(4,'Synthetic Organization 004',10,1000,'Demonstration'),
(5,'Synthetic Organization 005',10,1000,'Demonstration'),
(6,'Synthetic Organization 006',10,1000,'Demonstration'),
(7,'Synthetic Organization 007',10,1000,'Demonstration'),
(8,'Synthetic Organization 008',10,1000,'Demonstration'),
(9,'Synthetic Organization 009',10,1000,'Demonstration'),
(10,'Synthetic Organization 010',10,1000,'Demonstration');

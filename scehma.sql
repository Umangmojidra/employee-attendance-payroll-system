CREATE DATABASE  IF NOT EXISTS `eap` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `eap`;
-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: eap
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `e_id` int DEFAULT NULL,
  `dep_id` int DEFAULT NULL,
  `status` varchar(40) DEFAULT NULL,
  `login_date` date DEFAULT NULL,
  `login_time` time DEFAULT NULL,
  `penalty` tinyint(1) DEFAULT '0',
  `overtime` int DEFAULT '0',
  KEY `e_id` (`e_id`),
  KEY `dep_id` (`dep_id`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`e_id`) REFERENCES `employees` (`e_id`),
  CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`dep_id`) REFERENCES `departments` (`dep_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES (202501002,3,'Present','2025-10-01','10:29:56',0,0),(202501003,4,'Half_Day','2025-10-01','10:53:29',0,0),(202501004,5,'Present','2025-10-01','11:38:59',1,2),(202501005,1,'Present','2025-10-01','11:03:25',1,0),(202501006,2,'Absent','2025-10-01','09:00:59',0,0),(202501002,3,'Half_Day','2025-10-02','09:30:03',0,0),(202501003,4,'Work_from_home','2025-10-02','09:22:18',0,0),(202501004,5,'Work_from_home','2025-10-02','11:33:23',1,0),(202501005,1,'Half_Day','2025-10-02','09:13:45',0,0),(202501006,2,'Present','2025-10-02','11:20:49',1,0),(202501002,3,'Present','2025-10-03','11:55:08',1,0),(202501003,4,'Half_Day','2025-10-03','11:08:44',0,0),(202501004,5,'Absent','2025-10-03','10:47:54',0,0),(202501005,1,'Work_from_home','2025-10-03','11:51:36',1,0),(202501006,2,'Work_from_home','2025-10-03','11:09:27',1,0),(202501002,3,'Work_from_home','2025-10-04','09:15:10',0,0),(202501003,4,'Work_from_home','2025-10-04','09:23:17',0,0),(202501004,5,'Present','2025-10-04','11:06:03',1,1),(202501005,1,'Present','2025-10-04','10:05:12',0,1),(202501006,2,'Work_from_home','2025-10-04','09:13:25',0,0),(202501002,3,'Work_from_home','2025-10-05','11:48:37',1,0),(202501003,4,'Present','2025-10-05','09:23:03',0,0),(202501004,5,'Present','2025-10-05','11:20:15',1,2),(202501005,1,'Present','2025-10-05','11:38:11',1,0),(202501006,2,'Half_Day','2025-10-05','09:47:50',0,0),(202501002,3,'Absent','2025-10-06','10:22:29',0,0),(202501003,4,'Half_Day','2025-10-06','09:56:47',0,0),(202501004,5,'Work_from_home','2025-10-06','11:36:35',1,0),(202501005,1,'Absent','2025-10-06','11:04:01',0,0),(202501006,2,'Present','2025-10-06','09:47:03',0,0),(202501002,3,'Work_from_home','2025-10-07','10:30:47',0,0),(202501003,4,'Present','2025-10-07','10:46:18',1,0),(202501004,5,'Half_Day','2025-10-07','10:36:41',0,0),(202501005,1,'Half_Day','2025-10-07','10:46:04',0,0),(202501006,2,'Present','2025-10-07','10:05:20',0,2),(202501002,3,'Half_Day','2025-10-08','11:16:10',0,0),(202501003,4,'Present','2025-10-08','11:14:14',1,2),(202501004,5,'Absent','2025-10-08','10:56:02',0,0),(202501005,1,'Present','2025-10-08','11:18:55',1,1),(202501006,2,'Work_from_home','2025-10-08','09:01:40',0,0),(202501002,3,'Absent','2025-10-09','09:45:54',0,0),(202501003,4,'Work_from_home','2025-10-09','11:17:11',1,0),(202501004,5,'Present','2025-10-09','09:33:19',0,1),(202501005,1,'Half_Day','2025-10-09','10:05:09',0,0),(202501006,2,'Work_from_home','2025-10-09','09:16:51',0,0),(202501002,3,'Work_from_home','2025-10-10','10:33:45',1,0),(202501003,4,'Half_Day','2025-10-10','09:09:37',0,0),(202501004,5,'Present','2025-10-10','09:58:58',0,1),(202501005,1,'Half_Day','2025-10-10','11:02:57',0,0),(202501006,2,'Present','2025-10-10','11:36:39',1,2),(202501002,3,'Absent','2025-10-11','10:38:03',0,0),(202501003,4,'Half_Day','2025-10-11','09:27:02',0,0),(202501004,5,'Present','2025-10-11','11:51:12',1,1),(202501005,1,'Half_Day','2025-10-11','09:10:17',0,0),(202501006,2,'Present','2025-10-11','10:21:42',0,2),(202501002,3,'Present','2025-10-12','11:36:01',1,0),(202501003,4,'Absent','2025-10-12','09:15:52',0,0),(202501004,5,'Present','2025-10-12','10:54:58',1,1),(202501005,1,'Absent','2025-10-12','11:16:02',0,0),(202501006,2,'Work_from_home','2025-10-12','10:29:06',0,0),(202501002,3,'Present','2025-10-13','10:48:47',1,1),(202501003,4,'Present','2025-10-13','09:05:38',0,0),(202501004,5,'Absent','2025-10-13','09:33:35',0,0),(202501005,1,'Present','2025-10-13','11:36:12',1,0),(202501006,2,'Work_from_home','2025-10-13','11:23:29',1,0),(202501002,3,'Half_Day','2025-10-14','10:12:37',0,0),(202501003,4,'Absent','2025-10-14','10:28:37',0,0),(202501004,5,'Absent','2025-10-14','11:10:20',0,0),(202501005,1,'Absent','2025-10-14','09:58:41',0,0),(202501006,2,'Half_Day','2025-10-14','11:02:04',0,0),(202501002,3,'Present','2025-10-15','11:51:12',1,0),(202501003,4,'Work_from_home','2025-10-15','10:03:01',0,0),(202501004,5,'Work_from_home','2025-10-15','09:31:02',0,0),(202501005,1,'Absent','2025-10-15','09:22:30',0,0),(202501006,2,'Half_Day','2025-10-15','11:28:24',0,0),(202501002,3,'Present','2025-10-16','10:37:11',1,0),(202501003,4,'Work_from_home','2025-10-16','11:45:22',1,0),(202501004,5,'Present','2025-10-16','10:53:32',1,2),(202501005,1,'Half_Day','2025-10-16','11:27:20',0,0),(202501006,2,'Work_from_home','2025-10-16','09:46:11',0,0),(202501002,3,'Absent','2025-10-17','10:31:21',0,0),(202501003,4,'Present','2025-10-17','10:00:10',0,0),(202501004,5,'Work_from_home','2025-10-17','10:20:16',0,0),(202501005,1,'Work_from_home','2025-10-17','09:10:26',0,0),(202501006,2,'Half_Day','2025-10-17','09:15:49',0,0),(202501002,3,'Absent','2025-10-18','09:26:38',0,0),(202501003,4,'Absent','2025-10-18','09:03:45',0,0),(202501004,5,'Present','2025-10-18','09:11:41',0,1),(202501005,1,'Present','2025-10-18','09:51:16',0,0),(202501006,2,'Half_Day','2025-10-18','09:05:57',0,0),(202501002,3,'Absent','2025-10-19','09:08:46',0,0),(202501003,4,'Work_from_home','2025-10-19','10:53:11',1,0),(202501004,5,'Absent','2025-10-19','10:31:38',0,0),(202501005,1,'Half_Day','2025-10-19','09:02:30',0,0),(202501006,2,'Work_from_home','2025-10-19','11:02:51',1,0),(202501002,3,'Half_Day','2025-10-20','11:31:35',0,0),(202501003,4,'Absent','2025-10-20','11:34:32',0,0),(202501004,5,'Work_from_home','2025-10-20','11:11:55',1,0),(202501005,1,'Present','2025-10-20','09:35:36',0,2),(202501006,2,'Present','2025-10-20','10:40:31',1,0),(202501002,3,'Work_from_home','2025-10-21','10:00:31',0,0),(202501003,4,'Present','2025-10-21','10:55:29',1,2),(202501004,5,'Present','2025-10-21','10:06:20',0,1),(202501005,1,'Half_Day','2025-10-21','09:29:14',0,0),(202501006,2,'Work_from_home','2025-10-21','11:49:17',1,0),(202501002,3,'Present','2025-10-22','10:13:27',0,2),(202501003,4,'Absent','2025-10-22','11:13:16',0,0),(202501004,5,'Work_from_home','2025-10-22','11:49:43',1,0),(202501005,1,'Present','2025-10-22','09:45:15',0,1),(202501006,2,'Absent','2025-10-22','10:52:35',0,0),(202501002,3,'Absent','2025-10-23','10:12:51',0,0),(202501003,4,'Absent','2025-10-23','09:11:04',0,0),(202501004,5,'Half_Day','2025-10-23','10:34:35',0,0),(202501005,1,'Present','2025-10-23','10:17:35',0,0),(202501006,2,'Absent','2025-10-23','11:33:23',0,0),(202501002,3,'Work_from_home','2025-10-24','11:30:03',1,0),(202501003,4,'Half_Day','2025-10-24','09:30:35',0,0),(202501004,5,'Present','2025-10-24','11:10:47',1,2),(202501005,1,'Absent','2025-10-24','11:07:25',0,0),(202501006,2,'Half_Day','2025-10-24','10:17:15',0,0),(202501002,3,'Present','2025-10-25','11:21:02',1,2),(202501003,4,'Present','2025-10-25','10:30:22',0,1),(202501004,5,'Half_Day','2025-10-25','09:02:13',0,0),(202501005,1,'Present','2025-10-25','09:59:24',0,1),(202501006,2,'Present','2025-10-25','10:31:52',1,0),(202501002,3,'Work_from_home','2025-10-26','11:46:03',1,0),(202501003,4,'Present','2025-10-26','11:38:49',1,0),(202501004,5,'Absent','2025-10-26','09:43:50',0,0),(202501005,1,'Work_from_home','2025-10-26','10:17:42',0,0),(202501006,2,'Half_Day','2025-10-26','09:02:00',0,0),(202501002,3,'Present','2025-10-27','09:58:51',0,1),(202501003,4,'Present','2025-10-27','09:54:52',0,0),(202501004,5,'Present','2025-10-27','10:41:20',1,2),(202501005,1,'Present','2025-10-27','11:25:12',1,0),(202501006,2,'Half_Day','2025-10-27','10:01:01',0,0),(202501002,3,'Half_Day','2025-10-28','09:47:06',0,0),(202501003,4,'Absent','2025-10-28','11:45:52',0,0),(202501004,5,'Half_Day','2025-10-28','09:27:38',0,0),(202501005,1,'Present','2025-10-28','10:52:17',1,0),(202501006,2,'Absent','2025-10-28','09:26:39',0,0),(202501002,3,'Absent','2025-10-29','09:35:30',0,0),(202501003,4,'Present','2025-10-29','10:14:51',0,0),(202501004,5,'Present','2025-10-29','10:13:00',0,1),(202501005,1,'Present','2025-10-29','09:38:57',0,2),(202501006,2,'Absent','2025-10-29','10:05:09',0,0),(202501002,3,'Present','2025-10-30','09:06:49',0,0),(202501003,4,'Absent','2025-10-30','11:53:49',0,0),(202501004,5,'Absent','2025-10-30','09:56:10',0,0),(202501005,1,'Present','2025-10-30','09:42:57',0,1),(202501006,2,'Half_Day','2025-10-30','09:28:56',0,0),(202501007,5,'Half_Day','2025-10-15','19:12:42',1,0),(202501008,3,'Present','2025-10-16','08:55:11',0,0),(202501008,3,'Work_from_home','2026-02-27','22:04:05',1,0),(202501008,3,'Absent','2026-02-27','22:04:36',0,0),(202501009,1,'Work_from_home','2026-02-27','22:20:01',1,0),(202501002,2,'Absent','2026-10-17','11:09:16',0,1),(202501003,5,'Present','2026-10-17','12:49:02',0,1),(202501004,1,'Work_from_home','2026-10-17','11:58:54',0,0),(202501005,3,'Work_from_home','2026-10-17','11:23:47',0,1),(202501006,5,'Work_from_home','2026-10-17','11:17:11',0,0),(202501007,2,'Work_from_home','2026-10-17','11:26:56',0,0),(202501008,4,'Work_from_home','2026-10-17','09:43:47',0,1),(202501002,5,'Work_from_home','2026-10-17','10:27:50',1,1),(202501003,3,'Work_from_home','2026-10-17','10:56:38',1,0),(202501004,1,'Absent','2026-10-17','12:36:31',1,2),(202501005,3,'Absent','2026-10-17','11:30:14',1,0),(202501006,2,'Work_from_home','2026-10-17','09:39:44',1,0),(202501007,3,'Absent','2026-10-17','09:41:04',0,1),(202501008,5,'Work_from_home','2026-10-17','09:57:43',1,0),(202501002,1,'Half_Day','2026-10-17','09:47:29',1,1),(202501003,3,'Half_Day','2026-10-17','10:47:29',1,0),(202501004,4,'Half_Day','2026-10-17','10:59:47',0,0),(202501005,1,'Present','2026-10-17','10:34:05',0,2),(202501006,4,'Present','2026-10-17','09:05:39',0,0),(202501007,5,'Absent','2026-10-17','11:03:00',0,1),(202501008,1,'Half_Day','2026-10-17','09:56:45',0,2),(202501006,1,'Present','2026-03-03','21:09:51',1,0),(202501002,2,'Absent','2026-03-03','21:10:57',0,0),(202501003,4,'Work_from_home','2026-03-03','21:11:18',1,0),(202501004,3,'Present','2026-03-03','21:11:35',1,0),(202501007,5,'Present','2026-03-03','21:11:53',1,0),(202501009,1,'Present','2026-03-03','21:12:20',1,0),(202501005,5,'Half_Day','2026-03-03','21:13:11',1,0),(202501008,3,'Present','2026-03-03','21:13:20',1,0),(202501010,3,'Present','2026-03-03','21:13:32',1,0),(202501004,3,'Present','2026-03-04','23:45:56',1,0),(202501002,2,'Work_from_home','2026-03-05','10:42:28',1,0),(202501009,1,'Absent','2026-03-05','10:44:11',0,0);
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `dep_id` int NOT NULL,
  `dep_name` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`dep_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (1,'HR'),(2,'Finance'),(3,'IT'),(4,'Marketing'),(5,'Operations');
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `e_id` int NOT NULL AUTO_INCREMENT,
  `e_name` varchar(50) DEFAULT NULL,
  `dep_id` int DEFAULT NULL,
  `mobile` bigint DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `city` varchar(40) DEFAULT NULL,
  `joining_date` date DEFAULT (curdate()),
  `blood_group` varchar(10) DEFAULT NULL,
  `salary` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`e_id`),
  KEY `fk_dep_id` (`dep_id`),
  CONSTRAINT `fk_dep_id` FOREIGN KEY (`dep_id`) REFERENCES `departments` (`dep_id`)
) ENGINE=InnoDB AUTO_INCREMENT=202501013 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES (202501002,'sai',2,8974563214,'bvb@gmail.com','hyderabad','2025-10-14','b-',45000.00),(202501003,'Biswajit',4,7894562310,'panda23@gmail.com','puri','2025-10-15','a+',30000.00),(202501004,'reddy',3,8975642301,'reddy1@gmail.com','vijayawada','2025-10-15','ab-',40000.00),(202501005,'divya',5,8794651230,'divya5@gmail.com','tirupati','2025-10-15','o+',35000.00),(202501006,'rohit',1,8796320145,'rohit67@gmail.com','kovvuru','2025-10-15','b-',50000.00),(202501007,'manoj',5,9876544561,'manoj234@gmail.com','hyderabad','2025-10-15','o+',60000.00),(202501008,'somya',3,9866325417,'mjxno@gmail.com','secundrabad','2025-10-16','b+',60000.00),(202501009,'harman',1,9999887745,'harman4@gmail.com','vizag','2025-10-16','ab-',55000.00),(202501010,'devam ',3,7894561230,'devam1w@gmail.com','bhavnagar','2026-03-03','ab+',60000.00),(202501011,'kiran',3,8888888444,'kiran@gmail.com','vadodra','2026-03-03','ab-',90000.00),(202501012,'Rajiv Rai',5,8563741235,'rajivrai123@gmail.com','Pune','2026-03-28','B+',85000.00);
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manager`
--

DROP TABLE IF EXISTS `manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manager` (
  `m_id` int NOT NULL,
  `m_name` varchar(40) DEFAULT NULL,
  `pin` int NOT NULL,
  PRIMARY KEY (`m_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager`
--

LOCK TABLES `manager` WRITE;
/*!40000 ALTER TABLE `manager` DISABLE KEYS */;
INSERT INTO `manager` VALUES (101,'Deepali',1006),(102,'Umang',3101),(103,'Prem Chandu',9090),(104,'Murari',6262),(105,'Satish',9666);
/*!40000 ALTER TABLE `manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payroll`
--

DROP TABLE IF EXISTS `payroll`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payroll` (
  `e_id` int DEFAULT NULL,
  `dep_id` int DEFAULT NULL,
  `half_days` int DEFAULT NULL,
  `full_days` int DEFAULT NULL,
  `wfhs` int DEFAULT NULL,
  `absents` int DEFAULT NULL,
  `month` int DEFAULT NULL,
  `per_bonus` int DEFAULT NULL,
  `total_overtime` int DEFAULT NULL,
  `total_penalty` int DEFAULT NULL,
  `pro_rated_sal` decimal(10,2) DEFAULT NULL,
  `tax_amount` decimal(10,2) DEFAULT NULL,
  `pro_fund` decimal(10,2) DEFAULT NULL,
  KEY `e_id` (`e_id`),
  KEY `dep_id` (`dep_id`),
  CONSTRAINT `payroll_ibfk_1` FOREIGN KEY (`e_id`) REFERENCES `employees` (`e_id`),
  CONSTRAINT `payroll_ibfk_2` FOREIGN KEY (`dep_id`) REFERENCES `departments` (`dep_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payroll`
--

LOCK TABLES `payroll` WRITE;
/*!40000 ALTER TABLE `payroll` DISABLE KEYS */;
INSERT INTO `payroll` VALUES (202501002,2,5,10,7,8,10,1000,6,10,27370.00,2380.00,1200.00),(202501003,4,6,10,6,8,10,5000,5,7,21339.50,2110.50,1200.00),(202501004,3,4,13,6,7,10,3000,18,12,29520.00,3280.00,1200.00),(202501005,5,8,14,3,5,10,4000,9,7,25587.50,3162.50,1200.00),(202501006,1,9,7,9,5,10,6000,6,8,34994.67,4772.00,1200.00),(202501007,5,1,0,0,0,10,100,0,1,790.50,59.50,200.00),(202501005,1,8,14,3,5,10,2000,9,7,24075.00,2675.00,1200.00);
/*!40000 ALTER TABLE `payroll` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-28 20:37:10

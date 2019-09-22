-- EntryDSM 4.0 TFT DDL

CREATE DATABASE IF NOT EXISTS entry4;

use entry4;

CREATE TABLE `unauthorized_applicant` (
  `email` varchar(320) NOT NULL,
  `password` varchar(320) NOT NULL DEFAULT '',
  `verification_code` varchar(50) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `admin` (
  `admin_id` varchar(45) NOT NULL,
  `admin_password` varchar(93) NOT NULL DEFAULT '',
  `admin_type` varchar(32) NOT NULL,
  `admin_email` varchar(320) NOT NULL,
  `admin_name` varchar(13) NOT NULL,
  PRIMARY KEY (`admin_id`),
  KEY `type_index` (`admin_type`),
  KEY `name_index` (`admin_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `applicant` (
  `email` varchar(320) NOT NULL,
  `password` varchar(93) NOT NULL DEFAULT '',
  `applicant_name` varchar(13) DEFAULT NULL,
  `sex` varchar(12) DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `parent_name` varchar(13) DEFAULT NULL,
  `parent_tel` varchar(12) DEFAULT NULL,
  `applicant_tel` varchar(12) DEFAULT NULL,
  `address` varchar(500) DEFAULT NULL,
  `post_code` varchar(5) DEFAULT NULL,
  `image_path` varchar(256) DEFAULT NULL,


  PRIMARY KEY (`email`),
  UNIQUE KEY `applicant_tel_UNIQUE` (`applicant_tel`),
  UNIQUE KEY `image_path_UNIQUE` (`image_path`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `applicant_status` (
  `applicant_email` varchar(320) NOT NULL,
  `receipt_code` int(3) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `is_paid` tinyint(4) NOT NULL DEFAULT '0',
  `is_printed_application_arrived` tinyint(4) NOT NULL DEFAULT '0',
  `is_passed_first_apply` tinyint(4) NOT NULL DEFAULT '0',
  `is_final_submit` tinyint(4) NOT NULL DEFAULT '0',
  `exam_code` varchar(6) DEFAULT NULL,


  PRIMARY KEY (`applicant_email`),
  UNIQUE KEY `receipt_code_UNIQUE` (`receipt_code`),
  UNIQUE KEY `exam_code_UNIQUE` (`exam_code`),
  KEY `fk_applicant_status_applicant_idx` (`applicant_email`),
  CONSTRAINT `fk_applicant_status_applicant` FOREIGN KEY (`applicant_email`) REFERENCES `applicant` (`email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `academic_information` (
  `applicant_email` varchar(320) NOT NULL,
  `school_code` varchar(10) NOT NULL,
  `student_class` varchar(2) DEFAULT NULL,
  `student_number` varchar(2) DEFAULT NULL,
  `academic_tel` varchar(12) DEFAULT NULL,


  PRIMARY KEY (`applicant_email`),
  KEY `fk_academic_information_school_idx` (`school_code`),
  CONSTRAINT `fk_academic_information_school` FOREIGN KEY (`school_code`) REFERENCES `school` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `applicant_document` (
  `applicant_email` varchar(320) NOT NULL,
  `self_introduction_text` text,
  `study_plan_text` text,


  PRIMARY KEY (`applicant_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `applicant_score` (
  `applicant_email` varchar(320) NOT NULL,
  `volunteer_time` int(11) DEFAULT NULL,
  `full_cut_count` int(11) DEFAULT NULL,
  `period_cut_count` int(11) DEFAULT NULL,
  `late_count` int(11) DEFAULT NULL,
  `early_leave_count` int(11) DEFAULT NULL,
  `volunteer_score` decimal(10,5) DEFAULT NULL,
  `attendance_score` int(11) DEFAULT NULL,
  `conversion_score` decimal(10,5) DEFAULT NULL,
  `ged_average_score` decimal(10,5) DEFAULT NULL,
  `final_score` decimal(10,5) DEFAULT NULL,


  PRIMARY KEY (`applicant_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `classification` (
  `applicant_email` varchar(320) NOT NULL,
  `apply_type` varchar(45) DEFAULT NULL,
  `is_ged` tinyint(4) DEFAULT NULL,
  `is_daejeon` tinyint(4) DEFAULT NULL,
  `is_graduated` tinyint(4) DEFAULT NULL,
  `additional_type` varchar(45) DEFAULT NULL,
  `social_detail_type` varchar(45) DEFAULT NULL,


  `graudated_year` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`applicant_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `grade_by_semester` (
  `applicant_email` varchar(320) NOT NULL,
  `subject` varchar(45) NOT NULL,
  `semester` int(10) unsigned NOT NULL,
  `score` varchar(1) DEFAULT NULL,


  PRIMARY KEY (`applicant_email`,`subject`,`semester`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `school` (
  `code` varchar(10) NOT NULL,
  `school_name` varchar(50) DEFAULT NULL,
  `school_full_name` varchar(60) DEFAULT NULL,
  `education_office` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`code`),
  KEY `school_name` (`school_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

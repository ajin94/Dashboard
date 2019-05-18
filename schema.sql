CREATE DATABASE `dashboard`;

USE `dashboard`;


CREATE TABLE `users` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(100),
  `password` VARCHAR(100),
  `created_date` DATETIME DEFAULT CURRENT_TIMESTAMP
);

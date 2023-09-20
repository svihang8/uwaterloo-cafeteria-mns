CREATE DATABASE IF NOT EXISTS cafeteria;

USE cafeteria;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS DishIngredient;
SET FOREIGN_KEY_CHECKS = 1;
-- CREATE TABLE IF NOT EXISTS DishIngredient(
--     id INT PRIMARY KEY AUTO_INCREMENT,
--     dish_id INT,
--     ingredient_id INT,
--     FOREIGN KEY (dish_id) REFERENCES Dishes(id),
--     FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id)
-- );

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Menu;
SET FOREIGN_KEY_CHECKS = 1;
-- CREATE Table IF NOT EXISTS Menu(
--     id INT PRIMARY KEY AUTO_INCREMENT,
--     date datetime NOT NULL,
--     dish_id INT,
--     FOREIGN KEY (dish_id) REFERENCES Dishes(id)
-- );

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Ingredients;
SET FOREIGN_KEY_CHECKS = 1;
-- CREATE TABLE IF NOT EXISTS Ingredients(
--     id INT PRIMARY KEY AUTO_INCREMENT,
--     ingredient VARCHAR(255) UNIQUE NOT NULL,
--     allergen boolean DEFAULT false
-- );

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Dishes;
SET FOREIGN_KEY_CHECKS = 1;
-- CREATE TABLE IF NOT EXISTS Dishes(
--     id INT PRIMARY KEY AUTO_INCREMENT,
--     dish VARCHAR(255) UNIQUE NOT NULL,
--     url text
-- );

DROP TABLE IF EXISTS Allergies;
-- CREATE TABLE IF NOT EXISTS Allergies(
--     id INT PRIMARY KEY AUTO_INCREMENT,
--     user_id INT,
--     ingredient_id INT
-- );

--@block

DROP TABLE IF EXISTS Users;
-- CREATE TABLE IF NOT EXISTS Users(
--     id INT PRIMARY KEY AUTO_INCREMENT,
--     firstname VARCHAR(255) NOT NULL,
--     phonenumber CHAR(10) UNIQUE NOT NULL,
--     notificationtime TIME(0) DEFAULT '00:00:00'
-- );

--@block
SELECT notificationtime FROM Users WHERE firstname = 'Vihang'
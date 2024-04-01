-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 03, 2023 at 05:30 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Tandon`
--

-- --------------------------------------------------------

--
-- Table structure for table `Administrator`
--

CREATE TABLE `Administrator` (
  `Admin_ID` varchar(30) NOT NULL,
  `Admin_Password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Administrator`
--

INSERT INTO `Administrator` (`Admin_ID`, `Admin_Password`) VALUES
('Admin', 'Admin');

-- --------------------------------------------------------

--
-- Table structure for table `Choice`
--

CREATE TABLE `Choice` (
  `Admin_ID` varchar(30) NOT NULL,
  `Instructor_ID` varchar(30) NOT NULL,
  `Course_ID` varchar(30) NOT NULL,
  `Course_Name` varchar(30) NOT NULL,
  `Course_Credits` int(11) NOT NULL,
  `Course_Description` varchar(100) NOT NULL,
  `Department_Name` varchar(30) NOT NULL,
  `Semester` varchar(30) NOT NULL,
  `Student_Limit` int(11) NOT NULL,
  `Section_ID` varchar(30) NOT NULL,
  `Section_Day` varchar(30) NOT NULL,
  `Section_Time` time NOT NULL,
  `Section2_ID` varchar(30) NOT NULL,
  `Section2_Day` varchar(30) NOT NULL,
  `Section2_Time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Course`
--

CREATE TABLE `Course` (
  `Course_ID` varchar(30) NOT NULL,
  `Course_Name` varchar(50) NOT NULL,
  `Course_Credits` int(11) NOT NULL,
  `Course_Description` varchar(100) NOT NULL,
  `Department_Name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------


--
-- Table structure for table `Department`
--

CREATE TABLE `Department` (
  `Department_Name` varchar(30) NOT NULL,
  `Department_Address` varchar(30) NOT NULL,
  `Department_Email` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Instructor`
--

CREATE TABLE `Instructor` (
  `Instructor_ID` varchar(30) NOT NULL,
  `Instructor_Password` varchar(30) NOT NULL,
  `Instructor_Fname` varchar(30) NOT NULL,
  `Instructor_Lname` varchar(30) NOT NULL,
  `Instructor_Email` varchar(30) NOT NULL,
  `Department_Name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- --------------------------------------------------------

--
-- Table structure for table `Section`
--

CREATE TABLE `Section` (
  `Section_ID` varchar(30) NOT NULL,
  `Course_ID` varchar(30) NOT NULL,
  `Course_Name` varchar(50) NOT NULL,
  `Semester` varchar(10) DEFAULT NULL CHECK (`Semester` in ('Fall','Spring')),
  `Section_Day` varchar(10) DEFAULT NULL CHECK (`Section_Day` in ('Monday','Tuesday','Wednesday','Thursday','Friday')),
  `Section_Time` time DEFAULT NULL,
  `Student_Limit` int(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Student`
--

CREATE TABLE `Student` (
  `Student_ID` varchar(30) NOT NULL,
  `Student_Password` varchar(30) NOT NULL,
  `Student_Fname` varchar(30) NOT NULL,
  `Student_Lname` varchar(30) NOT NULL,
  `Major` varchar(30) NOT NULL,
  `Credits_Taken` int(11) DEFAULT NULL CHECK (`Credits_Taken` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Takes`
--

CREATE TABLE `Takes` (
  `Course_ID` varchar(30) NOT NULL,
  `Student_ID` varchar(30) NOT NULL,
  `Section_ID` varchar(30) NOT NULL,
  `Grade` int(11) DEFAULT NULL,
  `Rating` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Teaches`
--

CREATE TABLE `Teaches` (
  `Course_ID` varchar(30) NOT NULL,
  `Instructor_ID` varchar(30) NOT NULL,
  `Section_ID` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Indexes for table `Administrator`
--
ALTER TABLE `Administrator`
  ADD PRIMARY KEY (`Admin_ID`);

--
-- Indexes for table `Choice`
--
ALTER TABLE `Choice`
  ADD PRIMARY KEY (`Admin_ID`,`Instructor_ID`),
  ADD KEY `Instructor_ID` (`Instructor_ID`);

--
-- Indexes for table `Course`
--
ALTER TABLE `Course`
  ADD PRIMARY KEY (`Course_ID`),
  ADD KEY `Department_Name` (`Department_Name`),
  ADD KEY `Course_Name` (`Course_Name`);

--
-- Indexes for table `Department`
--
ALTER TABLE `Department`
  ADD PRIMARY KEY (`Department_Name`);

--
-- Indexes for table `Instructor`
--
ALTER TABLE `Instructor`
  ADD PRIMARY KEY (`Instructor_ID`),
  ADD KEY `Department_Name` (`Department_Name`);


--
-- Indexes for table `Section`
--
ALTER TABLE `Section`
  ADD PRIMARY KEY (`Course_ID`,`Section_ID`),
  ADD KEY `Course_Name` (`Course_Name`),
  ADD KEY `Section_ID` (`Section_ID`,`Course_ID`,`Course_Name`);

--
-- Indexes for table `Student`
--
ALTER TABLE `Student`
  ADD PRIMARY KEY (`Student_ID`);

--
-- Indexes for table `Takes`
--
ALTER TABLE `Takes`
  ADD PRIMARY KEY (`Course_ID`,`Section_ID`,`Student_ID`),
  ADD KEY `Student_ID` (`Student_ID`),
  ADD KEY `Section_ID` (`Section_ID`,`Course_ID`);

--
-- Indexes for table `Teaches`
--
ALTER TABLE `Teaches`
  ADD PRIMARY KEY (`Course_ID`,`Section_ID`,`Instructor_ID`),
  ADD KEY `Instructor_ID` (`Instructor_ID`),
  ADD KEY `Section_ID` (`Section_ID`,`Course_ID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Choice`
--
ALTER TABLE `Choice`
  ADD CONSTRAINT `choice_ibfk_1` FOREIGN KEY (`Instructor_ID`) REFERENCES `Instructor` (`Instructor_ID`),
  ADD CONSTRAINT `choice_ibfk_2` FOREIGN KEY (`Admin_ID`) REFERENCES `Administrator` (`Admin_ID`);

--
-- Constraints for table `Course`
--
ALTER TABLE `Course`
  ADD CONSTRAINT `course_ibfk_1` FOREIGN KEY (`Department_Name`) REFERENCES `Department` (`Department_Name`);

--
-- Constraints for table `Instructor`
--
ALTER TABLE `Instructor`
  ADD CONSTRAINT `instructor_ibfk_1` FOREIGN KEY (`Department_Name`) REFERENCES `Department` (`Department_Name`);

--
-- Constraints for table `Section`
--
ALTER TABLE `Section`
  ADD CONSTRAINT `section_ibfk_1` FOREIGN KEY (`Course_ID`) REFERENCES `Course` (`Course_ID`),
  ADD CONSTRAINT `section_ibfk_2` FOREIGN KEY (`Course_Name`) REFERENCES `Course` (`Course_Name`);

--
-- Constraints for table `Takes`
--
ALTER TABLE `Takes`
  ADD CONSTRAINT `takes_ibfk_1` FOREIGN KEY (`Student_ID`) REFERENCES `Student` (`Student_ID`),
  ADD CONSTRAINT `takes_ibfk_2` FOREIGN KEY (`Section_ID`,`Course_ID`) REFERENCES `Section` (`Section_ID`, `Course_ID`);

--
-- Constraints for table `Teaches`
--
ALTER TABLE `Teaches`
  ADD CONSTRAINT `teaches_ibfk_1` FOREIGN KEY (`Instructor_ID`) REFERENCES `Instructor` (`Instructor_ID`),
  ADD CONSTRAINT `teaches_ibfk_2` FOREIGN KEY (`Section_ID`,`Course_ID`) REFERENCES `Section` (`Section_ID`, `Course_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


--
-- View Creation for coursesectioncapacitydifference`
--

CREATE View `coursesectioncapacitydiff` AS
SELECT
    `s`.`Course_ID` AS `Course_ID`,
    `s`.`Section_ID` AS `Section_ID`,
    `s`.`Student_Limit` - COUNT(`r`.`Student_ID`) AS `remaining_spots`
FROM
    `section` `s`
LEFT JOIN
    `takes` `r` ON (`s`.`Course_ID` = `r`.`Course_ID` AND `s`.`Section_ID` = `r`.`Section_ID`)
GROUP BY
    `s`.`Course_ID`, `s`.`Section_ID`;



--
-- View Creation for InstructorRatingAverage`
--


CREATE VIEW InstructorRatingAverage AS
SELECT t.instructor_id,
       AVG(r.rating) AS average_rating
FROM teaches t
JOIN takes r ON t.course_id = r.course_id
           AND t.section_id = r.section_id
GROUP BY t.instructor_id;

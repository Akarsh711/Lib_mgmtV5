-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 19, 2020 at 06:09 PM
-- Server version: 10.4.6-MariaDB
-- PHP Version: 7.1.32

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lib_mgmt_test`
--

-- --------------------------------------------------------

--
-- Table structure for table `booksv2`
--

CREATE TABLE `booksv2` (
  `sno` int(11) NOT NULL,
  `name` char(50) NOT NULL,
  `rollno` varchar(15) NOT NULL,
  `author` text DEFAULT NULL,
  `more` text DEFAULT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `booksv2`
--

INSERT INTO `booksv2` (`sno`, `name`, `rollno`, `author`, `more`, `date`) VALUES
(129, 'Lina', '170090800005', '', '', '2019-09-04 23:28:00'),
(130, 'Sneha', '170090800113', '', '', '2019-09-04 23:28:29'),
(140, 'LLLL', '21', '', '', '2019-09-05 07:54:18'),
(147, 'Raman', '02', '', '', '2019-09-05 18:06:03'),
(179, 'Nariel', '99', '', '', '2019-09-15 13:43:35'),
(181, 'Siraj', '1000', '', '', '2019-09-15 13:44:40'),
(186, 'Ravi', '79', '', '', '2019-09-18 21:42:17'),
(188, 'Aman', '19', '', '', '2019-09-18 21:45:41'),
(189, 'Aman', '06', '', '', '2019-09-18 21:56:00'),
(191, 'Harsh', '', '', '', '2019-09-19 18:38:17'),
(192, 'Harsh', '15', '', '', '2019-09-19 18:38:32'),
(193, 'Akarsh', '04', '', '', '2019-11-29 14:20:14'),
(196, 'Nariel', '369', '', '', '2020-01-19 21:50:07'),
(198, 'Priya', '963', '', '', '2020-01-19 21:56:56'),
(199, 'Suman', '639', '', '', '2020-01-19 22:06:43'),
(200, 'sunny', '88', '', '', '2020-01-19 22:27:17');

-- --------------------------------------------------------

--
-- Table structure for table `books_in_lib`
--

CREATE TABLE `books_in_lib` (
  `sno` int(255) NOT NULL,
  `bookid` int(255) NOT NULL,
  `bookname` varchar(255) NOT NULL,
  `total_we_have` int(255) NOT NULL,
  `remaining_books` int(255) NOT NULL,
  `trade_code` int(11) NOT NULL,
  `trade` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `books_in_lib`
--

INSERT INTO `books_in_lib` (`sno`, `bookid`, `bookname`, `total_we_have`, `remaining_books`, `trade_code`, `trade`) VALUES
(1, 101, 'Math-1', 160, 153, 0, 'All'),
(2, 102, 'English-1', 140, 137, 0, 'All'),
(3, 103, 'Chem-1', 155, 154, 0, 'All'),
(4, 104, 'ED-1', 145, 142, 0, 'All'),
(5, 201, 'Math-2', 130, 128, 0, 'All'),
(6, 202, 'English-2', 196, 196, 0, 'All'),
(7, 203, 'CFIET', 120, 118, 0, 'All'),
(8, 204, 'ED-2', 150, 149, 0, 'All'),
(9, 301, 'C-Programing', 150, 150, 0, 'All'),
(10, 302, 'Digital-Electronics', 160, 160, 0, 'All'),
(11, 303, 'C-Programing', 150, 150, 0, 'All'),
(12, 304, 'Digital-Electronics', 160, 160, 0, 'All'),
(13, 1301, 'INTRO-TO-Electronics', 120, 120, 1, 'Electronics Engineering'),
(15, 1302, 'INTRO-TO-Analog', 100, 100, 1, 'Electronics Engineering'),
(17, 2301, 'Design-of-Machine', 100, 100, 2, 'Mechanical Engineering'),
(18, 2302, 'Thermodynamics', 180, 180, 2, 'Mechanical Engineering'),
(21, 999, 'test_Book', 100, 98, 999, 'test_trade'),
(22, 888, 'test_book2', 200, 199, 888, 'test_trade2');

-- --------------------------------------------------------

--
-- Table structure for table `my_rel`
--

CREATE TABLE `my_rel` (
  `sno` int(255) NOT NULL,
  `foreignkey` int(255) NOT NULL,
  `bookname` text NOT NULL,
  `book_id` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `my_rel`
--

INSERT INTO `my_rel` (`sno`, `foreignkey`, `bookname`, `book_id`) VALUES
(457, 129, 'math-1', '0101'),
(458, 129, 'math-2', '0201'),
(480, 140, 'ED-1', '0104'),
(492, 147, 'Chem-1', '0103'),
(530, 179, 'CFIET', '0203'),
(531, 179, 'CFIET', '0203'),
(532, 181, 'Math-2', '0201'),
(541, 186, 'Math-1', '0101'),
(542, 186, 'Math-1', '0101'),
(543, 186, 'English-1', '0102'),
(544, 186, 'ED-1', '0104'),
(545, 189, 'ED-1', '0104'),
(546, 189, 'English-1', '0102'),
(548, 192, 'ED-2', '0204'),
(549, 193, 'Math-1', '0101'),
(550, 193, 'Math-1', '0101'),
(551, 193, 'English-1', '0102'),
(554, 196, 'test_Book', '999'),
(556, 198, 'Math-1', '0101'),
(557, 198, 'Math-1', '0101'),
(558, 199, 'test_Book', '999'),
(559, 200, 'test_book2', '888');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `booksv2`
--
ALTER TABLE `booksv2`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `books_in_lib`
--
ALTER TABLE `books_in_lib`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `my_rel`
--
ALTER TABLE `my_rel`
  ADD PRIMARY KEY (`sno`),
  ADD KEY `book_rel` (`foreignkey`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `booksv2`
--
ALTER TABLE `booksv2`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=201;

--
-- AUTO_INCREMENT for table `books_in_lib`
--
ALTER TABLE `books_in_lib`
  MODIFY `sno` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `my_rel`
--
ALTER TABLE `my_rel`
  MODIFY `sno` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=560;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `my_rel`
--
ALTER TABLE `my_rel`
  ADD CONSTRAINT `my_rel_ibfk_1` FOREIGN KEY (`foreignkey`) REFERENCES `booksv2` (`sno`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

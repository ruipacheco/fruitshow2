-- phpMyAdmin SQL Dump
-- version 3.5.8.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 03, 2013 at 01:09 AM
-- Server version: 5.5.32-0ubuntu0.13.04.1
-- PHP Version: 5.4.9-4ubuntu2.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `fruit_show`
--

-- --------------------------------------------------------

--
-- Table structure for table `Category`
--

CREATE TABLE IF NOT EXISTS `Category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8_bin NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `color` text COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=6 ;

--
-- Dumping data for table `Category`
--

INSERT INTO `Category` (`id`, `title`, `date_created`, `color`) VALUES
(1, 'Public', '2013-09-15 03:53:00', ''),
(3, 'Private & Personal', '2013-09-15 04:45:01', ''),
(4, 'NSFW', '2013-09-18 06:50:21', ''),
(5, 'Finance & Economics', '2013-09-18 06:50:33', '');

-- --------------------------------------------------------

--
-- Table structure for table `Invite`
--

CREATE TABLE IF NOT EXISTS `Invite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) COLLATE utf8_bin NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `display_hash` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `Post`
--

CREATE TABLE IF NOT EXISTS `Post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `body` text COLLATE utf8_bin NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` int(11) DEFAULT NULL,
  `thread_id` int(11) NOT NULL,
  `display_hash` varchar(255) COLLATE utf8_bin NOT NULL,
  `display_name` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `display_hash_2` (`display_hash`),
  UNIQUE KEY `id` (`id`),
  KEY `display_hash` (`display_hash`),
  KEY `created_by` (`created_by`),
  KEY `thread_id` (`thread_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=66 ;

--
-- Dumping data for table `Post`
--

INSERT INTO `Post` (`id`, `body`, `date_created`, `created_by`, `thread_id`, `display_hash`, `display_name`) VALUES
(63, 'http://global3.memecdn.com/boobies_o_291194.jpg', '2013-10-03 22:08:26', 14, 75, '475433', ''),
(64, '(http://global3.memecdn.com/boobies_o_291194.jpg, "Boobies!")', '2013-10-03 22:08:26', 14, 75, '188882', ''),
(65, '![Boobies!](http://global3.memecdn.com/boobies_o_291194.jpg, "Boobies!")', '2013-10-03 22:08:26', 14, 75, '771381', '');

-- --------------------------------------------------------

--
-- Table structure for table `Role`
--

CREATE TABLE IF NOT EXISTS `Role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET latin1 NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `id_2` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=4 ;

--
-- Dumping data for table `Role`
--

INSERT INTO `Role` (`id`, `title`, `date_created`) VALUES
(1, 'Citizen', '2013-10-02 08:19:57'),
(2, 'Administrator', '2013-10-02 08:21:16'),
(3, 'Deleted', '2013-10-02 22:33:27');

-- --------------------------------------------------------

--
-- Table structure for table `Thread`
--

CREATE TABLE IF NOT EXISTS `Thread` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8_bin NOT NULL,
  `body` text COLLATE utf8_bin,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` int(11) DEFAULT NULL,
  `display_hash` varchar(255) COLLATE utf8_bin NOT NULL,
  `display_name` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `nsfw` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `display_hash_2` (`display_hash`),
  UNIQUE KEY `id_2` (`id`),
  KEY `created_by` (`created_by`),
  KEY `id` (`id`),
  KEY `display_hash` (`display_hash`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=77 ;

--
-- Dumping data for table `Thread`
--

INSERT INTO `Thread` (`id`, `title`, `body`, `date_created`, `created_by`, `display_hash`, `display_name`, `nsfw`) VALUES
(75, 'Hello!', 'Original exception was: ''AnonymousUserMixin'' object has no attribute ''_sa_instance_state''', '2013-10-03 22:08:26', 14, '98331', NULL, 1),
(76, 'This is a safe thread', 'Enjoy!', '2013-10-03 22:08:26', 14, '377255', NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `User`
--

CREATE TABLE IF NOT EXISTS `User` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) COLLATE utf8_bin NOT NULL,
  `password` varchar(255) COLLATE utf8_bin NOT NULL,
  `display_hash` varchar(255) COLLATE utf8_bin NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `email` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_2` (`username`),
  UNIQUE KEY `display_hash_2` (`display_hash`),
  UNIQUE KEY `id` (`id`),
  KEY `display_hash` (`display_hash`),
  KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Forum users' AUTO_INCREMENT=16 ;

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`id`, `username`, `password`, `display_hash`, `date_created`, `last_login`, `email`) VALUES
(11, 'aaaa', '$pbkdf2-sha512$12000$v7cW4lxrbW3tfS/lvDeG0A$WDFdog5Hlf48F89zff8nqhRFhUKRVz.lyBkattHZ7OypfwI9insd.SttSi4ZXY.Cg3frl759pH2sg0M3Abew0Q', '280711', '2013-09-24 22:11:34', '2013-10-03 11:39:20', 'aaaa@aaaa.com'),
(13, 'bbb', '$pbkdf2-sha512$12000$SsnZu5eytpaytpaSkvKe8w$WeoZzMMmcFe5Gm1CRy0fgzBOxfl.wbrm9wZxZCGZGmafeUGk.zaoDpcxPcVDumjnmanFevUohs4kkS2pBKu9DQ', '330825', '2013-09-24 22:46:04', '2013-10-03 11:39:42', 'bbb@bbb.com'),
(14, 'Funny Bunny', '$pbkdf2-sha512$12000$NKbUWosxxrj3HgNA6N373w$QuPy6K6yNePAXVbHcdtqFb7ZQnmkBO7Qa6fvy2MPIbRQ9kJIvjak.uvAh.z4fkuiSDVwhaekkl5TDuX3HHuaoQ', '342180', '2013-09-30 20:05:40', '2013-10-03 21:41:00', 'rui.pacheco@gmail.com'),
(15, 'Rui Pacheco', '$pbkdf2-sha512$12000$2lurtXaOUeq9VypljLF2Lg$2u3a4G/XrTlykm0VxZR22uJaXTKX.Y5F1MC2iqjKnLMO7ljXIrOoGASPvageif3y98Q0HdDq6cF7Icy.jfY2Sg', '824567', '2013-10-03 15:28:47', '2013-10-02 16:30:25', 'ruipacheco@hotmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `User_Role`
--

CREATE TABLE IF NOT EXISTS `User_Role` (
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  KEY `role_id` (`role_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `User_Role`
--

INSERT INTO `User_Role` (`user_id`, `role_id`) VALUES
(14, 2);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Post`
--
ALTER TABLE `Post`
  ADD CONSTRAINT `Post_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `User` (`id`),
  ADD CONSTRAINT `Post_ibfk_3` FOREIGN KEY (`thread_id`) REFERENCES `Thread` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Thread`
--
ALTER TABLE `Thread`
  ADD CONSTRAINT `Thread_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `User` (`id`);

--
-- Constraints for table `User_Role`
--
ALTER TABLE `User_Role`
  ADD CONSTRAINT `User_Role_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `User_Role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `Role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

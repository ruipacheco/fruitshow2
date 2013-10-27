-- phpMyAdmin SQL Dump
-- version 4.0.6deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 27, 2013 at 03:49 AM
-- Server version: 5.5.34-0ubuntu0.13.10.1
-- PHP Version: 5.5.3-1ubuntu2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
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
-- Table structure for table `Comment`
--

CREATE TABLE IF NOT EXISTS `Comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message_id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `body` text COLLATE utf8_bin NOT NULL,
  `display_hash` varchar(255) COLLATE utf8_bin NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `display_hash` (`display_hash`),
  KEY `message_id` (`message_id`),
  KEY `sender_id` (`sender_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `Invite`
--

CREATE TABLE IF NOT EXISTS `Invite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `display_hash` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `Message`
--

CREATE TABLE IF NOT EXISTS `Message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sender_id` int(11) NOT NULL,
  `sender_last_viewed` datetime NOT NULL,
  `subject` varchar(255) COLLATE utf8_bin NOT NULL,
  `body` text COLLATE utf8_bin NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_updated` datetime NOT NULL,
  `display_hash` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `display_hash` (`display_hash`),
  KEY `sender_id` (`sender_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=5 ;

-- --------------------------------------------------------

--
-- Table structure for table `Post`
--

CREATE TABLE IF NOT EXISTS `Post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `body` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` int(11) DEFAULT NULL,
  `thread_id` int(11) NOT NULL,
  `display_hash` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `display_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `display_hash_2` (`display_hash`),
  UNIQUE KEY `id` (`id`),
  KEY `display_hash` (`display_hash`),
  KEY `created_by` (`created_by`),
  KEY `thread_id` (`thread_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=21 ;

-- --------------------------------------------------------

--
-- Table structure for table `Role`
--

CREATE TABLE IF NOT EXISTS `Role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `display_hash` varchar(255) COLLATE utf8_bin NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `id_2` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=5 ;

--
-- Dumping data for table `Role`
--

INSERT INTO `Role` (`id`, `title`, `display_hash`, `date_created`) VALUES
(1, 'Administrator', '543210', '2013-10-08 17:29:31'),
(2, 'Private Citizen', '123456', '2013-10-20 18:43:19'),
(3, 'Citizen', '012345', '2013-10-08 17:29:19');

-- --------------------------------------------------------

--
-- Table structure for table `Thread`
--

CREATE TABLE IF NOT EXISTS `Thread` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `body` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `display_hash` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `display_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `nsfw` tinyint(1) NOT NULL DEFAULT '0',
  `last_updated` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `display_hash_2` (`display_hash`),
  UNIQUE KEY `id_2` (`id`),
  KEY `created_by` (`created_by`),
  KEY `id` (`id`),
  KEY `display_hash` (`display_hash`),
  KEY `role_id` (`role_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=45 ;

-- --------------------------------------------------------

--
-- Table structure for table `User`
--

CREATE TABLE IF NOT EXISTS `User` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `display_hash` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_2` (`username`),
  UNIQUE KEY `display_hash_2` (`display_hash`),
  UNIQUE KEY `id` (`id`),
  KEY `display_hash` (`display_hash`),
  KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Forum users' AUTO_INCREMENT=31 ;

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`id`, `username`, `password`, `display_hash`, `date_created`, `last_login`, `email`) VALUES
(17, 'Funny Bunny', '$pbkdf2-sha512$12000$iPEeI.Tcm/M.pxQCgDBG6A$4rE5WsGhIG9CCWkGQTFN14ee139fw7lhdVTg4KMeMFyTZpuA4H.orlFhBydzuMKlOl4ldO397q1.E5AyUbCdwg', '521498', '2013-10-08 11:31:27', '2013-10-08 11:37:26', 'rui.pacheco@gmail.com'),
(18, 'James', '$pbkdf2-sha512$12000$KyVE6J0zxrgXorT23puTcg$Knq.zIVTex7rCiw0qWMMDUZw.BoN.wD3qpB5oXxDqeGWtqf/yUnj8OusRxNMjLAlALxokxwdDHXHmQtCSn1zcQ', '235941', '2013-10-08 11:44:02', '2013-10-27 10:56:09', 'james@james.com'),
(19, 'Hollister', '$pbkdf2-sha512$12000$.L/XGsNYa00pBcB4D.EcAw$QzrtTZ46VM51fUkt1dS/uI5u0ypvH13QQx31aN9nAQCwDP5YNE4Qg6rev2Zi5cIC8Bj4U.69SWUnKvUalDxpzA', '50411', '2013-10-08 11:44:02', '2013-10-26 19:11:25', 'hollister@hollister.com'),
(24, 'joe', '$pbkdf2-sha512$12000$ljLmfI9Ram1tTekdo7SW8g$eDPgQy9YiiQKZHaUUgo1AW8NDuHD7SQV7Cm.lO5fvGQmqHfOs8bOAAZGDcTlj3uIxUDYjjq.CUa6feQaDmDT9w', '500630', '2013-10-08 14:09:21', '2013-10-26 13:46:11', 'joe@joe.com'),
(25, 'mark', '$pbkdf2-sha512$12000$YgyhtLYWgpDSmhMiBKC09g$R.zczfCdmNd.mxjE0hdXBji7iC3XYNR5niYqKRrfryCQZqi3SoX9XfXraap01sb0tbo/oksZOJurUGeowMsB9A', '61520', '2013-10-08 14:10:08', '2013-10-08 14:10:36', 'mark@mark.com'),
(26, 'Mojojo', '$pbkdf2-sha512$12000$p3SOEeJ8Tyml9B5DCKG0tg$OZ0qWAtzblKeKLZLCGTHpztlchOtI6GlsPnUVM0q9Vsymo7L/Sjh43Ts7CAhlC/r.Ri.2mlLa8GrooYs3DOCgg', '518882', '2013-10-08 22:02:31', '2013-10-08 22:02:46', 'mojojo@mojojo.com'),
(27, 'Bono', '$pbkdf2-sha512$12000$sRaiFCIEgHBube2917q31g$X/C0ikGmcu5JCnx6pgL4L1LUjO15aFu053UV5msptQR90P7k.DT1ntGpWGE0gXcTfhhiN5qrzh3lVjQYSgUHCw', '892060', '2013-10-08 22:32:18', '2013-10-09 17:15:07', 'bono@bono.com');

-- --------------------------------------------------------

--
-- Table structure for table `User_Message`
--

CREATE TABLE IF NOT EXISTS `User_Message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message_id` int(11) NOT NULL,
  `recipient_id` int(11) NOT NULL,
  `last_viewed` datetime NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `message_id` (`message_id`),
  KEY `recipient_id` (`recipient_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=3 ;

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
(17, 3),
(18, 3),
(19, 3),
(24, 3),
(25, 3),
(26, 3),
(27, 3),
(24, 2),
(25, 2),
(18, 1),
(18, 2);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Comment`
--
ALTER TABLE `Comment`
  ADD CONSTRAINT `Comment_ibfk_1` FOREIGN KEY (`message_id`) REFERENCES `Message` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Comment_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Message`
--
ALTER TABLE `Message`
  ADD CONSTRAINT `Message_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

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
  ADD CONSTRAINT `Thread_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Thread_ibfk_3` FOREIGN KEY (`role_id`) REFERENCES `Role` (`id`);

--
-- Constraints for table `User_Message`
--
ALTER TABLE `User_Message`
  ADD CONSTRAINT `User_Message_ibfk_2` FOREIGN KEY (`recipient_id`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `User_Message_ibfk_3` FOREIGN KEY (`message_id`) REFERENCES `Message` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `User_Role`
--
ALTER TABLE `User_Role`
  ADD CONSTRAINT `User_Role_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `User_Role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `Role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

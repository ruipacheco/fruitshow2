-- phpMyAdmin SQL Dump
-- version 3.5.8.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 18, 2013 at 06:30 AM
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

DROP TABLE IF EXISTS `Category`;
CREATE TABLE IF NOT EXISTS `Category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8_bin NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `color` text COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=4 ;

--
-- Dumping data for table `Category`
--

INSERT INTO `Category` (`category_id`, `title`, `date_created`, `color`) VALUES
(1, 'Public', '2013-09-15 03:53:00', ''),
(2, 'Registered', '2013-09-15 04:44:29', ''),
(3, 'Private & Personal', '2013-09-15 04:45:01', '');

-- --------------------------------------------------------

--
-- Table structure for table `Post`
--

DROP TABLE IF EXISTS `Post`;
CREATE TABLE IF NOT EXISTS `Post` (
  `post_id` int(11) NOT NULL AUTO_INCREMENT,
  `body` text COLLATE utf8_bin NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `spam` tinyint(1) NOT NULL DEFAULT '0',
  `created_by` int(11) DEFAULT NULL,
  `thread_id` int(11) NOT NULL,
  `display_hash` varchar(255) COLLATE utf8_bin NOT NULL,
  `display_name` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`post_id`),
  UNIQUE KEY `display_hash_2` (`display_hash`),
  KEY `display_hash` (`display_hash`),
  KEY `created_by` (`created_by`,`thread_id`,`display_hash`),
  KEY `thread_id` (`thread_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=25 ;

--
-- Dumping data for table `Post`
--

INSERT INTO `Post` (`post_id`, `body`, `date_created`, `spam`, `created_by`, `thread_id`, `display_hash`, `display_name`) VALUES
(13, 'This is the body of a post.', '2013-09-17 01:44:47', 0, NULL, 18, '12345', 'Anonymous Tits McGee'),
(14, 'Blah blah blah. Blah.', '2013-09-17 02:14:57', 0, NULL, 18, '54321', 'Anonymous Coward'),
(15, 'eee', '2013-09-26 14:54:55', 0, NULL, 22, '872241', 'eee'),
(16, 'eee', '2013-09-26 14:55:59', 0, NULL, 22, '640088', 'blah'),
(17, 'wef;wdfdf;f;vkfmkfnrfkr33423', '2013-09-26 14:59:53', 0, NULL, 18, '17109', 'ee'),
(18, 'ererere\r\n\r\nererereerer\r\n\r\nererer\r\nvcbfgr\r\n\r\nt4546e;fds frrt49\r\n\r\n4t', '2013-09-26 14:59:53', 0, NULL, 18, '754395', ''),
(19, 'eee', '2013-09-26 15:12:03', 0, NULL, 18, '845981', '4'),
(20, 'rrr', '2013-09-26 15:12:28', 0, NULL, 18, '624442', '5'),
(21, 'Burkha!', '2013-09-26 15:33:14', 0, NULL, 18, '11605', 'blahrhrhr'),
(22, 'Red Hot Chili Peppers', '2013-09-26 16:05:37', 0, NULL, 21, '399187', 'Tony Kiedis'),
(23, 'Blah!', '2013-09-26 16:06:07', 0, NULL, 21, '326919', 'Flea'),
(24, '<p>Meh!meh!meh!meh!meh!</p>\r\n<p>Blah!Bha!rr</p>', '2013-09-26 16:06:07', 0, NULL, 21, '124548', 'Poster');

-- --------------------------------------------------------

--
-- Table structure for table `Thread`
--

DROP TABLE IF EXISTS `Thread`;
CREATE TABLE IF NOT EXISTS `Thread` (
  `thread_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8_bin NOT NULL,
  `body` text COLLATE utf8_bin,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` int(11) DEFAULT NULL,
  `category_id` int(11) NOT NULL,
  `display_hash` varchar(255) COLLATE utf8_bin NOT NULL,
  `spam` tinyint(1) NOT NULL DEFAULT '0',
  `display_name` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`thread_id`),
  UNIQUE KEY `display_hash_2` (`display_hash`),
  KEY `created_by` (`created_by`),
  KEY `thread_id` (`thread_id`),
  KEY `category_id` (`category_id`),
  KEY `display_hash` (`display_hash`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=23 ;

--
-- Dumping data for table `Thread`
--

INSERT INTO `Thread` (`thread_id`, `title`, `body`, `date_created`, `created_by`, `category_id`, `display_hash`, `spam`, `display_name`) VALUES
(18, 'Test thread', '<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>\r\n\r\n<p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?</p>\r\n\r\n<p>But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?</p>\r\n\r\n<p>At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.</p>\r\n\r\n<p>On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains.</p>', '2013-09-25 13:18:09', NULL, 1, '664173', 0, 'Tits McGee'),
(19, 'Second test thread', 'And this is the body.', '2013-09-25 13:18:09', NULL, 1, '84311', 0, ''),
(20, 'Third thread', 'Just because I like to look at my own designs.', '2013-09-25 13:18:09', NULL, 1, '207167', 0, ''),
(21, 'A conversation', 'Too!', '2013-09-25 14:02:25', NULL, 1, '377752', 0, ''),
(22, 'A new thread', 'This is the body of the new thread.', '2013-09-26 10:58:01', NULL, 1, '47943', 0, 'Green Eggs and Ham');

-- --------------------------------------------------------

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
CREATE TABLE IF NOT EXISTS `User` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) COLLATE utf8_bin NOT NULL,
  `password` varchar(255) COLLATE utf8_bin NOT NULL,
  `display_hash` varchar(255) COLLATE utf8_bin NOT NULL COMMENT 'User identifier to be displayed instead of PK',
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login` timestamp NULL DEFAULT NULL,
  `email` varchar(255) COLLATE utf8_bin NOT NULL,
  `is_admin` tinyint(1) NOT NULL DEFAULT '0',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  `icon` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username_2` (`username`),
  UNIQUE KEY `username_3` (`username`),
  UNIQUE KEY `display_hash_2` (`display_hash`),
  KEY `display_hash` (`display_hash`),
  KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Forum users' AUTO_INCREMENT=14 ;

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`user_id`, `username`, `password`, `display_hash`, `date_created`, `last_login`, `email`, `is_admin`, `is_deleted`, `icon`) VALUES
(11, 'aaaa', '$pbkdf2-sha512$12000$jTFmjDGmtNba./8/ByBkDA$deujNGrqOI2EpjwB07zucUEyAnlS2CqMBF6Gx65cW5VH.gGpCRYaxx4LncBOtWd4zIDq7Yb9tSmTlkk.ioEd5w', '280711', '2013-09-24 22:11:34', NULL, 'eee@eee.com', 0, 0, NULL),
(13, 'bbb', '$pbkdf2-sha512$12000$SsnZu5eytpaytpaSkvKe8w$WeoZzMMmcFe5Gm1CRy0fgzBOxfl.wbrm9wZxZCGZGmafeUGk.zaoDpcxPcVDumjnmanFevUohs4kkS2pBKu9DQ', '330825', '2013-09-24 22:46:04', NULL, 'bbb@bbb.com', 0, 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `User_Category`
--

DROP TABLE IF EXISTS `User_Category`;
CREATE TABLE IF NOT EXISTS `User_Category` (
  `category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`category_id`,`user_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Post`
--
ALTER TABLE `Post`
  ADD CONSTRAINT `Post_ibfk_3` FOREIGN KEY (`thread_id`) REFERENCES `Thread` (`thread_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Post_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `User` (`user_id`);

--
-- Constraints for table `Thread`
--
ALTER TABLE `Thread`
  ADD CONSTRAINT `Thread_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `User` (`user_id`),
  ADD CONSTRAINT `Thread_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `Category` (`category_id`);

--
-- Constraints for table `User_Category`
--
ALTER TABLE `User_Category`
  ADD CONSTRAINT `User_Category_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `Category` (`category_id`),
  ADD CONSTRAINT `User_Category_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

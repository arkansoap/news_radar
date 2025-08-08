CREATE TABLE `news_radar_X_post` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `username` varchar(255) NOT NULL,
  `text` text NOT NULL,
  `link` varchar(255) NOT NULL,
  `date` timestamp NOT NULL
);

ALTER TABLE `news_radar_X_post`
ADD UNIQUE `link` (`link`);
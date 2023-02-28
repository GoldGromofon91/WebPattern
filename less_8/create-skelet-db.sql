PRAGMA
foreign_keys = off;
BEGIN
TRANSACTION;

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    username VARCHAR(32),
    type VARCHAR(32)
);

COMMIT TRANSACTION;
PRAGMA
foreign_keys = on;
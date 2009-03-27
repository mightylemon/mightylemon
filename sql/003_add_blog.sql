/*
-- Used for adding "blog" support to oebfare

-- SQLITE

BEGIN TRANSACTION;
CREATE TEMPORARY TABLE blogs_backup(id, title, slug, body, active, create_date, pub_date, tags);
DROP TABLE blog_post;
CREATE TABLE blog_post(
    "id" integer NOT NULL PRIMARY KEY,
    "title" varchar(100) NOT NULL,
    "slug" varchar(50) NOT NULL UNIQUE,
    "body" text NOT NULL,
    "active" bool NOT NULL,
    "create_date" datetime NOT NULL,
    "pub_date" datetime NOT NULL,
    "tags" varchar(255) NOT NULL,
    "blog_id" integer NOT NULL
);
INSERT INTO blog_post SELECT id,title,slug,body,active,create_date,pub_date,tags,1 FROM blogs_backup;
DROP TABLE blogs_backup;
COMMIT;

-- END SQLITE
-- POSTGRESQL

ALTER TABLE blog_post ADD COLUMN blog_id integer;
ALTER TABLE blog_post ALTER COLUMN blog_id SET DEFAULT 1;
UPDATE blog_post SET blog_id = 1;

-- END POSTGRESQL
*/


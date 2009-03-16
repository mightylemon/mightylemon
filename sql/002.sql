-- this sql is for anyone who used oebfare before the recent changes by
-- myself and leah culver. this keeps things compatible (hence the rst default).
ALTER TABLE blog_post ADD COLUMN markup_type character varying(10) NOT NULL DEFAULT 'rst';
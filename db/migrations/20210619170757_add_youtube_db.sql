-- migrate:up
CREATE TABLE youtube_vids(
    id char(11) NOT NULL PRIMARY KEY,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    title text NOT NULL,
    description text NOT NULL,
    thumbnail text NOT NULL,
    published_at timestamp without time zone NOT NULL
);

-- migrate:down

DROP TABLE youtube_vids;
CREATE TABLE IF NOT EXISTS views
(
    film_id          UUID NOT NULL,
    user_id          INTEGER NOT NULL,
    film_position_ms INTEGER NOT NULL
);
CREATE
INDEX views_film_user_idx ON views (film_id, user_id);

COPY views FROM '/views_data.csv'
WITH (FORMAT csv, HEADER);
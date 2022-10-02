CREATE TABLE IF NOT EXISTS views
(
    film_id          UUID,
    user_id          UInt64,
    film_position_ms UInt32
)
    ENGINE = MergeTree()
        ORDER BY (film_id, user_id);

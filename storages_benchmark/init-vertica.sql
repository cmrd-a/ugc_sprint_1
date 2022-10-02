CREATE TABLE IF NOT EXISTS views
(
    film_id UUID,
    user_id INTEGER,
    film_position_ms   INTEGER
);

COPY views FROM LOCAL '/views_data.csv' DELIMITER ',';

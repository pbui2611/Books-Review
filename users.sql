CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    t_email VARCHAR(128) NULL,
    t_password VARCHAR(128) NULL,
    t_name_user VARCHAR(64) NULL
);

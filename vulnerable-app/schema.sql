DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL
);

-- password_hash values are fabricated placeholder strings in valid bcrypt
-- format, not derived from any real password.
INSERT INTO users (username, email, password_hash) VALUES
    ('alice', 'alice@example.com', '$2b$12$e0MYzXyjpJS7Pd0RVvHwHeFmH6VXAcgkYJp6X2HqW0zAKgIE4CyzS'),
    ('bob', 'bob@example.com', '$2b$12$KIXQ0z3vY2sVJZ2p1oQxHOo7t0EaW6uP4c5Bq2R8FvW1lY9nD3sZa'),
    ('admin', 'admin@example.com', '$2b$12$Zq8vT1nC4dR6yU2pS0mIeuJ4bV7wA9xK3fH5jN8oP1qL2rT6yB4cW');

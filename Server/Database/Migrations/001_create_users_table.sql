CREATE TABLE users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    google_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) NOT NULL,
    telegram_id BIGINT UNIQUE,
    telegram_username VARCHAR(255),
    telegram_linked_at TIMESTAMP WITH TIME ZONE,
    calendar_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    telegram_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_users_google_id ON users(google_id);

CREATE INDEX idx_users_telegram_id ON users(telegram_id);
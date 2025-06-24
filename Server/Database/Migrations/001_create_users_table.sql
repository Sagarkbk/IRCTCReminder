CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    google_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    telegram_id BIGINT UNIQUE,
    telegram_username VARCHAR(255),
    telegram_linked_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'Asia/Kolkata'),
    is_active BOOLEAN DEFAULT TRUE,
    reminder_days INTEGER DEFAULT 1 CHECK (reminder_days IN (1, 2)),
    calendar_enabled BOOLEAN DEFAULT FALSE,
    telegram_enabled BOOLEAN DEFAULT FALSE,
    preferences_updated_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'Asia/Kolkata')
);

CREATE INDEX idx_users_google_id ON users(google_id);

CREATE INDEX idx_users_telegram_id ON users(telegram_id);
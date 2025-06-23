CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    google_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    telegram_id BIGINT UNIQUE, -- Can be NULL until user links Telegram
    telegram_username VARCHAR(255),
    telegram_linked_at TIMESTAMP WITH TIME ZONE, -- Track when Telegram was linked
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'Asia/Kolkata'),
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Global reminder preferences
    reminder_days INTEGER DEFAULT 1 CHECK (reminder_days IN (1, 2)), -- 1 = only release day, 2 = release day + day before
    calendar_enabled BOOLEAN DEFAULT FALSE,
    telegram_enabled BOOLEAN DEFAULT FALSE,
    preferences_updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_google_id ON users(google_id);

CREATE INDEX idx_users_telegram_id ON users(telegram_id);
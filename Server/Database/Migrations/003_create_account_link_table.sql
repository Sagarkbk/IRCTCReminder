CREATE TABLE google_telegram_link (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(50) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'Asia/Kolkata')
);

CREATE INDEX idx_google_telegram_link_token ON google_telegram_link(token);

CREATE INDEX idx_google_telegram_link_expires ON google_telegram_link(expires_at);
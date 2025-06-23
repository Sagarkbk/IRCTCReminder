CREATE TABLE selected_holidays (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    holiday_name VARCHAR(255) NOT NULL,
    holiday_date DATE NOT NULL,
    category VARCHAR(100), -- from the API response
    day_before_sent BOOLEAN DEFAULT FALSE, -- 61 days before holiday
    release_day_sent BOOLEAN DEFAULT FALSE, -- 60 days before holiday
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'Asia/Kolkata')
);

CREATE INDEX idx_selected_holidays_user_id ON selected_holidays(user_id);

CREATE INDEX idx_selected_holidays_date ON selected_holidays(holiday_date);

CREATE UNIQUE INDEX idx_selected_holidays_unique ON selected_holidays(user_id, holiday_date, holiday_name);
CREATE TABLE selected_holidays (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    holiday_name VARCHAR(255) NOT NULL,
    holiday_date DATE NOT NULL,
    category VARCHAR(100),
    day_before_sent BOOLEAN DEFAULT FALSE,
    release_day_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_holiday_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_selected_holidays_user_id ON selected_holidays(user_id);

CREATE INDEX idx_selected_holidays_date ON selected_holidays(holiday_date);

CREATE UNIQUE INDEX idx_selected_holidays_unique ON selected_holidays(user_id, holiday_date, holiday_name);
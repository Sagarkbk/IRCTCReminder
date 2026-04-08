CREATE TABLE journeys (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    journey_name VARCHAR(255) NOT NULL,
    journey_date DATE NOT NULL,
    google_calendar_event_id_release_date VARCHAR(255),
    google_calendar_event_id_day_before_release VARCHAR(255),
    release_day_date DATE NOT NULL,
    day_before_release_date DATE NOT NULL,
    reminder_on_release_day BOOLEAN NOT NULL DEFAULT FALSE,
    reminder_on_day_before BOOLEAN NOT NULL DEFAULT FALSE,
    sent_telegram_reminder_release_day TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    sent_telegram_reminder_day_before TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_updated_at TIMESTAMP WITH TIME ZONE
);

CREATE UNIQUE INDEX idx_journeys_unique ON journeys(user_id, journey_date, journey_name);

CREATE INDEX idx_journeys_user_id ON journeys(user_id);

CREATE INDEX idx_release_day_date ON journeys(release_day_date);

CREATE INDEX idx_day_before_release_date ON journeys(day_before_release_date);
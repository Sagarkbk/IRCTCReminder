CREATE TABLE journeys (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    journey_name VARCHAR(255) NOT NULL,
    journey_date DATE NOT NULL,
    category VARCHAR(100),
    reminder_on_release_day BOOLEAN NOT NULL DEFAULT FALSE,
    reminder_on_day_before BOOLEAN NOT NULL DEFAULT FALSE,
    release_day_date DATE,
    day_before_release_date DATE,
    sent_reminder_release_day BOOLEAN NOT NULL DEFAULT FALSE,
    sent_reminder_day_before BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_journeys_user_id ON journeys(user_id);

CREATE INDEX idx_journeys_date ON journeys(journey_date);

CREATE UNIQUE INDEX idx_journeys_unique ON journeys(user_id, journey_date, journey_name);
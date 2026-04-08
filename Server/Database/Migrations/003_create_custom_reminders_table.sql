CREATE TABLE custom_reminders(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    journey_id BIGINT NOT NULL REFERENCES journeys(id) ON DELETE CASCADE,
    reminder_date DATE NOT NULL,
    google_calendar_event_id_custom_date VARCHAR(255),
    sent_telegram_reminder_custom_day TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_customer_reminders_unique ON custom_reminders(journey_id, reminder_date);

CREATE INDEX idx_customer_reminders_journey_id ON custom_reminders(journey_id);

CREATE INDEX idx_custom_reminders_telegram_sent ON custom_reminders(reminder_date, sent_telegram_reminder_custom_day);
import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

export interface CustomReminder {
  journey_id: number;
  reminder_date: string;
}

export interface Journey {
  id: number;
  journey_name: string;
  journey_date: string;
  release_day_date: string;
  day_before_release_date: string;
  reminder_on_release_day: boolean;
  reminder_on_day_before: boolean;
  custom_reminders: CustomReminder[];
}

interface JourneyState {
  journeys: Journey[];
  isLoading: boolean;
  error: string | null;
}

const initialState: JourneyState = {
  journeys: [],
  isLoading: false,
  error: null,
};

const journeySlice = createSlice({
  name: "journey",
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },

    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },

    setJourneys: (state, action: PayloadAction<Journey[]>) => {
      state.journeys = action.payload;
    },

    addJourney: (state, action: PayloadAction<Journey>) => {
      state.journeys.push(action.payload);
    },

    deleteJourney: (state, action: PayloadAction<number>) => {
      state.journeys = state.journeys.filter(
        (journey) => journey.id !== action.payload,
      );
    },

    updateJourney: (state, action: PayloadAction<Journey>) => {
      const index = state.journeys.findIndex(
        (journey) => journey.id === action.payload.id,
      );
      if (index !== -1) {
        state.journeys[index] = action.payload;
      }
    },
  },
});

export const {
  setLoading,
  setError,
  setJourneys,
  addJourney,
  deleteJourney,
  updateJourney,
} = journeySlice.actions;

export default journeySlice.reducer;

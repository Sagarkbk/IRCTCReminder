import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

export interface Stats {
  total_journeys: number;
  completed_journeys: number;
  yet_to_complete_journeys: number;
}

interface StatsState {
  stats: Stats | null;
  isLoading: boolean;
  error: string | null;
}

const initialStats = {
  total_journeys: 0,
  completed_journeys: 0,
  yet_to_complete_journeys: 0,
};

const initialState: StatsState = {
  stats: initialStats,
  isLoading: false,
  error: null,
};

const statsSlice = createSlice({
  name: "stats",
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },

    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },

    setStats: (state, action: PayloadAction<Stats>) => {
      state.stats = action.payload;
      state.isLoading = false;
      state.error = null;
    },
  },
});

export const { setLoading, setError, setStats } = statsSlice.actions;

export default statsSlice.reducer;

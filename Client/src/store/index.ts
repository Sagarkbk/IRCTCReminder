import { configureStore } from "@reduxjs/toolkit";

import authReducer from "./slices/authSlice";
import statsReducer from "./slices/statsSlice";
import journeyReducer from "./slices/journeySlice";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    stats: statsReducer,
    journey: journeyReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;

export type AppDispatch = typeof store.dispatch;

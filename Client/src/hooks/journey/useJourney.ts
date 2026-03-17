import { useAppDispatch, useAppSelector } from "../../store/hooks";
import {
  setLoading,
  setError,
  setJourneys,
  addJourney,
  deleteJourney,
  updateJourney,
} from "../../store/slices/journeySlice";
import apiClient from "../../api/apiClient";
import { isAxiosError } from "axios";

interface Body {
  journey_name: string;
  journey_date: string;
  reminder_on_release_day: boolean;
  reminder_on_day_before: boolean;
  custom_reminders: string[];
}

export function useJourney() {
  const dispatch = useAppDispatch();
  const { journeys, isLoading, error } = useAppSelector(
    (state) => state.journey,
  );

  const fetchJourneys = async () => {
    try {
      dispatch(setLoading(true));
      const response = await apiClient.get(
        `${import.meta.env.VITE_API_URL}/journey/existing`,
      );
      dispatch(setJourneys(response.data.data));
    } catch (err) {
      if (isAxiosError(err)) {
        dispatch(
          setError(
            err.response?.data?.detail || "Failed to fetch existing journeys.",
          ),
        );
      } else {
        dispatch(setError("An unexpected error occurred."));
      }
    } finally {
      dispatch(setLoading(false));
    }
  };

  const addNewJourney = async (body: Body) => {
    try {
      dispatch(setLoading(true));
      const response = await apiClient.post(
        `${import.meta.env.VITE_API_URL}/journey/add`,
        body,
      );
      dispatch(addJourney(response.data.data));
    } catch (err) {
      if (isAxiosError(err)) {
        dispatch(
          setError(err.response?.data?.detail || "Failed to add new journey."),
        );
      } else {
        dispatch(setError("An unexpected error occurred."));
      }
    } finally {
      dispatch(setLoading(false));
    }
  };

  const removeExistingJourney = async (id: number) => {
    try {
      dispatch(setLoading(true));
      await apiClient.delete(
        `${import.meta.env.VITE_API_URL}/journey/delete?journey_id=${id}`,
      );
      dispatch(deleteJourney(id));
    } catch (err) {
      if (isAxiosError(err)) {
        dispatch(
          setError(err.response?.data?.detail || "Failed to delete journey."),
        );
      } else {
        dispatch(setError("An unexpected error occurred."));
      }
    } finally {
      dispatch(setLoading(false));
    }
  };

  const editJourney = async (id: number, body: Body) => {
    try {
      dispatch(setLoading(true));
      const response = await apiClient.put(
        `${import.meta.env.VITE_API_URL}/journey/update?journey_id=${id}`,
        body,
      );
      dispatch(updateJourney(response.data.data));
    } catch (err) {
      if (isAxiosError(err)) {
        dispatch(
          setError(err.response?.data?.detail || "Failed to update journey."),
        );
      } else {
        dispatch(setError("An unexpected error occurred."));
      }
    } finally {
      dispatch(setLoading(false));
    }
  };

  return {
    fetchJourneys,
    addNewJourney,
    removeExistingJourney,
    editJourney,
    journeys,
    isLoading,
    error,
  };
}

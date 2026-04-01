import { isAxiosError } from "axios";
import { useEffect } from "react";
import apiClient from "../../api/apiClient";
import { useAppDispatch } from "../../store/hooks";
import { setStats, setLoading, setError } from "../../store/slices/statsSlice";

export interface Stats {
  total_journeys: number;
  completed_journeys: number;
  yet_to_complete_journeys: number;
}

export function useJourneyStats() {
  const dispatch = useAppDispatch();

  useEffect(() => {
    const fetchJourneyStats = async () => {
      try {
        dispatch(setLoading(true));
        const response = await apiClient.get("/journey/journeyStats");
        dispatch(setStats(response.data.data));
      } catch (err) {
        if (isAxiosError(err)) {
          dispatch(
            setError(
              err.response?.data?.detail ||
                "Failed to fetch user journey statistics.",
            ),
          );
        } else {
          dispatch(setError("An unexpected error occurred."));
        }
      } finally {
        dispatch(setLoading(false));
      }
    };
    fetchJourneyStats();
  }, [dispatch]);

  return {};
}

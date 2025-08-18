import { isAxiosError } from "axios";
import { useEffect, useState } from "react";
import apiClient from "../../api/apiClient";

export interface Stats {
  total_journeys: number;
  completed_journeys: number;
  yet_to_complete_journeys: number;
}

export function useJourneyStats() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchJourneyStats = async () => {
      try {
        setIsLoading(true);
        const response = await apiClient.get(
          `${import.meta.env.VITE_API_URL}/journey/journeyStats`
        );
        setStats(response.data.data);
      } catch (err) {
        if (isAxiosError(err)) {
          setError(
            err.response?.data?.detail || "Failed to fetch user profile."
          );
        } else {
          setError("An unexpected error occurred.");
        }
      } finally {
        setIsLoading(false);
      }
    };
    fetchJourneyStats();
  }, []);

  return { stats, error, isLoading };
}

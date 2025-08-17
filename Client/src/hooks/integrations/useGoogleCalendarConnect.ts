import { isAxiosError } from "axios";
import { useState } from "react";
import apiClient from "../../api/apiClient";
import { useAuth } from "../auth/useAuth";

export function useGoogleCalendarConnect() {
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const { login } = useAuth();

  const connectCalendar = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await apiClient.put(
        `${import.meta.env.VITE_API_URL}/user/preferences`,
        {
          calendar_enabled: true,
        }
      );
      login(response.data.data);
    } catch (err) {
      if (isAxiosError(err)) {
        setError(err.response?.data?.detail || "Failed to fetch user profile.");
      } else {
        setError("An unexpected error occurred.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return { connectCalendar, error, isLoading };
}

import { useState } from "react";
import apiClient from "../../api/apiClient";
import { isAxiosError } from "axios";
import { useAuth } from "../auth/useAuth";

export function useTelegramConnect() {
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const { login } = useAuth();

  const connectTelegram = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await apiClient.put(
        `${import.meta.env.VITE_API_URL}/user/preferences`,
        {
          telegram_enabled: true,
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

  return { connectTelegram, error, isLoading };
}

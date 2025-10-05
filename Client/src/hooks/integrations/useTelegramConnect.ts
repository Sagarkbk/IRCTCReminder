import { useState } from "react";
import apiClient from "../../api/apiClient";
import { isAxiosError } from "axios";
// import { useAuth } from "../auth/useAuth";

export function useTelegramConnect() {
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [token, setToken] = useState<string | null>(null);
  // const { login } = useAuth();

  const generateToken = async () => {
    try {
      setIsLoading(true);
      setError(null);
      setToken(null);
      const response = await apiClient.post(
        `${import.meta.env.VITE_API_URL}/integration/telegram/generateToken`,
        {
          telegram_enabled: true,
        }
      );
      setToken(response.data.data);
      // login(response.data.data);
    } catch (err) {
      if (isAxiosError(err)) {
        setError(
          err.response?.data?.detail || "Failed to generate connection token."
        );
      } else {
        setError("An unexpected error occurred.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return { generateToken, token, error, isLoading };
}

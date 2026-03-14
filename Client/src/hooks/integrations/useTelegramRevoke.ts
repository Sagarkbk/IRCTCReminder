import { useState } from "react";
import apiClient from "../../api/apiClient";
import { isAxiosError } from "axios";
import { useAppDispatch } from "../../store/hooks";
import { login } from "../../store/slices/authSlice";

export function useTelegramRevoke() {
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const dispatch = useAppDispatch();

  const revokeTelegram = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await apiClient.put(
        `${import.meta.env.VITE_API_URL}/user/preferences`,
        {
          telegram_enabled: false,
        },
      );
      dispatch(login(response.data.data));
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

  return { revokeTelegram, error, isLoading };
}

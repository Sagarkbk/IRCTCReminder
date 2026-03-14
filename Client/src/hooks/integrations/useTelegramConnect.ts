import { useEffect, useState } from "react";
import apiClient from "../../api/apiClient";
import { isAxiosError } from "axios";
import { useAppDispatch } from "../../store/hooks";
import { login } from "../../store/slices/authSlice";

export function useTelegramConnect() {
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [token, setToken] = useState<string | null>(null);
  const dispatch = useAppDispatch();

  const reFetchUser = async () => {
    try {
      const response = await apiClient.get(
        `${import.meta.env.VITE_API_URL}/user/profile`,
      );
      dispatch(login(response.data.data));
    } catch (err) {
      console.error("Failed to refresh user profile:", err);
    }
  };

  useEffect(() => {
    const handleFocus = () => {
      reFetchUser();
    };
    window.addEventListener("focus", handleFocus);
    return () => document.removeEventListener("focus", handleFocus);
  }, []);

  const generateToken = async () => {
    try {
      setIsLoading(true);
      setError(null);
      setToken(null);
      const response = await apiClient.post(
        `${import.meta.env.VITE_API_URL}/integration/telegram/generateToken`,
        {
          telegram_enabled: true,
        },
      );
      setToken(response.data.data);
      // login(response.data.data);
    } catch (err) {
      if (isAxiosError(err)) {
        setError(
          err.response?.data?.detail || "Failed to generate connection token.",
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

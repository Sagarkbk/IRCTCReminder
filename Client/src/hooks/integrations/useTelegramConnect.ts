import { useEffect, useState, useCallback } from "react";
import apiClient from "../../api/apiClient";
import { isAxiosError } from "axios";
import { useAppDispatch } from "../../store/hooks";
import { login } from "../../store/slices/authSlice";

export function useTelegramConnect() {
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [token, setToken] = useState<string | null>(null);
  const [shouldRefetch, setShouldRefetch] = useState(false);
  const dispatch = useAppDispatch();

  const reFetchUser = useCallback(async () => {
    try {
      const response = await apiClient.get("/user/profile");
      dispatch(login(response.data.data));
    } catch (err) {
      console.error("Failed to refresh user profile:", err);
    }
  }, [dispatch]);

  useEffect(() => {
    if (!shouldRefetch) return;

    const handleFocus = () => {
      reFetchUser();
      setShouldRefetch(false);
    };
    window.addEventListener("focus", handleFocus);
    return () => window.removeEventListener("focus", handleFocus);
  }, [shouldRefetch]);

  const generateToken = async () => {
    try {
      setIsLoading(true);
      setShouldRefetch(true);
      setError(null);
      setToken(null);
      const response = await apiClient.post(
        "/integration/telegram/generateToken",
      );
      setToken(response.data.data);
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

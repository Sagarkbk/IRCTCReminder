import { isAxiosError } from "axios";
import { useEffect, useState } from "react";
import apiClient from "../../api/apiClient";

interface UserProfile {
  id: number;
  email: string;
  username: string;
  calendar_enabled: boolean;
  telegram_enabled: boolean;
}

export function useUserProfile() {
  const [userData, setUserData] = useState<UserProfile | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const response = await apiClient.get("/user/profile");
        setUserData(response.data.data);
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

    fetchUserProfile();
  }, []);

  return { userData, error, isLoading };
}

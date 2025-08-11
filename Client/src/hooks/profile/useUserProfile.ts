import { isAxiosError } from "axios";
import { useEffect, useState } from "react";
import apiClient from "../../api/apiClient";

export function useUserProfile() {
  const [data, setData] = useState(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const response = await apiClient.get("/user/profile");
        setData(response.data.data);
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

  return { data, error, isLoading };
}

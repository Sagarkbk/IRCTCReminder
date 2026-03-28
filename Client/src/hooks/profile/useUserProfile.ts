import { isAxiosError } from "axios";
import { useEffect } from "react";
import apiClient from "../../api/apiClient";
import { useAppDispatch, useAppSelector } from "../../store/hooks";
import { login } from "../../store/slices/authSlice";

export function useUserProfile() {
  const dispatch = useAppDispatch();
  const { isAuthenticated } = useAppSelector((state) => state.auth);

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        if (!isAuthenticated) return;

        const response = await apiClient.get("/user/profile");
        dispatch(login(response.data.data));
      } catch (err) {
        if (isAxiosError(err)) {
          console.log(
            err.response?.data?.detail || "Failed to fetch user profile.",
          );
        } else {
          console.log("An unexpected error occurred.");
        }
      }
    };

    fetchUserProfile();
  }, [isAuthenticated, dispatch]);
}

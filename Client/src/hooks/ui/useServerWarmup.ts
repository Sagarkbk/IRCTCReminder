import { useEffect } from "react";
import apiClient from "../../api/apiClient";

export function useServerWarmup() {
  useEffect(() => {
    const warmUp = async () => {
      try {
        await apiClient.get("/health/app");
        console.log("Server wakeup signal sent.");
      } catch (error) {
        console.log("Server warmup ping attempted.");
      }
    };

    warmUp();
  }, []);
}

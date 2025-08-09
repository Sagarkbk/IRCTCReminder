import { useGoogleLogin } from "@react-oauth/google";
import axios from "axios";

export function useGoogleAuth() {
  const handleGoogleAuth = useGoogleLogin({
    onSuccess: async (codeResponse) => {
      try {
        const { code } = codeResponse;
        const response = await axios.post(
          `${import.meta.env.VITE_API_URL}/api/auth/google`,
          {
            authCode: code,
            clientId: import.meta.env.VITE_WEB_CLIENT_ID,
          }
        );
        console.log(response.data);
      } catch (error) {
        console.error("Login/Signup failed:", error);
      }
    },
    flow: "auth-code",
    scope: "https://www.googleapis.com/auth/calendar.events",
  });
  return { handleGoogleAuth };
}

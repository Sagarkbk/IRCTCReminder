import { useGoogleLogin } from "@react-oauth/google";
import axios from "axios";
import { useAppDispatch } from "../../store/hooks";
import { login, setLoading, setError } from "../../store/slices/authSlice";

export function useGoogleAuth() {
  const dispatch = useAppDispatch();

  const handleGoogleAuth = useGoogleLogin({
    onSuccess: async (codeResponse) => {
      try {
        dispatch(setLoading(true));
        dispatch(setError(null));
        const { code } = codeResponse;
        const response = await axios.post(
          `${import.meta.env.VITE_API_URL}/auth/google`,
          {
            authCode: code,
            clientId: import.meta.env.VITE_WEB_CLIENT_ID,
          },
        );
        const data = response.data.data;
        const user = data.user;
        console.log(data);
        localStorage.setItem("jwt_token", data.token);
        dispatch(login(user));
      } catch (error) {
        console.error("Login/Signup failed:", error);
        dispatch(setError("Authentication failed. Please try again."));
      } finally {
        dispatch(setLoading(false));
      }
    },
    flow: "auth-code",
    scope: "https://www.googleapis.com/auth/calendar.events",
  });
  return { handleGoogleAuth };
}

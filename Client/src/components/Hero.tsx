import { useGoogleLogin } from "@react-oauth/google";
import axios from "axios";

export function Hero() {
  const handleGoogleLogin = useGoogleLogin({
    onSuccess: async (codeResponse) => {
      try {
        const { code } = codeResponse;
        const response = await axios.post("/api", {
          authCode: code,
          clientId: import.meta.env.VITE_WEB_CLIENT_ID,
        });
        console.log(response.data);
      } catch (error) {
        console.error("Login/Signup failed:", error);
      }
    },
    flow: "auth-code",
  });

  return (
    <section
      id="hero"
      className="h-screen flex flex-col items-center justify-center text-center px-4 sm:px-6 lg:px-8 bg-slate-900"
    >
      <div className="max-w-3xl">
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 to-teal-500">
          Never Miss Your IRCTC Booking Window Again
        </h1>

        <p className="mt-6 max-w-2xl mx-auto text-xl text-slate-300">
          Get automated reminders for train ticket bookings with precise timing.
          Stay informed about your travel plans without the stress.
        </p>
      </div>

      <div className="mt-8 flex flex-wrap justify-center gap-4">
        <button
          className="px-8 py-3 font-semibold text-white bg-transparent border-2 border-indigo-500 rounded-full shadow-lg transform transition-all duration-300 ease-in-out hover:scale-105 hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 focus:ring-offset-slate-900 cursor-pointer"
          onClick={() => handleGoogleLogin()}
        >
          Sign In with Google
        </button>
        <a
          className="px-8 py-3 font-semibold text-white bg-transparent border-2 border-emerald-500 rounded-full shadow-lg transform transition-all duration-300 ease-in-out hover:scale-105 hover:bg-emerald-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 focus:ring-offset-slate-900 cursor-pointer"
          onClick={(e) => {
            e.preventDefault();
            document
              .getElementById("demo")
              ?.scrollIntoView({ behavior: "smooth" });
          }}
        >
          Watch Demo
        </a>
      </div>
    </section>
  );
}

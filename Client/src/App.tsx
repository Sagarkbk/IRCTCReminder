import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Landing } from "./pages/Landing";
import { Home } from "./pages/Home";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { Profile } from "./pages/Profile";
import { useAppSelector } from "./store/hooks";

const AppRoutes = () => {
  const { isAuthenticated, isLoading, error } = useAppSelector(
    (state) => state.auth,
  );

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-slate-900 text-white">
        Loading...
      </div>
    );
  }

  return (
    <>
      {error && (
        <div className="fixed top-0 left-0 right-0 bg-red-600 text-white p-3 text-center z-50">
          {error}
        </div>
      )}
      <Routes>
        {isAuthenticated ? (
          <>
            <Route path="/" element={<Home />} />
            <Route path="/profile" element={<Profile />} />
          </>
        ) : (
          <Route path="/" element={<Landing />} />
        )}
      </Routes>
    </>
  );
};

function App() {
  const webClientId = import.meta.env.VITE_WEB_CLIENT_ID || "";

  return (
    <GoogleOAuthProvider clientId={webClientId}>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </GoogleOAuthProvider>
  );
}

export default App;

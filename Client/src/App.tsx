import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Landing } from "./pages/Landing";
import { Home } from "./pages/Home";
import { useCheckAuth } from "./hooks/useCheckAuth";
import { GoogleOAuthProvider } from "@react-oauth/google";

function App() {
  const { isAuthenticated } = useCheckAuth();
  const webClientId = import.meta.env.VITE_WEB_CLIENT_ID || "";

  return (
    <GoogleOAuthProvider clientId={webClientId}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={isAuthenticated ? <Home /> : <Landing />} />
        </Routes>
      </BrowserRouter>
    </GoogleOAuthProvider>
  );
}

export default App;

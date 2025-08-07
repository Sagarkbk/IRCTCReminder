import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Landing } from "./pages/Landing";
import { Home } from "./pages/Home";
import { useCheckAuth } from "./hooks/useCheckAuth";

function App() {
  const { isAuthenticated } = useCheckAuth();

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={isAuthenticated ? <Home /> : <Landing />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

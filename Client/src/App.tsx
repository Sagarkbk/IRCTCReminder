import "./App.css";
import { Features } from "./components/Features";
import { Hero } from "./components/Hero";
import { HowItWorks } from "./components/HowItWorks";
import { PublicNavbar } from "./components/PublicNavbar";

function App() {
  return (
    <>
      <PublicNavbar />
      <Hero />
      <HowItWorks />
      <Features />
    </>
  );
}

export default App;

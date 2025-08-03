import "./App.css";
import { Demo } from "./components/Demo";
import { Features } from "./components/Features";
import { Hero } from "./components/Hero";
import { HowItWorks } from "./components/HowItWorks";
import { PublicNavbar } from "./components/PublicNavbar";

function App() {
  return (
    <>
      <PublicNavbar />
      <Hero />
      <Demo />
      <HowItWorks />
      <Features />
    </>
  );
}

export default App;

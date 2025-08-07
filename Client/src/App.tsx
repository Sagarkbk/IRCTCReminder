import "./App.css";
import { Demo } from "./components/Demo";
import { Hero } from "./components/Hero";
import { HowItWorks } from "./components/HowItWorks";
import { PublicNavbar } from "./components/PublicNavbar";
import { PublicFooter } from "./components/PublicFooter";

function App() {
  return (
    <div>
      <PublicNavbar />
      <main>
        <Hero />
        <Demo />
        <HowItWorks />
      </main>
      <PublicFooter />
    </div>
  );
}

export default App;

import { PublicNavbar } from "../components/PublicNavbar";
import { Hero } from "../components/Hero";
import { Demo } from "../components/Demo";
import { HowItWorks } from "../components/HowItWorks";
import { PublicFooter } from "../components/PublicFooter";

export function Landing() {
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

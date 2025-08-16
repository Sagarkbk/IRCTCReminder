import { type User } from "../context/AuthContext";
import { IntegrationCard } from "./IntegrationCard";

export function AccountIntegrations({ user }: { user: User }) {
  if (!user) {
    return null;
  }

  return (
    <section>
      <h2 className="text-2xl font-semibold border-b-2 border-slate-700 pb-2 mb-6">
        Integrations
      </h2>

      <IntegrationCard
        cardName={"Google Calendar"}
        isEnabled={user.calendar_enabled}
      />
      <IntegrationCard
        cardName={"Telegram"}
        isEnabled={user.telegram_enabled}
      />
    </section>
  );
}

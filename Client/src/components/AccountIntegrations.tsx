import { type User } from "../context/AuthContext";
import { useGoogleCalendarConnect } from "../hooks/integrations/useGoogleCalendarConnect";
import { useGoogleCalendarRevoke } from "../hooks/integrations/useGoogleCalendarRevoke";
import { useTelegramConnect } from "../hooks/integrations/useTelegramConnect";
import { useTelegramRevoke } from "../hooks/integrations/useTelegramRevoke";
import { IntegrationCard } from "./IntegrationCard";

export function AccountIntegrations({ user }: { user: User }) {
  if (!user) {
    return null;
  }

  const { connectCalendar, isLoading: calendarConnectLoading } =
    useGoogleCalendarConnect();
  const { revokeCalendar, isLoading: CalendarRevokeLoading } =
    useGoogleCalendarRevoke();

  const { connectTelegram, isLoading: telegramConnectLoading } =
    useTelegramConnect();
  const { revokeTelegram, isLoading: telegramRevokeLoading } =
    useTelegramRevoke();

  return (
    <section>
      <h2 className="text-2xl font-semibold border-b-2 border-slate-700 pb-2 mb-6">
        Integrations
      </h2>

      <IntegrationCard
        cardName={"Google Calendar"}
        isEnabled={user.calendar_enabled}
        onConnect={connectCalendar}
        onRevoke={revokeCalendar}
        connectLoading={calendarConnectLoading}
        revokeLoading={CalendarRevokeLoading}
      />
      <IntegrationCard
        cardName={"Telegram"}
        isEnabled={user.telegram_enabled}
        onConnect={connectTelegram}
        onRevoke={revokeTelegram}
        connectLoading={telegramConnectLoading}
        revokeLoading={telegramRevokeLoading}
      />
    </section>
  );
}

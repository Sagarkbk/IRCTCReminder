import { useState } from "react";
import { type User } from "../context/AuthContext";
import { useGoogleCalendarConnect } from "../hooks/integrations/useGoogleCalendarConnect";
import { useGoogleCalendarRevoke } from "../hooks/integrations/useGoogleCalendarRevoke";
import { useTelegramConnect } from "../hooks/integrations/useTelegramConnect";
import { useTelegramRevoke } from "../hooks/integrations/useTelegramRevoke";
import { IntegrationCard } from "./IntegrationCard";
import { Modal } from "./Modal";

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

  const [isModalOpen, setIsModalOpen] = useState(false);

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
        onConnect={() => setIsModalOpen(true)}
        onRevoke={revokeTelegram}
        connectLoading={telegramConnectLoading}
        revokeLoading={telegramRevokeLoading}
      />
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Connect Telegram"
      >
        <div className="p-4">
          <p className="text-slate-300 mb-4">
            This is a placeholder for the Telegram connection instructions.
          </p>
          <div className="flex justify-end space-x-2">
            <button
              onClick={() => setIsModalOpen(false)}
              className="px-4 py-2 rounded bg-slate-600 hover:bg-slate-700"
            >
              Close
            </button>
          </div>
        </div>
      </Modal>
    </section>
  );
}

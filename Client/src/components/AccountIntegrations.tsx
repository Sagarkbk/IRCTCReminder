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

  const {
    generateToken,
    token,
    isLoading: telegramConnectLoading,
  } = useTelegramConnect();
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
        title="Connect Telegram Account"
      >
        <div className="p-4 text-slate-300">
          {telegramConnectLoading ? (
            <p>Generating token, please wait...</p>
          ) : token ? (
            <div>
              <p className="mb-4 text-slate-300 text-center">
                A secure link has been generated. Click the button below to open
                Telegram and link your account.
              </p>
              <a
                href={`https://t.me/TicketBookingReminderBot?text=/link%20${token}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block w-full text-center px-4 py-3 rounded bg-cyan-600 hover:bg-cyan-700 text-white -bold transition-colors duration-200"
              >
                Connect via Telegram
              </a>
              <p className="text-sm text-slate-400 mt-4 text-center">
                This link is valid for 30 minutes.
              </p>
            </div>
          ) : (
            <>
              <p className="mb-4">
                Click the button below to generate a unique token. You will then
                send this token to the IRCTC Reminder Bot on Telegram to link
                your account.
              </p>
              <div className="flex justify-end">
                <button
                  onClick={generateToken}
                  className="px-4 py-2 rounded bg-indigo-600 hover:bg-indigo-700 text-white font-semibold"
                >
                  Generate Token
                </button>
              </div>
            </>
          )}
        </div>
      </Modal>
    </section>
  );
}

import { type User } from "../context/AuthContext";

export function AccountIntegrations({ user }: { user: User }) {
  if (!user) {
    return null;
  }

  return (
    <section>
      <h2 className="text-2xl font-semibold border-b-2 border-slate-700 pb-2 mb-6">
        Integrations
      </h2>

      <div className="bg-slate-800 rounded-lg p-6 shadow-lg mb-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-lg font-semibold">Google Calendar</p>
            <p className="text-sm text-slate-400">Connected</p>
          </div>
          <button className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg transition-colors duration-200 w-36  cursor-pointer">
            Revoke Access
          </button>
        </div>
      </div>

      <div className="bg-slate-800 rounded-lg p-6 shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-lg font-semibold">Telegram Bot</p>
            <p className="text-sm text-slate-400">Not Connected</p>
          </div>
          <button className="bg-sky-600 hover:bg-sky-700 text-white font-bold py-2 px-4 rounded-lg transition-colors duration-200 w-36 cursor-pointer">
            Connect
          </button>
        </div>
      </div>
    </section>
  );
}

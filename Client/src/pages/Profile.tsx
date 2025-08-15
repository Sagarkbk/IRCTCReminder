import { useAuth } from "../hooks/auth/useAuth";

export function Profile() {
  const { user } = useAuth();

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white p-4 sm:p-6 md:p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold bg-gradient-to-r from-cyan-400 to-blue-600 text-transparent bg-clip-text mb-8">
          Profile & Settings
        </h1>

        {/* User Information Section */}
        <section className="mb-8">
          <h2 className="text-2xl font-semibold border-b-2 border-slate-700 pb-2 mb-6">
            Account Information
          </h2>
          <div className="bg-slate-800 rounded-lg p-6 shadow-lg">
            <div className="flex flex-col sm:flex-row sm:items-center mb-4">
              <p className="w-32 text-slate-400">Name</p>
              <p className="text-lg">{user.username}</p>
            </div>
            <div className="flex flex-col sm:flex-row sm:items-center">
              <p className="w-32 text-slate-400">Email</p>
              <p className="text-lg">{user.email}</p>
            </div>
          </div>
        </section>
        <section className="mb-8">
          <h2 className="text-2xl font-semibold border-b-2 border-slate-700 pb-2 mb-6">
            Statistics
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            <div className="bg-slate-800 p-4 rounded-lg shadow-lg text-center">
              <p className="text-sm text-slate-400">Total Journeys</p>
              <p className="text-3xl font-bold">12</p>
            </div>
            <div className="bg-slate-800 p-4 rounded-lg shadow-lg text-center">
              <p className="text-sm text-slate-400">Completed Journeys</p>
              <p className="text-3xl font-bold">8</p>
            </div>
            <div className="bg-slate-800 p-4 rounded-lg shadow-lg text-center">
              <p className="text-sm text-slate-400">Upcoming Journeys</p>
              <p className="text-3xl font-bold">4</p>
            </div>
          </div>
        </section>

        {/* Integrations Section */}
        <section>
          <h2 className="text-2xl font-semibold border-b-2 border-slate-700 pb-2 mb-6">
            Integrations
          </h2>

          {/* Google Calendar Card */}
          <div className="bg-slate-800 rounded-lg p-6 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-lg font-semibold">Google Calendar</p>
                <p className="text-sm text-slate-400">Connected</p>
              </div>
              <button className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg transition-colors duration-200">
                Revoke Access
              </button>
            </div>
            <div className="flex items-center justify-between mt-4">
              <div>
                <p className="text-lg font-semibold">Telegram Bot</p>
                <p className="text-sm text-slate-400">Not Connected</p>
              </div>
              <button className="bg-sky-600 hover:bg-sky-700 text-white font-bold py-2 px-4 rounded-lg transition-colors duration-200">
                Connect
              </button>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

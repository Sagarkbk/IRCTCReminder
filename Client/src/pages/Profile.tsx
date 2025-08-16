import { AccountInfo } from "../components/AccountInfo";
import { AccountIntegrations } from "../components/AccountIntegrations";
import { AccountStatistics } from "../components/AccountStatistics";
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
        <AccountInfo user={user} />
        <AccountStatistics user={user} />
        <AccountIntegrations user={user} />
      </div>
    </div>
  );
}

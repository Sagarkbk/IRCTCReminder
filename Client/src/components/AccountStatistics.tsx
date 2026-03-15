import { type User } from "../store/slices/authSlice";
import { useAppSelector } from "../store/hooks";
import { useJourneyStats } from "../hooks/profile/useJourneyStats";

export function AccountStatistics({ user }: { user: User }) {
  if (!user) {
    return null;
  }

  useJourneyStats();

  const stats = useAppSelector((state) => state.stats.stats);

  return (
    <section className="mb-8">
      <h2 className="text-2xl font-semibold border-b-2 border-slate-700 pb-2 mb-6">
        Statistics
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        <div className="bg-slate-800 p-4 rounded-lg shadow-lg text-center">
          <p className="text-sm text-slate-400">Total Journeys</p>
          <p className="text-3xl font-bold">{stats?.total_journeys}</p>
        </div>
        <div className="bg-slate-800 p-4 rounded-lg shadow-lg text-center">
          <p className="text-sm text-slate-400">Completed Journeys</p>
          <p className="text-3xl font-bold">{stats?.completed_journeys}</p>
        </div>
        <div className="bg-slate-800 p-4 rounded-lg shadow-lg text-center">
          <p className="text-sm text-slate-400">Upcoming Journeys</p>
          <p className="text-3xl font-bold">
            {stats?.yet_to_complete_journeys}
          </p>
        </div>
      </div>
    </section>
  );
}

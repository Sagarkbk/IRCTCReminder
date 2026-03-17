import { HomeNavbar } from "../components/HomeNavbar";
import { JourneyList } from "../components/JourneyList";
import { useAppSelector } from "../store/hooks";

export function Home() {
  const { user, error, isLoading } = useAppSelector((state) => state.auth);

  if (isLoading) {
    return <div>Loading user profile...</div>;
  }

  if (error) {
    return <div className="text-red-500">Error: {error}</div>;
  }

  return (
    <div className="min-h-screen bg-slate-900">
      <HomeNavbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="mb-10">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-400 to-teal-400 text-transparent bg-clip-text">
            Welcome, {user?.username}
          </h1>
          <p className="text-slate-400 mt-2">
            Manage your train journey reminders in one place.
          </p>
        </div>

        <JourneyList />
      </main>
    </div>
  );
}

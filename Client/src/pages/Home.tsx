import { HomeNavbar } from "../components/HomeNavbar";
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
    <>
      <HomeNavbar />
      <div className="p-8 text-white bg-black">
        <h1 className="text-3xl font-bold">Welcome, {user?.username}</h1>
        {user ? (
          <div className="mt-4">
            <p>Email: {user.email}</p>
            <p>User ID: {user.id}</p>
            <p>Calendar Enabled: {user.calendar_enabled ? "Yes" : "No"}</p>
            <p>Telegram Enabled: {user.telegram_enabled ? "Yes" : "No"}</p>
          </div>
        ) : (
          <p>No user data found.</p>
        )}
      </div>
    </>
  );
}

import { HomeNavbar } from "../components/HomeNavbar";
import { useUserProfile } from "../hooks/profile/useUserProfile";

export function Home() {
  const { userData, error, isLoading } = useUserProfile();

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
        <h1 className="text-3xl font-bold">Welcome, {userData?.username}</h1>
        {userData ? (
          <div className="mt-4">
            <p>Email: {userData.email}</p>
            <p>User ID: {userData.id}</p>
            <p>Calendar Enabled: {userData.calendar_enabled ? "Yes" : "No"}</p>
            <p>Telegram Enabled: {userData.telegram_enabled ? "Yes" : "No"}</p>
          </div>
        ) : (
          <p>No user data found.</p>
        )}
      </div>
    </>
  );
}

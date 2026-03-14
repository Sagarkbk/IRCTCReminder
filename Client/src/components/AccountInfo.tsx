import { type User } from "../store/slices/authSlice";

export function AccountInfo({ user }: { user: User }) {
  if (!user) {
    return null;
  }

  return (
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
  );
}

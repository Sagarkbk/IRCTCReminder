export function IntegrationCard({
  cardName,
  isEnabled,
  onConnect,
  onRevoke,
  revokeLoading,
  connectLoading,
}: {
  cardName: string;
  isEnabled: boolean;
  onConnect: () => void;
  onRevoke: () => void;
  revokeLoading: boolean;
  connectLoading: boolean;
}) {
  return (
    <div className="bg-slate-800 rounded-lg p-6 shadow-lg mb-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-lg font-semibold">{cardName}</p>
          <p className="text-sm text-slate-400">
            {isEnabled ? "Connected" : "Not Connected"}
          </p>
        </div>
        {isEnabled ? (
          <button
            className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg transition-colors duration-200 w-36  cursor-pointer"
            onClick={onRevoke}
          >
            {revokeLoading ? "Revoking..." : "Revoke Access"}
          </button>
        ) : (
          <button
            className="bg-sky-600 hover:bg-sky-700 text-white font-bold py-2 px-4 rounded-lg transition-colors duration-200 w-36 cursor-pointer"
            onClick={onConnect}
          >
            {connectLoading ? "Connecting..." : "Connect"}
          </button>
        )}
      </div>
    </div>
  );
}

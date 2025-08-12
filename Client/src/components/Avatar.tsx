export function Avatar({ name }: { name: string }) {
  const initial = name ? name.charAt(0).toUpperCase() : "?";

  return (
    <div className="relative inline-flex h-8 w-8 items-center justify-center overflow-hidden rounded-full bg-indigo-600">
      <span className="font-semibold text-white text-sm">{initial}</span>
    </div>
  );
}

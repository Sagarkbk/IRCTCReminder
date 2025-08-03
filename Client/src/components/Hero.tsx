export function Hero() {
  return (
    <section
      id="hero"
      className="h-screen flex flex-col items-center justify-center text-center px-4 sm:px-6 lg:px-8 bg-slate-50 dark:bg-slate-900"
    >
      <div className="max-w-3xl">
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-slate-800 dark:text-slate-200">
          Never Miss Your IRCTC Booking Window Again
        </h1>

        <p className="mt-4 text-lg sm:text-xl text-slate-600 dark:text-slate-400">
          Get automated reminders for train ticket bookings with precise timing.
          Stay informed about your travel plans without the stress.
        </p>
      </div>

      <div className="mt-8 flex flex-wrap justify-center gap-4">
        <button className="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-75 cursor-pointer">
          Sign In with Google
        </button>
        <a
          className="px-6 py-3 bg-emerald-600 text-white font-semibold rounded-lg shadow-md hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-opacity-75 cursor-pointer"
          onClick={(e) => {
            e.preventDefault();
            document
              .getElementById("demo")
              ?.scrollIntoView({ behavior: "smooth" });
          }}
        >
          Watch Demo
        </a>
      </div>
    </section>
  );
}

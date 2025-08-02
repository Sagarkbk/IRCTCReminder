export function Hero() {
  return (
    <section
      id="hero"
      className="h-screen flex flex-col items-center justify-center text-center px-4 sm:px-6 lg:px-8 bg-white dark:bg-black"
    >
      <div className="max-w-3xl">
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-gray-900 dark:text-white">
          Never Miss Your IRCTC Booking Window Again
        </h1>

        <p className="mt-4 text-lg sm:text-xl text-gray-600 dark:text-gray-300">
          Get automated reminders for train ticket bookings with precise timing.
          Stay informed about your travel plans without the stress.
        </p>
      </div>

      <div className="mt-8 flex flex-wrap justify-center gap-4">
        <button
          className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 
      focus:ring-blue-500 focus:ring-opacity-75 cursor-pointer"
        >
          Sign In with Google
        </button>
        <a
          href="#demo"
          className="px-6 py-3 bg-gray-200 text-gray-800 font-semibold rounded-lg shadow-md hover:bg-gray-300 dark:bg-gray-700 dark:text-white 
      dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-opacity-75"
        >
          Watch Demo
        </a>
      </div>
    </section>
  );
}

export function Demo() {
  return (
    <section
      id="demo"
      className="h-screen flex flex-col items-center justify-center text-center px-4 sm:px-6 lg:px-8 bg-slate-50 dark:bg-slate-900"
    >
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-extrabold text-slate-800 dark:text-slate-200">
            Watch How It Works
          </h2>
          <p className="mt-4 text-lg text-slate-600 dark:text-slate-400">
            See a step-by-step guide on how to use IRCTC Reminder to never miss
            a booking.
          </p>
        </div>
        <div className="max-w-4xl mx-auto">
          <iframe
            className="w-full aspect-video shadow-lg"
            src="https://www.youtube.com/embed/dQw4w9WgXcQ"
            title="YouTube video player"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          ></iframe>
        </div>
      </div>
    </section>
  );
}

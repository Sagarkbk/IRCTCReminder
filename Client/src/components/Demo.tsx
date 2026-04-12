export function Demo() {
  return (
    <section
      id="demo"
      className="flex flex-col items-center justify-center text-center px-4 py-24 sm:px-6 lg:px-8 bg-slate-900"
    >
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-600">
            Watch Demo
          </h2>
          <p className="mt-4 text-lg text-slate-300">
            See a step-by-step guide on how to use Rail Reminders to never miss
            a booking.
          </p>
        </div>
        <div className="max-w-4xl mx-auto">
          <iframe
            className="w-full aspect-video rounded-lg shadow-lg border-2 border-cyan-500 shadow-cyan-500/20"
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

export function PublicFooter() {
  return (
    <footer className="bg-slate-900 border-t border-slate-800">
      <div className="container mx-auto px-6 py-8">
        <div className="flex justify-center items-center">
          <nav className="flex space-x-6 sm:space-x-8 md:space-x-10">
            <a
              className="text-slate-400 hover:text-blue-400 cursor-pointer transition-colors duration-300"
              onClick={(e) => {
                e.preventDefault();
                document
                  .getElementById("hero")
                  ?.scrollIntoView({ behavior: "smooth" });
              }}
            >
              Home
            </a>
            <a
              className="text-slate-400 hover:text-blue-400 cursor-pointer transition-colors duration-300"
              onClick={(e) => {
                e.preventDefault();
                document
                  .getElementById("demo")
                  ?.scrollIntoView({ behavior: "smooth" });
              }}
            >
              Demo
            </a>
            <a
              className="text-slate-400 hover:text-blue-400 cursor-pointer transition-colors duration-300"
              onClick={(e) => {
                e.preventDefault();
                document
                  .getElementById("howitworks")
                  ?.scrollIntoView({ behavior: "smooth" });
              }}
            >
              How It Works
            </a>
          </nav>
        </div>
      </div>
    </footer>
  );
}

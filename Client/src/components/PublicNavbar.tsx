import { useState } from "react";
import { FiMenu, FiX } from "react-icons/fi";

export function PublicNavbar() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <>
      <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-800 shadow-lg grid grid-cols-3 items-center p-4 sm:px-6 md:px-8 lg:px-12">
        <a
          className="text-xl font-bold text-white hover:text-blue-400 cursor-pointer"
          onClick={(e) => {
            e.preventDefault();
            document
              .getElementById("hero")
              ?.scrollIntoView({ behavior: "smooth" });
          }}
        >
          Rail Reminders
        </a>
        <div className="hidden md:flex justify-center items-center gap-x-4 sm:gap-x-6">
          <a
            className="text-gray-300 text-base sm:text-lg hover:text-blue-400 cursor-pointer"
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
            className="text-gray-300 text-base sm:text-lg hover:text-blue-400 cursor-pointer"
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
            className="text-gray-300 text-base sm:text-lg hover:text-blue-400 cursor-pointer"
            onClick={(e) => {
              e.preventDefault();
              document
                .getElementById("howitworks")
                ?.scrollIntoView({ behavior: "smooth" });
            }}
          >
            How it works
          </a>
        </div>
        <div className="md:hidden flex justify-end items-center col-start-3">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="cursor-pointer"
          >
            {sidebarOpen ? (
              <FiX className="w-6 h-6 text-white" />
            ) : (
              <FiMenu className="w-6 h-6 text-white" />
            )}
          </button>
        </div>
      </nav>
      <div
        className={`fixed top-0 right-0 w-64 bg-gray-900 shadow-lg transform transition-transform duration-300 ease-in-out ${
          sidebarOpen ? "translate-x-0" : "translate-x-full"
        } md:hidden z-40`}
      >
        <div className="p-5 pt-16 mt-6 flex flex-col">
          <a
            className="text-gray-300 text-lg hover:text-blue-400 py-2 cursor-pointer"
            onClick={(e) => {
              e.preventDefault();
              setSidebarOpen(false);
              document
                .getElementById("hero")
                ?.scrollIntoView({ behavior: "smooth" });
            }}
          >
            Home
          </a>
          <a
            className="text-gray-300 text-lg hover:text-blue-400 py-2 cursor-pointer"
            onClick={(e) => {
              e.preventDefault();
              setSidebarOpen(false);
              document
                .getElementById("demo")
                ?.scrollIntoView({ behavior: "smooth" });
            }}
          >
            Demo
          </a>
          <a
            className="text-gray-300 text-lg hover:text-blue-400 py-2 cursor-pointer"
            onClick={(e) => {
              e.preventDefault();
              setSidebarOpen(false);
              document
                .getElementById("howitworks")
                ?.scrollIntoView({ behavior: "smooth" });
            }}
          >
            How it works
          </a>
        </div>
      </div>
    </>
  );
}

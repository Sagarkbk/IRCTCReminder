import { MdLightMode } from "react-icons/md";
import { MdDarkMode } from "react-icons/md";
import { useState } from "react";

export function PublicNavbar() {
  const [theme, setTheme] = useState<"Light" | "Dark">("Light");

  const toggleTheme = () => {
    setTheme(theme === "Light" ? "Dark" : "Light");
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white shadow-md p-4 dark:bg-gray-800 dark:shadow-lg flex items-center justify-between sm:px-6 md:px-8 lg:px-12">
      <a href="#" className="text-xl font-bold text-gray-900 dark:text-white">
        IRCTC Reminder
      </a>
      <div className="flex items-center gap-x-4 sm:gap-x-6">
        <a
          href="#home"
          className="text-gray-700 dark:text-gray-300 text-base sm:text-lg hover:text-blue-600 dark:hover:text-blue-400"
        >
          Home
        </a>
        <a
          href="#howitworks"
          className="text-gray-700 dark:text-gray-300 text-base sm:text-lg hover:text-blue-600 dark:hover:text-blue-400"
        >
          How it works
        </a>
        <a
          href="#features"
          className="text-gray-700 dark:text-gray-300 text-base sm:text-lg hover:text-blue-600 dark:hover:text-blue-400"
        >
          Features
        </a>
        <button
          onClick={toggleTheme}
          className="p-2 rounded-full text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700 flex items-center justify-center cursor-pointer"
        >
          {theme === "Light" ? (
            <MdDarkMode size={24} />
          ) : (
            <MdLightMode size={24} />
          )}
        </button>
      </div>
    </nav>
  );
}

import { MdLightMode } from "react-icons/md";
import { MdDarkMode } from "react-icons/md";
import { useState, useEffect } from "react";

export function PublicNavbar() {
  const [theme, setTheme] = useState<"light" | "dark">(() => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark" || savedTheme === "light") {
      return savedTheme;
    }
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      return "dark";
    }
    return "light";
  });

  useEffect(() => {
    const root = window.document.documentElement;
    if (theme === "dark") {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === "light" ? "dark" : "light"));
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white shadow-md p-4 dark:bg-gray-800 dark:shadow-lg flex items-center justify-between sm:px-6 md:px-8 lg:px-12">
      <a
        href="#"
        className="text-xl font-bold text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400"
      >
        IRCTC Reminder
      </a>
      <div className="flex items-center gap-x-4 sm:gap-x-6 mr-30">
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
      </div>
      <button
        onClick={toggleTheme}
        className="p-2 rounded-full text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700 flex items-center justify-center cursor-pointer"
      >
        {theme === "light" ? (
          <MdDarkMode size={24} />
        ) : (
          <MdLightMode size={24} />
        )}
      </button>
    </nav>
  );
}

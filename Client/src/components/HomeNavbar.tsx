import { FaChevronDown } from "react-icons/fa";
import { useAuth } from "../hooks/auth/useAuth";
import { useEffect, useRef, useState } from "react";
import { Avatar } from "./Avatar";
import { Link, useNavigate } from "react-router-dom";

export function HomeNavbar() {
  const { user, logout } = useAuth();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsDropdownOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <nav className="bg-slate-800 p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-white text-xl font-bold cursor-pointer">
          IRCTC Reminder
        </Link>
        <div className="relative" ref={dropdownRef}>
          {" "}
          <button
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            className="flex items-center space-x-2 text-white focus:outline-none cursor-pointer"
          >
            {user && <Avatar name={user.username} />}{" "}
            <span className="hidden md:block">{user?.username}</span>{" "}
            <FaChevronDown
              className={`ml-1 transition-transform duration-200 ${
                isDropdownOpen ? "rotate-180" : ""
              }`}
            />{" "}
          </button>
          {isDropdownOpen && (
            <div className="absolute right-2 top-full mt-1 bg-slate-700 rounded-md shadow-lg py-1 z-10 min-w-max max-w-xs lg:left-0">
              <Link
                to={"/profile"}
                className="block px-4 py-2 text-sm text-white hover:bg-slate-600"
              >
                Profile
              </Link>
              <button
                onClick={handleLogout}
                className="block w-full text-left px-4 py-2 text-sm text-white hover:bg-slate-600 cursor-pointer"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}

import { FaGoogle, FaPencilAlt, FaTelegramPlane, FaBell } from "react-icons/fa";
import { FiChevronRight } from "react-icons/fi";

export function HowItWorks() {
  const steps = [
    {
      icon: <FaGoogle className="w-8 h-8" />,
      title: "Sign In & Authorize",
      description:
        "Sign in with Google and grant one-time permission for calendar access.",
    },
    {
      icon: <FaPencilAlt className="w-8 h-8" />,
      title: "Add Your Journey",
      description: "Provide Journey Details to get reminded",
    },
    {
      icon: <FaTelegramPlane className="w-8 h-8" />,
      title: "Link Telegram (Optional)",
      description:
        "Connect your Telegram account to receive instant chat reminders.",
    },
    {
      icon: <FaBell className="w-8 h-8" />,
      title: "Get Automated Reminders",
      description:
        "Relax and receive timely alerts on your calendar and Telegram.",
    },
  ];

  return (
    <section
      id="howitworks"
      className="min-h-screen flex flex-col items-center md:justify-center bg-slate-50 dark:bg-slate-900 p-4 pt-24 md:pt-4 scroll-m-16"
    >
      <div className="text-center mb-4">
        <h2 className="text-3xl font-extrabold text-slate-800 dark:text-slate-200 sm:text-4xl">
          How It Works
        </h2>
        <p className="mt-4 text-lg text-slate-600 dark:text-slate-400">
          Get set up in just a few simple steps.
        </p>
      </div>

      <div className="flex flex-col md:flex-row items-stretch justify-center w-full max-w-xs sm:max-w-sm md:max-w-6xl space-y-8 md:space-y-0 md:space-x-4">
        {steps.map((step, index) => (
          <div key={index} className="flex items-center w-full">
            {/* Card: Added h-full to ensure it stretches */}
            <div
              className="flex flex-col items-center text-center p-6 bg-white dark:bg-slate-800 rounded-xl shadow-lg hover:shadow-2xl transition-shadow 
      duration-300 h-full w-full"
            >
              <div
                className="flex-shrink-0 flex items-center justify-center w-16 h-16 mb-4 bg-slate-100 dark:bg-slate-700 rounded-full text-blue-500 
      dark:text-blue-400"
              >
                {step.icon}
              </div>
              <div className="flex-grow">
                <h3 className="text-xl font-semibold text-slate-900 dark:text-slate-100">
                  {step.title}
                </h3>
                <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
                  {step.description}
                </p>
              </div>
            </div>

            {index < steps.length - 1 && (
              <div className="hidden md:flex px-4">
                <FiChevronRight className="w-8 h-8 text-slate-300 dark:text-slate-600" />
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}

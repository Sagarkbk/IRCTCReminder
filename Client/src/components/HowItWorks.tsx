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
      className="flex flex-col items-center justify-center text-center px-4 py-24 sm:px-6 lg:px-8 bg-slate-900"
    >
      <div className="text-center mb-4">
        <h2 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-blue-600 sm:text-4xl">
          How It Works
        </h2>
        <p className="mt-4 max-w-2xl mx-auto text-lg text-slate-300">
          Get set up in just a few simple steps.
        </p>
      </div>

      <div className="mt-16 flex flex-col md:flex-row items-stretch justify-center w-full max-w-xs sm:max-w-sm md:max-w-6xl space-y-8 md:space-y-0 md:space-x-4">
        {steps.map((step, index) => (
          <div key={index} className="flex items-center w-full">
            <div className="flex flex-col items-center text-center p-6 bg-slate-800 border border-slate-700 rounded-xl shadow-lg transition-transform duration-300 hover:-translate-y-1 hover:shadow-2xl h-full w-full">
              <div className="flex-shrink-0 flex items-center justify-center w-16 h-16 mb-4 bg-slate-700 rounded-full text-sky-400">
                {step.icon}
              </div>
              <div className="flex-grow">
                <h3 className="text-xl font-semibold text-slate-100">
                  {step.title}
                </h3>
                <p className="mt-2 text-sm text-slate-400">
                  {step.description}
                </p>
              </div>
            </div>

            {index < steps.length - 1 && (
              <div className="hidden md:flex px-4">
                <FiChevronRight className="w-8 h-8 text-slate-600" />
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}

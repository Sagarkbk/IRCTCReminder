import { Link } from "react-router-dom";
import { FaChevronLeft } from "react-icons/fa";

export function PrivacyPolicy() {
  return (
    <div className="min-h-screen bg-slate-900 text-slate-300 p-6 md:p-12">
      <div className="max-w-3xl mx-auto">
        <Link
          to="/"
          className="inline-flex items-center gap-2 text-indigo-400 hover:text-indigo-300 mb-8 transition-colors"
        >
          <FaChevronLeft size={14} /> Back to Home
        </Link>

        <h1 className="text-4xl font-bold text-white mb-2">
          Rail Reminders: Privacy Policy
        </h1>
        <p className="text-slate-500 mb-8 italic">
          Effective Date: April 12, 2026{" "}
        </p>

        <div className="space-y-8 leading-relaxed">
          <section>
            <h2 className="text-xl font-semibold text-white mb-3">
              1. Information We Collect
            </h2>
            <ul className="list-disc pl-5 space-y-2">
              <li>
                <strong className="text-slate-200">
                  Google Account Information:
                </strong>{" "}
                When you log in via Google, we receive your name, email address,
                and profile picture.
              </li>
              <li>
                <strong className="text-slate-200">
                  Telegram Information:
                </strong>{" "}
                When you link your Telegram account, we store your Telegram User
                ID and username to send you notifications.
              </li>
              <li>
                <strong className="text-slate-200">Journey Data:</strong> We
                store the train journey details you provide (journey name, date,
                and preferences) to generate reminders.
              </li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mb-3">
              2. How We Use Your Information
            </h2>
            <ul className="list-disc pl-5 space-y-2">
              <li>To create and manage your secure account.</li>
              <li>To send you automated reminders via the Telegram bot.</li>
              <li>
                To create Google Calendar events (if you enable that
                integration).
              </li>
              <li>
                To monitor and improve the performance of our application.
              </li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mb-3">
              3. Data Storage and Security
            </h2>
            <p>
              We use industry-standard security measures (SSL/TLS encryption) to
              protect your data. Your information is stored securely using Neon
              (PostgreSQL). We
              <span className="text-indigo-400 font-medium"> never</span> sell
              your personal data to third parties.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mb-3">
              4. Third-Party Services
            </h2>
            <p className="mb-2">
              We share data only with the following services to provide our core
              features:
            </p>
            <ul className="list-disc pl-5 space-y-1">
              <li>Google LLC (Authentication & Calendar)</li>
              <li>Telegram FZ-LLC (Notifications)</li>
              <li>Render & Neon (Infrastructure & Database)</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mb-3">
              5. Your Rights
            </h2>
            <p>
              You can delete your account and all associated data at any time
              through the Profile settings in the application.
            </p>
          </section>

          <section className="pt-8 border-t border-slate-800">
            <p className="text-sm text-slate-500 text-center">
              Questions? Contact us at:{" "}
              <span className="text-slate-400 italic">
                railreminders.help@gmail.com
              </span>
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}

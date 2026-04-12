import { Link } from "react-router-dom";
import { FaChevronLeft } from "react-icons/fa";

export function TermsOfService() {
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
          Rail Reminders: Terms of Service
        </h1>
        <p className="text-slate-500 mb-8 italic">
          Last Updated: April 12, 2026
        </p>

        <div className="space-y-8 leading-relaxed">
          <section>
            <h2 className="text-xl font-semibold text-white mb-3">
              1. Description of Service
            </h2>
            <p>
              Rail Reminders ("the Service") is a tool designed to help users
              track their train journeys and receive automated notifications. We
              are an independent service and are{" "}
              <strong className="text-red-400">NOT affiliated</strong> with
              IRCTC or Indian Railways.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mb-3">
              2. User Responsibilities
            </h2>
            <ul className="list-disc pl-5 space-y-2">
              <li>You must provide accurate journey information.</li>
              <li>
                You are responsible for maintaining the security of your account
                and linked integrations (Google/Telegram).
              </li>
            </ul>
          </section>

          <section className="bg-red-500/10 border border-red-500/20 p-6 rounded-xl">
            <h2 className="text-xl font-semibold text-white mb-3">
              3. Limitation of Liability
            </h2>
            <p className="mb-4">
              While we strive for 100% reliability, Rail Reminders is provided
              "as is." We are{" "}
              <strong className="text-white underline">not liable</strong> for
              any missed trains, financial losses, or damages resulting from:
            </p>
            <ul className="list-disc pl-5 space-y-2 text-slate-400">
              <li>Failed notifications or reminders.</li>
              <li>Incorrect journey data provided by the user.</li>
              <li>Service outages or technical delays.</li>
            </ul>
            <p className="mt-4 font-semibold text-slate-200">
              Users are advised to always cross-check their official IRCTC
              tickets.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mb-3">
              4. Account Termination
            </h2>
            <p>
              We reserve the right to suspend or terminate your account if you
              misuse the service or violate these terms.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mb-3">
              5. Governing Law
            </h2>
            <p>These terms are governed by the laws of India.</p>
          </section>

          <section className="pt-8 border-t border-slate-800">
            <p className="text-sm text-slate-500 text-center">
              Questions or concerns? Contact us at:{" "}
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

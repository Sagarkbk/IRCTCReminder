import { FaTrain, FaCalendarAlt } from "react-icons/fa";
import { type Journey } from "../store/slices/journeySlice";
interface JourneyCardProps {
  journey: Journey;
}
export function JourneyCard({ journey }: JourneyCardProps) {
  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  };

  return (
    <div className="bg-slate-800/50 border border-slate-700 hover:border-indigo-500/50 transition-all rounded-xl p-5 shadow-lg flex flex-col group">
      <div className="flex items-center gap-3 mb-4">
        <div className="bg-indigo-500/10 p-2 rounded-lg text-indigo-400">
          <FaTrain size={18} />
        </div>
        <h3 className="text-xl font-bold text-white truncate flex-1">
          {journey.journey_name}
        </h3>
      </div>

      <div className="flex items-center text-slate-400 text-sm">
        <FaCalendarAlt className="mr-2" size={14} />
        <span>{formatDate(journey.journey_date)}</span>
      </div>
    </div>
  );
}

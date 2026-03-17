import { useEffect, useState } from "react";
import { useJourney } from "../hooks/journey/useJourney";
import { JourneyCard } from "./JourneyCard";
import { FaPlus } from "react-icons/fa";
import { AddJourneyModal } from "./AddJourneyModal";

export function JourneyList() {
  const { journeys, fetchJourneys, isLoading, error } = useJourney();
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);

  useEffect(() => {
    fetchJourneys();
  }, []);

  if (isLoading && journeys.length === 0) {
    return (
      <div className="text-center py-10 text-slate-400">
        Loading journeys...
      </div>
    );
  }

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-2xl font-bold text-white mb-6">Your Journeys</h2>
        <button
          onClick={() => setIsAddModalOpen(true)}
          className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg font-semibold transition-all text-sm shadow-lg shadow-indigo-500/10"
        >
          <FaPlus size={14} /> Add New
        </button>
      </div>

      {error && (
        <div className="text-center py-4 mb-6 bg-red-500/10 text-red-400 rounded-lg border border-red-500/20">
          {error}
        </div>
      )}

      {journeys.length === 0 ? (
        <div className="bg-slate-800/30 border border-dashed border-slate-700 rounded-2xl py-16 text-center">
          <p className="text-slate-400">
            No journeys found. Start by adding one!
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {journeys.map((journey) => (
            <JourneyCard key={journey.id} journey={journey} />
          ))}
        </div>
      )}

      <AddJourneyModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
      />
    </div>
  );
}

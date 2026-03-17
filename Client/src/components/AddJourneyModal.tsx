import { useState, useEffect } from "react";
import { Modal } from "./Modal";
import { FaTrash } from "react-icons/fa";
import { useJourney } from "../hooks/journey/useJourney";

interface AddJourneyModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function AddJourneyModal({ isOpen, onClose }: AddJourneyModalProps) {
  const [name, setName] = useState("");
  const [date, setDate] = useState("");
  const [reminderOnReleaseDay, setReminderOnReleaseDay] = useState(true);
  const [reminderOnDayBefore, setReminderOnDayBefore] = useState(true);
  const [customReminders, setCustomReminders] = useState<string[]>([]);

  const today = new Date();
  const minJourney = new Date(today);
  minJourney.setDate(today.getDate() + 62);
  const minJourneyDate = minJourney.toISOString().split("T")[0];

  const tomorrow = new Date(today);
  tomorrow.setDate(today.getDate() + 1);
  const minCustomDate = tomorrow.toISOString().split("T")[0];

  let maxCustomDate = "";
  if (date) {
    const journeyDateObj = new Date(date);
    const maxDateObj = new Date(journeyDateObj);
    maxDateObj.setDate(journeyDateObj.getDate() - 62);
    maxCustomDate = maxDateObj.toISOString().split("T")[0];
  }

  const addCustomReminder = () => {
    if (customReminders.length < 3) {
      setCustomReminders([...customReminders, ""]);
    }
  };

  const updateCustomReminder = (index: number, val: string) => {
    const updated = [...customReminders];
    updated[index] = val;
    setCustomReminders(updated);
  };

  const removeCustomReminder = (index: number) => {
    setCustomReminders(customReminders.filter((_, i) => i !== index));
  };

  useEffect(() => {
    if (date && maxCustomDate < minCustomDate) {
      setCustomReminders([]);
    }
  }, [date, maxCustomDate, minCustomDate]);

  const handleClose = () => {
    setName("");
    setDate("");
    setReminderOnReleaseDay(true);
    setReminderOnDayBefore(true);
    setCustomReminders([]);
    onClose();
  };

  const { addNewJourney, isLoading } = useJourney();

  const handleSubmit = async () => {
    if (!name.trim()) {
      alert("Please enter a journey name");
      return;
    }
    if (!date) {
      alert("Please select a journey date");
      return;
    }

    await addNewJourney({
      journey_name: name,
      journey_date: date,
      reminder_on_release_day: reminderOnReleaseDay,
      reminder_on_day_before: reminderOnDayBefore,
      custom_reminders: customReminders.filter((d) => d !== ""),
    });
    console.log(customReminders);

    handleClose();
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="Add New Journey">
      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-slate-400 mb-1.5">
            Journey Name
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g. Trip to Mumbai"
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 transition-colors"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-400 mb-1.5">
            Journey Date
          </label>
          <input
            type="date"
            value={date}
            min={minJourneyDate}
            onChange={(e) => setDate(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500 transition-colors [color-scheme:dark]"
          />
        </div>

        <div className="space-y-3">
          <label className="block text-sm font-medium text-slate-400">
            Standard Reminders
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <label className="flex items-center gap-3 bg-slate-900 border border-slate-700 p-3 rounded-lg cursor-pointer hover:border-indigo-500/50 transition-colors">
              <input
                type="checkbox"
                checked={reminderOnReleaseDay}
                onChange={(e) => setReminderOnReleaseDay(e.target.checked)}
                className="w-4 h-4 accent-indigo-600 cursor-pointer"
              />
              <span className="text-sm text-slate-200">Release Day</span>
            </label>
            <label className="flex items-center gap-3 bg-slate-900 border border-slate-700 p-3 rounded-lg cursor-pointer hover:border-indigo-500/50 transition-colors">
              <input
                type="checkbox"
                checked={reminderOnDayBefore}
                onChange={(e) => setReminderOnDayBefore(e.target.checked)}
                className="w-4 h-4 accent-indigo-600 cursor-pointer"
              />
              <span className="text-sm text-slate-200">Day Before Release</span>
            </label>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <label className="text-sm font-medium text-slate-400">
              Custom Reminders ({customReminders.length}/3)
              {!date && (
                <p className="text-[12px] text-slate-500 mt-1 italic">
                  * Select a journey date to enable custom reminders
                </p>
              )}
              {date && maxCustomDate < minCustomDate && (
                <p className="text-[12px] text-slate-500 mt-1 italic">
                  * Custom Reminders are not available for the selected journey
                  date
                </p>
              )}
            </label>

            {customReminders.length < 3 && maxCustomDate >= minCustomDate && (
              <button
                type="button"
                onClick={addCustomReminder}
                disabled={!date}
                className={`text-xs font-semibold transition-colors ${
                  !date
                    ? "text-slate-600 cursor-not-allowed"
                    : "text-indigo-400 hover:text-indigo-300"
                }`}
                title={!date ? "Please select a journey date first" : ""}
              >
                + Add Date
              </button>
            )}
          </div>

          <div className="space-y-2">
            {customReminders.map((reminderDate, index) => (
              <div key={index} className="flex gap-2">
                <input
                  type="date"
                  value={reminderDate}
                  min={minCustomDate}
                  max={maxCustomDate}
                  onChange={(e) => updateCustomReminder(index, e.target.value)}
                  className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-indigo-500 [color-scheme:dark]"
                />
                <button
                  type="button"
                  onClick={() => removeCustomReminder(index)}
                  className="p-2 text-slate-500 hover:text-red-400 transition-colors"
                >
                  <FaTrash size={14} />
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className="flex justify-end gap-3 pt-4 border-t border-slate-700">
          <button
            onClick={handleClose}
            className="px-4 py-2 text-slate-400 hover:text-white transition-colors"
          >
            Cancel
          </button>
          <button
            className={`bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-lg font-semibold transition-all 
                ${isLoading ? "opacity-50 cursor-not-allowed" : ""}`}
            onClick={handleSubmit}
            disabled={isLoading}
          >
            {isLoading ? "Adding..." : "Add Journey"}
          </button>
        </div>
      </div>
    </Modal>
  );
}

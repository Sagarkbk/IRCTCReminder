import { useState } from "react";

export function useGoogleCalendarConnect() {
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const connectCalendar = async () => {
    setIsLoading(false);
  };

  return { connectCalendar, isLoading };
}

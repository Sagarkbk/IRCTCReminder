import { useState } from "react";

export function useTelegramRevoke() {
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const revokeTelegram = async () => {
    setIsLoading(false);
  };

  return { revokeTelegram, isLoading };
}

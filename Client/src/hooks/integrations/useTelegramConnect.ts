import { useState } from "react";

export function useTelegramConnect() {
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const connectTelegram = async () => {
    setIsLoading(false);
  };

  return { connectTelegram, isLoading };
}

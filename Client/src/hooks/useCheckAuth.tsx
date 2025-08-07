import { useEffect, useState } from "react";

export function useCheckAuth() {
  const [isAuthenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    if (localStorage.getItem("token")) {
      setAuthenticated(true);
    } else {
      setAuthenticated(false);
    }
  }, []);

  return { isAuthenticated };
}

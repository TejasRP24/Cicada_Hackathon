import React, { createContext, useContext, useState } from "react";

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [emotion, setEmotion] = useState("neutral");
  return (
    <ThemeContext.Provider value={{ emotion, setEmotion }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}

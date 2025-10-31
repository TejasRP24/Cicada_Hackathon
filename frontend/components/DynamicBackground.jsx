import React, { useEffect, useState } from "react";
import { useTheme } from "./ThemeContext";
import "../components-css/dynamicBackground.css";

export default function DynamicBackground() {
  const { emotion } = useTheme();
  const [prevEmotion, setPrevEmotion] = useState(emotion);
  const [fade, setFade] = useState(false);

  useEffect(() => {
    if (emotion !== prevEmotion) {
      setFade(true);
      const timeout = setTimeout(() => {
        setPrevEmotion(emotion);
        setFade(false);
      }, 1200); // match new fade duration in CSS
      return () => clearTimeout(timeout);
    }
  }, [emotion, prevEmotion]);

  return (
    <>
      {/* old theme stays underneath */}
      <div className={`dynamic-bg bg-${prevEmotion}`} />
      {/* new theme fades in */}
      {fade && <div className={`dynamic-bg bg-${emotion} fade-in`} />}
    </>
  );
}

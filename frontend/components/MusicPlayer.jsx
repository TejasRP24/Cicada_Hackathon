import React, { useEffect, useRef, useState } from "react";
import { useTheme } from "./ThemeContext";
import musicMap from "../src/assets/musicMap.json";
import { Volume2, VolumeX, SkipForward, Play, Pause } from "lucide-react";

export default function MusicPlayer({ musicSrc }) {
  const { emotion } = useTheme();
  const audioRef = useRef(null);
  const [currentSong, setCurrentSong] = useState(null);
  const [isMuted, setIsMuted] = useState(false);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);

  // 🎯 Pick a random song based on emotion
  const pickRandomSong = () => {
    const emotionTracks = musicMap[emotion];
    if (!emotionTracks) {
      console.warn("No tracks found for emotion:", emotion);
      return null;
    }
    const songKeys = Object.keys(emotionTracks);
    if (songKeys.length === 0) {
      console.warn("Emotion track list is empty");
      return null;
    }
    const randomKey = songKeys[Math.floor(Math.random() * songKeys.length)];
    const selected = emotionTracks[randomKey];
    console.log("Selected song:", selected);
    return selected;
  };

  // 🧠 Update song when emotion changes
  useEffect(() => {
    if (!emotion) return;
    const newSong = pickRandomSong();
    setCurrentSong(newSong);
    setIsPlaying(true);
  }, [emotion]);

  // 🔄 Handle song transitions
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio || !currentSong || !isPlaying) return;

    const fadeOut = async () => {
      setIsTransitioning(true);
      for (let vol = audio.volume; vol > 0; vol -= 0.05) {
        audio.volume = Math.max(vol, 0);
        await new Promise((res) => setTimeout(res, 40));
      }
      audio.pause();
    };

    const fadeIn = async () => {
      audio.src = currentSong;
      audio.load();
      audio.muted = false;
      audio.volume = 0;
      try {
        await audio.play();
        console.log("Playback started:", currentSong);
      } catch (err) {
        console.warn("Autoplay blocked:", err);
        setIsPlaying(false);
        return;
      }
      for (let vol = 0; vol <= 1; vol += 0.05) {
        audio.volume = Math.min(vol, 1);
        await new Promise((res) => setTimeout(res, 40));
      }
      setIsTransitioning(false);
    };

    const transition = async () => {
      if (!audio.paused) await fadeOut();
      await fadeIn();
    };

    transition();
  }, [currentSong, isPlaying]);

  // 🔊 Toggle mute
  const toggleMute = () => {
    const audio = audioRef.current;
    if (!audio) return;
    audio.muted = !audio.muted;
    setIsMuted(audio.muted);
    console.log("Muted:", audio.muted);
  };

  // ⏭️ Skip to another track
  const skipTrack = () => {
    const nextSong = pickRandomSong();
    setCurrentSong(nextSong);
  };
  
  // ▶️ Toggle play/pause
  const togglePlay = async () => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isPlaying) {
      audio.pause();
      setIsPlaying(false);
      console.log("Playback paused");
    } else {
      try {
        await audio.play();
        setIsPlaying(true);
        console.log("Playback resumed");
      } catch (err) {
        console.warn("Autoplay blocked:", err);
      }
    }
  };

  return (
    <div className="music-player">
      <audio ref={audioRef} loop />
      <div className="music-controls">
        <button onClick={togglePlay} className="music-btn">
          {isPlaying ? <Pause size={22} /> : <Play size={22} />}
        </button>
        <button onClick={toggleMute} className="music-btn">
          {isMuted ? <VolumeX size={22} /> : <Volume2 size={22} />}
        </button>
        <button onClick={skipTrack} className="music-btn" disabled={isTransitioning}>
          <SkipForward size={22} />
        </button>
      </div>
    </div>
  );
}

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "../components/navbar";
import InputPage from "../pages/InputPage";
//import AboutPage from "./pages";
//import Dashboard from "./pages/Dashboard";
import { ThemeProvider } from "../components/ThemeContext";
//import MusicPlayer from "../components/MusicPlayer";
import "./index.css"; // global styles if any
import Advice from "../components/advice"
import History from "../components/History";
import DynamicBackground from "../components/DynamicBackground";
import MusicPlayer from "../components/MusicPlayer";
import InputWithChat from "../components/InputWithChat";
function App() {
  return (
    <ThemeProvider>
      <DynamicBackground />
      <Router>
        <div className="app-container">
          <Navbar />
          <Routes>
            <Route path="/" element={<InputPage />} />
            <Route path="/advice" element={<Advice/>}/>
            <Route path="/his" element={<History/>}/>
            <Route path="/chat" element={<InputWithChat />} />
          </Routes>
          <MusicPlayer/>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;

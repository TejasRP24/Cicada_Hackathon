import React from "react";
import { Link } from "react-router-dom";
import "../components-css/navbar.css";

export default function Navbar() {
  return (
    <nav className="navbar">
      <h1 className="navbar-title">MyMind</h1>
      <div className="navbar-links">
        <Link to="/" className="nav-link">Home</Link>
        <Link to="/dashboard" className="nav-link">Dashboard</Link>
        <Link to="/his" className="nav-link">History</Link>
      </div>
    </nav>
  );
}

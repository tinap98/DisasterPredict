import React from "react";
import { Link } from "react-router-dom";

const LandingPage = ({ isAuthenticated }) => {
  return (
    <div className="bg-custom min-h-screen flex flex-col text-white">
      {/* Hero Section */}
      <div className="flex flex-col items-center justify-center text-center px-6 flex-grow mt-20 pb-10 relative z-10">
        <h1 className="text-4xl font-bold text-amber-500">
          Welcome to DisasterPredict
        </h1>
        <p className="mt-4 text-lg max-w-2xl text-gray-200">
          Stay informed with real-time disaster tracking and news updates powered by NASA and other reliable sources.
        </p>
      </div>

      {/* Donate Section */}
      <div className="flex flex-col items-center pb-10">
        <h2 className="text-2xl font-semibold text-center mb-4">
          Support Relief Efforts
        </h2>
        <Link
          to={isAuthenticated ? "/donate" : "/login"}
          className="donate-button"
        >
          Donate Now
        </Link>
      </div>
    </div>
  );
};

export default LandingPage;

import React, { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";

const LandingPage = ({ isAuthenticated, handleLogout }) => {
  const [isVisible, setIsVisible] = useState(false);
  const contactRef = useRef(null); // Reference for Contact Us section

  // Function to observe when Contact Us is in view
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => setIsVisible(entry.isIntersecting),
      { threshold: 0.3 }
    );

    if (contactRef.current) observer.observe(contactRef.current);

    return () => {
      if (contactRef.current) observer.unobserve(contactRef.current);
    };
  }, []);

  // Function to scroll smoothly to Contact Us
  const handleScrollToContact = (e) => {
    e.preventDefault();
    contactRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Navbar */}
      <nav className="bg-teal-600 text-white py-4 px-6 flex justify-between items-center shadow-md">
        <h2 className="text-lg font-semibold">DisasterPredict</h2>
        <div className="space-x-6 flex items-center">
          {["Home", "Disaster News", "Disaster Map", "Contact Us", "Donate"].map((item, index) => (
            <Link
              key={index}
              to={
                item === "Home"
                  ? "/home"
                  : item === "Disaster News"
                  ? "/disaster-news"
                  : item === "Disaster Map"
                  ? "/disaster-map"
                  : item === "Donate"
                  ? "/donate"
                  : "#"
              }
              onClick={item === "Contact Us" ? handleScrollToContact : undefined} // Smooth scroll when Contact Us is clicked
              className="relative group transition duration-300"
            >
              {item}
              <span className="absolute left-0 bottom-0 w-0 h-[2px] bg-white transition-all duration-300 group-hover:w-full"></span>
            </Link>
          ))}
        </div>

        {/* Show Logout button if user is logged in, else show Signup & Login */}
        {isAuthenticated ? (
          <button
            onClick={handleLogout}
            className="bg-white text-gray-900 font-semibold py-2 px-4 rounded-md border border-gray-300 
             hover:bg-gray-100 hover:border-gray-400 transition-all"
          >
            Logout
          </button>
        ) : (
          <div className="space-x-4">
            <Link
              to="/login"
              className="bg-white text-teal-600 border border-teal-600 px-4 py-2 rounded-md font-semibold 
              shadow-sm hover:bg-teal-600 hover:text-white transition duration-300"
            >
              Login
            </Link>
            <Link
              to="/signup"
              className="bg-white text-teal-600 border border-teal-600 px-4 py-2 rounded-md font-semibold 
              shadow-sm hover:bg-teal-600 hover:text-white transition duration-300"
            >
              Signup
            </Link>
          </div>
        )}
      </nav>

      {/* Hero Section (Improved Spacing) */}
      <div className="flex flex-col items-center justify-center text-center px-6 flex-grow mt-20 pb-10">
        <h1 className="text-4xl font-bold text-gray-800">Welcome to DisasterPredict</h1>
        <p className="mt-4 text-lg text-gray-600 max-w-2xl">
          Stay informed with real-time disaster tracking and news updates powered by NASA and other reliable sources.
        </p>
      </div>

      {/* Contact Us Section */}
      <div ref={contactRef} className="bg-gray-100 py-16 px-8 mt-20">
        <h2
          className={`text-3xl font-bold text-teal-700 text-center mb-6 transition-transform duration-700 ${
            isVisible ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
          }`}
        >
          Contact Us
        </h2>
        <div
          className={`text-center text-gray-700 transition-opacity duration-700 ${
            isVisible ? "opacity-100" : "opacity-0"
          }`}
        >
          <p className="text-lg font-semibold">Stay Connected, Stay Safe!</p>
          <p className="mt-2">If you have any questions, feedback, or need assistance, feel free to reach out to us.</p>
          <p>We’re here to help you stay informed and prepared for any disasters.</p>
          <div className="mt-6 space-y-2">
            <p>📍 <strong>Address:</strong> DisasterPredict HQ, 123 Safety Street, Tech City, 56789</p>
            <p>📞 <strong>Phone:</strong> +1 (234) 567-8900</p>
            <p>📧 <strong>Email:</strong> support@disasterpredict.com</p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-100 py-4 text-center text-gray-600 text-sm">
        &copy; {new Date().getFullYear()} DisasterPredict. All rights reserved.
      </footer>
    </div>
  );
};

export default LandingPage;

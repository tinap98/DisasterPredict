import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Signup = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:5000/register", formData);
      alert("Registration successful! Please login.");
      navigate("/login");
    } catch (error) {
      alert(error.response?.data?.error || "Registration failed");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-black">
      <form
        onSubmit={handleSignup}
        className="bg-black/60 shadow-lg rounded-lg p-8 w-96 border border-amber-500"
      >
        <h2 className="text-2xl font-bold text-center text-amber-400 mb-6">
          Create an Account
        </h2>
        <input
          type="text"
          placeholder="Choose a username"
          value={formData.username}
          onChange={(e) =>
            setFormData({ ...formData, username: e.target.value })
          }
          required
          className="w-full p-3 bg-gray-900 border border-amber-500 rounded-md mb-4 focus:ring-2 focus:ring-amber-400 focus:outline-none placeholder-black placeholder-opacity-70 text-white"
        />
        <input
          type="email"
          placeholder="Enter your email"
          value={formData.email}
          onChange={(e) =>
            setFormData({ ...formData, email: e.target.value })
          }
          required
          className="w-full p-3 bg-gray-900 border border-amber-500 rounded-md mb-4 focus:ring-2 focus:ring-amber-400 focus:outline-none placeholder-black placeholder-opacity-70 text-white"
        />
        <input
          type="password"
          placeholder="Create a password"
          value={formData.password}
          onChange={(e) =>
            setFormData({ ...formData, password: e.target.value })
          }
          required
          className="w-full p-3 bg-gray-900 border border-amber-500 rounded-md mb-6 focus:ring-2 focus:ring-amber-400 focus:outline-none placeholder-black placeholder-opacity-70 text-white"
        />
        <button
          type="submit"
          className="w-full bg-amber-500 text-black font-semibold py-2 px-4 rounded-md hover:bg-amber-600 transition-all duration-300"
        >
          Register
        </button>
        <p className="mt-4 text-center text-gray-300">
          Already have an account?{" "}
          <a href="/login" className="text-amber-400 hover:underline">
            Log in
          </a>
        </p>
      </form>
    </div>
  );
};

export default Signup;

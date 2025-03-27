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
    <div className="flex items-center justify-center min-h-screen bg-white">
      <form
        onSubmit={handleSignup}
        className="bg-gray-100 shadow-lg rounded-lg p-8 w-96 transition-all duration-300 hover:shadow-2xl border border-teal-300"
      >
        <h2 className="text-2xl font-bold text-center text-teal-700 mb-6">
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
          className="w-full p-3 border border-gray-300 rounded-md mb-4 focus:ring-2 focus:ring-teal-400 focus:outline-none placeholder-gray-500 text-gray-700"
        />
        <input
          type="email"
          placeholder="Enter your email"
          value={formData.email}
          onChange={(e) =>
            setFormData({ ...formData, email: e.target.value })
          }
          required
          className="w-full p-3 border border-gray-300 rounded-md mb-4 focus:ring-2 focus:ring-teal-400 focus:outline-none placeholder-gray-500 text-gray-700"
        />
        <input
          type="password"
          placeholder="Create a password"
          value={formData.password}
          onChange={(e) =>
            setFormData({ ...formData, password: e.target.value })
          }
          required
          className="w-full p-3 border border-gray-300 rounded-md mb-6 focus:ring-2 focus:ring-teal-400 focus:outline-none placeholder-gray-500 text-gray-700"
        />
        <button
          type="submit"
          className="w-full bg-teal-600 text-white py-2 px-4 rounded-md hover:bg-teal-700 hover:shadow-lg transition-all duration-300"
        >
          Register
        </button>
        <p className="mt-4 text-center text-gray-600">
          Already have an account?{" "}
          <a href="/login" className="text-teal-700 hover:underline">
            Log in
          </a>
        </p>
      </form>
    </div>
  );
};

export default Signup;

import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";
import toast, { Toaster } from "react-hot-toast";

const Signup = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await axios.post("http://localhost:5000/register", formData);
      toast.success("Registration successful! Please login.");
      navigate("/login");
    } catch (error) {
      toast.error(error.response?.data?.error || "Registration failed");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-black">
      <Toaster position="top-center" />
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
          disabled={isLoading}
          className="w-full bg-amber-500 text-black font-semibold py-2 px-4 rounded-md hover:bg-amber-600 transition-all duration-300 disabled:opacity-50"
        >
          {isLoading ? "Registering..." : "Register"}
        </button>
        <p className="mt-4 text-center text-gray-300">
          Already have an account?{" "}
          <Link to="/login" className="text-amber-400 hover:underline">
            Log in
          </Link>
        </p>
      </form>
    </div>
  );
};

export default Signup;

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Login = () => {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:5000/login", formData);
      alert("Login successful!");
      navigate("/dashboard");
    } catch (error) {
      alert(error.response?.data?.error || "Login failed");
    }
  };

  return (
    <div
      className="relative flex items-center justify-center min-h-screen bg-cover bg-center"
      style={{ backgroundImage: "url('/images/world_map.jpg')" }}
    >
      {/* Dark Overlay */}
      <div className="absolute inset-0 bg-black/70"></div>

      {/* Login Box */}
      <div className="relative z-10 w-full max-w-md p-8 bg-black border border-gray-700 shadow-lg rounded-xl">
        <h2 className="text-3xl font-semibold text-center text-amber-500 mb-6">
          Login
        </h2>

        <form className="space-y-5" onSubmit={handleLogin}>
          <input
            type="text"
            placeholder="Username"
            value={formData.username}
            onChange={(e) =>
              setFormData({ ...formData, username: e.target.value })
            }
            required
            className="w-full p-3 bg-black border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:ring-2 focus:ring-amber-500 focus:outline-none"
          />

          <input
            type="password"
            placeholder="Password"
            value={formData.password}
            onChange={(e) =>
              setFormData({ ...formData, password: e.target.value })
            }
            required
            className="w-full p-3 bg-black border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:ring-2 focus:ring-amber-500 focus:outline-none"
          />

          <button
            type="submit"
            className="w-full p-3 text-black bg-amber-500 font-semibold rounded-lg hover:bg-amber-600 focus:ring-2 focus:ring-amber-500 transition-all"
          >
            Log In
          </button>
        </form>

        <p className="mt-4 text-center text-gray-400">
          New user?{" "}
          <a href="/signup" className="text-amber-500 hover:underline">
            Create an account
          </a>
        </p>
      </div>
    </div>
  );
};

export default Login;

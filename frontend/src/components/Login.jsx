import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Login = ({ setIsAuthenticated }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/login", {
        username,
        password,
      });

      localStorage.setItem("authToken", response.data.token);
      setIsAuthenticated(true);
      navigate("/home");
    } catch (error) {
      alert(error.response?.data?.error || "Login failed");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-white">
      <form
        onSubmit={handleLogin}
        className="bg-gray-100 shadow-lg rounded-lg p-8 w-96 transition-all duration-300 hover:shadow-2xl border border-teal-300"
      >
        <h2 className="text-2xl font-bold text-center text-teal-700 mb-6">
          Login
        </h2>
        <input
          type="text"
          placeholder="Enter your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          className="w-full p-3 border border-gray-300 rounded-md mb-4 focus:ring-2 focus:ring-teal-400 focus:outline-none placeholder-gray-500 text-gray-700"
        />
        <input
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full p-3 border border-gray-300 rounded-md mb-6 focus:ring-2 focus:ring-teal-400 focus:outline-none placeholder-gray-500 text-gray-700"
        />
        <button
          type="submit"
          className="w-full bg-teal-600 text-white p-3 rounded-md hover:bg-teal-700 transition-all duration-300 shadow-md"
        >
          Log In
        </button>
        <p className="mt-4 text-center text-gray-600">
          New user?{" "}
          <a href="/signup" className="text-teal-700 hover:underline">
            Create an account
          </a>
        </p>
      </form>
    </div>
  );
};

export default Login;

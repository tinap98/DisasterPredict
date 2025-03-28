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
    <div className="flex items-center justify-center min-h-screen bg-black">
      <form
        onSubmit={handleLogin}
        className="bg-black/60 shadow-lg rounded-lg p-8 w-96 border border-amber-500"
      >
        <h2 className="text-2xl font-bold text-center text-amber-400 mb-6">
          Login
        </h2>
        <input
          type="text"
          placeholder="Enter your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          className="w-full p-3 bg-gray-900 border border-amber-500 rounded-md mb-4 focus:ring-2 focus:ring-amber-400 focus:outline-none placeholder-black placeholder-opacity-70 text-white"
        />
        <input
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full p-3 bg-gray-900 border border-amber-500 rounded-md mb-6 focus:ring-2 focus:ring-amber-400 focus:outline-none placeholder-black placeholder-opacity-70 text-white"
        />
        <button
          type="submit"
          className="w-full bg-amber-500 text-black font-semibold p-3 rounded-md hover:bg-amber-600 transition-all duration-300"
        >
          Log In
        </button>
        <p className="mt-4 text-center text-gray-300">
          New user?{" "}
          <a href="/signup" className="text-amber-400 hover:underline">
            Create an account
          </a>
        </p>
      </form>
    </div>
  );
};

export default Login;

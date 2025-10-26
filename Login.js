import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Shield, Lock, User, Eye, EyeOff } from 'lucide-react';

const Login = () => {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const result = await login(formData.username, formData.password);
      if (result.success) navigate('/chat');
    } catch (error) {
      console.error('Login error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-blue-50 via-white to-pink-50">
      <div className="relative w-full max-w-md p-10 space-y-10">
        {/* Header */}
        <div className="text-center">
          <div className="flex justify-center mb-6">
            <div className="p-5 bg-gradient-to-r from-pink-400 to-blue-400 rounded-full shadow-lg">
              <Shield className="h-12 w-12 text-white" />
            </div>
          </div>
          <h2 className="text-3xl font-bold text-gray-800 mb-1">Encryption </h2>
          <p className="text-gray-500 text-sm"> Secure Messaging using AI</p>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-2xl shadow-md p-8 border border-gray-200">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {/* Username */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Username
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <User className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  name="username"
                  type="text"
                  required
                  placeholder="Enter your username"
                  className="w-full pl-10 pr-3 py-2 rounded-lg border border-gray-300 text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-transparent transition duration-200"
                  value={formData.username}
                  onChange={handleChange}
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  placeholder="Enter your password"
                  className="w-full pl-10 pr-10 py-2 rounded-lg border border-gray-300 text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-transparent transition duration-200"
                  value={formData.password}
                  onChange={handleChange}
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-700 transition" />
                  ) : (
                    <Eye className="h-5 w-5 text-gray-400 hover:text-gray-700 transition" />
                  )}
                </button>
              </div>
            </div>

            {/* Remember & Forgot */}
            <div className="flex items-center justify-between text-sm text-gray-600">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  className="h-4 w-4 border-gray-300 rounded"
                />
                <span>Remember me</span>
              </label>
              <Link to="#" className="font-medium text-pink-400 hover:text-pink-500">
                Forgot password?
              </Link>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-lg bg-gradient-to-r from-pink-400 to-blue-400 text-white font-semibold shadow hover:shadow-lg transition duration-200 flex justify-center items-center"
            >
              {loading ? (
                <div className="loading-spinner mr-2 border-t-white border-b-blue-400 h-4 w-4 rounded-full animate-spin"></div>
              ) : (
                'Sign In'
              )}
            </button>

            {/* Register */}
            <p className="text-center text-gray-500 text-sm mt-4">
              Don’t have an account?{' '}
              <Link
                to="/register"
                className="font-medium text-pink-400 hover:text-blue-400 transition"
              >
                Sign up
              </Link>
            </p>
          </form>
        </div>

        {/* Features Footer */}
        <div className="text-center text-gray-600 text-xs flex justify-center space-x-6">
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
            <span>End-to-End Encryption</span>
          </div>
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
            <span>AI Threat Detection</span>
          </div>
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
            <span>Self-Destruct Messages</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;

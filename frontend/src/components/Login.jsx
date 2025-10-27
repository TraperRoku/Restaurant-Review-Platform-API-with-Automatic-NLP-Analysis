import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; 
import { Award } from 'lucide-react';
import authService from '../services/auth.service';

const Login = () => {
  const [loginForm, setLoginForm] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate(); 

  const handleLogin = (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage('');

    authService.login(loginForm.username, loginForm.password).then(
      (userData) => {
        navigate('/');
        window.location.reload(); 
      },
      (error) => {
        const resMessage =
          (error.response && error.response.data && error.response.data.message) ||
          (error.response && error.response.data && error.response.data.error) || 
          error.message ||
          error.toString();
        setLoading(false);
        setErrorMessage(resMessage || "Wystąpił nieznany błąd logowania."); 
      }
    );
  };

  return (

    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4 -mt-20 md:-mt-24"> 
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
  
        <div className="text-center mb-8">
          <div className="bg-indigo-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <Award className="text-white" size={32} />
          </div>
          <h1 className="text-3xl font-bold text-gray-800">Restaurant Review</h1>
          <p className="text-gray-600 mt-2">Analiza NLP Recenzji Restauracji</p>
        </div>
    
        <form onSubmit={handleLogin} className="space-y-4">

          <div>
            <label className="block text-gray-700 font-semibold mb-2" htmlFor="username">
              Nazwa użytkownika
            </label>
            <input
              id="username" 
              type="text"
              value={loginForm.username}
              onChange={(e) => setLoginForm({ ...loginForm, username: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="Wprowadź nazwę użytkownika"
              required 
            />
          </div>
          <div>
            <label className="block text-gray-700 font-semibold mb-2" htmlFor="password">
              Hasło
            </label>
            <input
              id="password" 
              type="password"
              value={loginForm.password}
              onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="Wprowadź hasło"
              required 
            />
          </div>

          {errorMessage && (
            <div className="text-red-600 bg-red-100 p-3 rounded-lg text-sm font-medium">
              {errorMessage}
            </div>
          )}
  
          <button
            type="submit" 
            disabled={loading} 
            className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-colors disabled:opacity-50"
          >
            {loading ? 'Logowanie...' : 'Zaloguj się'}
          </button>
        </form> 

        <p className="text-center text-gray-600 mt-6 text-sm">
            Nie masz konta?{' '}
            <Link to="/register" className="text-indigo-600 hover:underline font-semibold">
                Zarejestruj się
            </Link>
        </p>

        <p className="text-center text-gray-600 mt-6 text-sm">
          Praca inżynierska - Filip Kaźmierczak
        </p>
      </div>
    </div>
  );
};

export default Login;
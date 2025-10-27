import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; 
import { UserPlus } from 'lucide-react'; 
import AuthService from '../services/auth.service';

const Register = () => {
  const [registerForm, setRegisterForm] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState(''); 
  const navigate = useNavigate();

  const handleRegister = (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage('');
    setSuccessMessage('');

    AuthService.register(registerForm.username, registerForm.password).then(
      (response) => {
        
        setSuccessMessage(response.data.message + " Możesz się teraz zalogować."); 
        setLoading(false);
        setRegisterForm({ username: '', password: '' }); 
    
      },
      (error) => {
   
        const resMessage =
          (error.response?.data?.message) ||
          error.message ||
          error.toString();
        setLoading(false);
        setErrorMessage(resMessage);
      }
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4 -mt-20"> {/* Dopasowanie marginesu */}
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <div className="bg-indigo-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <UserPlus className="text-white" size={32} /> 
          </div>
          <h1 className="text-3xl font-bold text-gray-800">Rejestracja</h1> 
          <p className="text-gray-600 mt-2">Utwórz nowe konto</p>
        </div>
        
        <form onSubmit={handleRegister} className="space-y-4">
          <div>
            <label className="block text-gray-700 font-semibold mb-2">Nazwa użytkownika</label>
            <input
              type="text"
              value={registerForm.username}
              onChange={(e) => setRegisterForm({ ...registerForm, username: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="Wprowadź nazwę użytkownika"
              required
              minLength={3} 
            />
          </div>
          <div>
            <label className="block text-gray-700 font-semibold mb-2">Hasło</label>
            <input
              type="password"
              value={registerForm.password}
              onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="Wprowadź hasło (min. 6 znaków)"
              required
              minLength={6} 
            />
          </div>
      
          {errorMessage && (
            <div className="text-red-600 bg-red-100 p-3 rounded-lg text-sm font-medium">
              {errorMessage}
            </div>
          )}
          {successMessage && (
             <div className="text-green-600 bg-green-100 p-3 rounded-lg text-sm font-medium">
              {successMessage}
            </div>
          )}
          
          <button
            type="submit"
            disabled={loading || successMessage} 
            className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-colors disabled:opacity-50"
          >
            {loading ? 'Rejestrowanie...' : 'Zarejestruj się'}
          </button>
        </form>

        <p className="text-center text-gray-600 mt-6 text-sm">
          Masz już konto?{' '}
          <Link to="/login" className="text-indigo-600 hover:underline font-semibold">
            Zaloguj się
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Register;

import React, { useState, useEffect } from 'react';

import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { Award, User, LogOut, BarChart3 } from 'lucide-react'; 
import authService from './services/auth.service';

function App() {
  const [currentUser, setCurrentUser] = useState(undefined);
  const navigate = useNavigate();
  const location = useLocation(); 

  useEffect(() => {
    const user = authService.getCurrentUser();
    if (user) {
      setCurrentUser(user);
    }
  }, []); 

  const handleLogout = () => {
    authService.logout();
    setCurrentUser(undefined);
    navigate('/login');

    window.location.reload(); 
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">

      <nav className="bg-white shadow-md sticky top-0 z-10"> 
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            
            <Link to="/" className="flex items-center gap-3 group"> 
              <div className="bg-indigo-600 p-2 rounded-lg group-hover:bg-indigo-700 transition-colors"> 
                <Award className="text-white" size={24} />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-800 group-hover:text-indigo-700 transition-colors">Restaurant Review Platform</h1>
                <p className="text-xs text-gray-600">Analiza NLP Recenzji</p>
              </div>
            </Link>

            <div className="flex items-center gap-4">
              {currentUser ? (
       
                <>
                  <Link
                    to="/"
                    className={`px-4 py-2 rounded-lg font-semibold transition-colors flex items-center gap-1 ${
                      location.pathname === '/' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                     <Award size={18}/> Dashboard
                  </Link>

                  <Link
                    to="/rankings"
                    className={`px-4 py-2 rounded-lg font-semibold transition-colors flex items-center gap-1 ${
                      location.pathname === '/rankings' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                     <BarChart3 size={18}/> Rankingi
                  </Link>
        
                  <div className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-lg border border-gray-200">
                    <User size={18} className="text-gray-600" />
                    <span className="font-semibold text-gray-700">{currentUser.username}</span>
                  </div>
                  
          
                  <button
                    onClick={handleLogout}
                    title="Wyloguj się" 
                    className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
                  >
                    <LogOut size={20} />
                  </button>
                </>
              ) : (
              
                <Link
                  to="/login"
                  className={`px-4 py-2 rounded-lg font-semibold transition-colors bg-indigo-600 text-white hover:bg-indigo-700`}
                >
                  Zaloguj się
                </Link>
              )}
            </div>
          </div>
        </div>
      </nav>


      <main className="flex-grow"> 
      
        <div className="max-w-7xl mx-auto px-4 py-8">
      
          <Outlet /> 
        </div>
      </main>


      <footer className="bg-white border-t border-gray-200 mt-auto"> 
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-gray-600 text-sm">
          <p className="font-semibold">Praca Inżynierska - Filip Kaźmierczak</p>
          <p className="mt-1">
            Opracowanie aplikacji internetowej do automatycznej oceny restauracji
          </p>
          <p className="mt-1">
            na podstawie analizy sentymentu recenzji tekstowych
          </p>
          <p className="mt-2 text-xs">Model: allegro/herbert-base-cased | F1-Score: 0.7655 | Accuracy: 0.7762</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
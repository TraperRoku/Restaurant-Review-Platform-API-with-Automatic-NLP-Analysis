import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import App from './App.jsx'; 
import Dashboard from './components/Dashboard.jsx'; 
import RestaurantDetails from './components/RestaurantDetails.jsx'; 
import Login from './components/Login.jsx'; 
import Register from './components/Register.jsx';
import Rankings from './components/Rankings.jsx';

import './index.css'; 

const router = createBrowserRouter([
  {
    path: '/', 
    element: <App />,
    children: [
      {
        path: '/', 
        element: <Dashboard />, 
      },
      {
        path: '/login', 
        element: <Login />, 
      },
      {
        path: '/register', 
        element: <Register />,
      },
      {
        path: '/rankings', 
        element: <Rankings />,
      },
      {
        path: '/restaurants/:id', 
        element: <RestaurantDetails />, 
      },
  
    ],
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>

    <RouterProvider router={router} />
  </React.StrictMode>
);
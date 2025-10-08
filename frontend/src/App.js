import React, { useState } from 'react';
import Login from './components/Login/Login';
import Register from './components/Register/Register';
import Inicio from './components/Inicio/Inicio';

export default function App() {
  const [user, setUser] = useState(null);
  const [view, setView] = useState('login'); 

  const handleLoginSuccess = (userData) => {
    
    localStorage.setItem('token', userData.token);
    setUser(userData);
    setView('inicio');
  };

  const handleRegisterSuccess = () => {
    alert('Registro exitoso. Por favor inicia sesión.');
    setView('login');
  };

  return (
    <>
      {view === 'login' && (
        <Login
          onLoginSuccess={handleLoginSuccess}
          onSwitchToRegister={() => setView('register')}
        />
      )}
      {view === 'register' && (
        <Register
          onRegisterSuccess={handleRegisterSuccess}
          onSwitchToLogin={() => setView('login')}
        />
      )}
      {view === 'inicio' && <Inicio user={user} />}
    </>
  );
}





// import React from 'react';
// import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
// import { AuthProvider, useAuth } from './contexts/AuthContext';
// import AuthContainer from './components/AuthContainer/AuthContainer';
// import Dashboard from './pages/Dashboard/Dashboard';
// import ProtectedRoute from './components/ProtectedRoute/ProtectedRoute';
// import './App.css';

// function AppContent() {
//   const { user, loading } = useAuth();

//   if (loading) {
//     return <div className="loading">Cargando...</div>;
//   }

//   return (
//     <Routes>
//       <Route 
//         path="/login" 
//         element={user ? <Navigate to="/dashboard" /> : <AuthContainer />} 
//       />
//       <Route 
//         path="/dashboard" 
//         element={
//           <ProtectedRoute>
//             <Dashboard />
//           </ProtectedRoute>
//         } 
//       />
//       <Route path="/" element={<Navigate to={user ? "/dashboard" : "/login"} />} />
//     </Routes>
//   );
// }

// function App() {
//   return (
//     <AuthProvider>
//       <Router>
//         <div className="App">
//           <AppContent />
//         </div>
//       </Router>
//     </AuthProvider>
//   );
// }

// export default App;
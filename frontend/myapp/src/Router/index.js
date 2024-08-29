import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SplashScreen from '../views/SplashScreen';
import Register from '../views/Register';
import List from '../views/List';
import PaymentSuccess from '../views/PaymentSuccess';

const AppRouter = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SplashScreen />} />
        <Route path="/register" element={<Register />} />
        <Route path="/list" element={<List />} />
        <Route path="/PaymentSuccess" element={<PaymentSuccess />} />
      </Routes>
    </Router>
  );
};

export default AppRouter;

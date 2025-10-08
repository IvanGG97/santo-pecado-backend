import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Navigate } from 'react-router-dom';
import styles from './ProtectedRoute.module.css';

const ProtectedRoute = ({ children }) => {
    const { user, loading } = useAuth();

    if (loading) {
        return <div className={styles.loading}>Cargando...</div>;
    }

    return user ? children : <Navigate to="/login" />;
};

export default ProtectedRoute;
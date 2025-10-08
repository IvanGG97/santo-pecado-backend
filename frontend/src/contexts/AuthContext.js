import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
    return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [empleado, setEmpleado] = useState(null);
    const [roles, setRoles] = useState([]);
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (token) {
            authAPI.getProfile(token)
                .then(data => {
                    setUser(data.user);
                    setEmpleado(data.empleado);
                    setRoles(data.roles || []);
                    setLoading(false);
                })
                .catch(error => {
                    console.error('Error al obtener perfil:', error);
                    logout();
                    setLoading(false);
                });
        } else {
            setLoading(false);
        }
    }, [token]);

    const login = async (username, password) => {
        try {
            const data = await authAPI.login(username, password);
            if (data.access) {
                localStorage.setItem('token', data.access);
                localStorage.setItem('refreshToken', data.refresh);
                setToken(data.access);
                setUser(data.user);
                setEmpleado(data.empleado);
                setRoles(data.roles || []);
                return { success: true };
            } else {
                return { success: false, error: data.error || 'Error en el login' };
            }
        } catch (error) {
            return { success: false, error: 'Error de conexión' };
        }
    };

    const register = async (userData) => {
        try {
            const data = await authAPI.register(userData);
            if (data.access) {
                localStorage.setItem('token', data.access);
                localStorage.setItem('refreshToken', data.refresh);
                setToken(data.access);
                setUser(data.user);
                setEmpleado(data.empleado);
                setRoles(data.roles || []);
                return { success: true };
            } else {
                return { success: false, error: data.error || 'Error en el registro' };
            }
        } catch (error) {
            return { success: false, error: 'Error de conexión' };
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        setToken(null);
        setUser(null);
        setEmpleado(null);
        setRoles([]);
    };

    const value = {
        user,
        empleado,
        roles,
        token,
        login,
        register,
        logout,
        loading
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};
import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import styles from './Dashboard.module.css';

const Dashboard = () => {
    const { user, empleado, roles, logout } = useAuth();

    return (
        <div className={styles.dashboard}>
            <header className={styles.header}>
                <h1>SM/TO PECADO - Dashboard</h1>
                <button onClick={logout} className={styles.logoutButton}>
                    Cerrar Sesión
                </button>
            </header>

            <main className={styles.main}>
                <div className={styles.userInfo}>
                    <h2>Información del Usuario</h2>
                    <p><strong>Usuario:</strong> {user?.username}</p>
                    <p><strong>Email:</strong> {user?.email}</p>
                    <p><strong>Nombre:</strong> {user?.first_name} {user?.last_name}</p>
                </div>

                {empleado && (
                    <div className={styles.empleadoInfo}>
                        <h2>Información del Empleado</h2>
                        <p><strong>DNI:</strong> {empleado.empleado_dni}</p>
                        <p><strong>Nombre:</strong> {empleado.empleado_nombre} {empleado.empleado_apellido}</p>
                        <p><strong>Teléfono:</strong> {empleado.empleado_telefono}</p>
                    </div>
                )}

                <div className={styles.rolesInfo}>
                    <h2>Roles</h2>
                    <ul>
                        {roles.map((rol, index) => (
                            <li key={index}>{rol}</li>
                        ))}
                    </ul>
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
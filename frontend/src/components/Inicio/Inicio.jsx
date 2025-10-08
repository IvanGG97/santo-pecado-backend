import React from 'react';
import styles from './Inicio.module.css';

export default function Inicio({ user }) {
    return (
        <div className={styles.container}>
            <h1 className={styles.welcome}>Bienvenido, {user.first_name || user.username}!</h1>
            <p className={styles.info}>Este es tu panel de inicio.</p>
        </div>
    );
}

import React, { useState } from 'react';
import styles from './Login.module.css';

export default function Login({ onLoginSuccess, onSwitchToRegister }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const isValid = username.trim() !== '' && password.trim() !== '';

    const handleLogin = async () => {
        if (!isValid) {
            setErrorMessage('Por favor, completa todos los campos.');
            return;
        }
        setErrorMessage('');
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/empleado/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });
            const data = await response.json();
            if (response.ok) {
                onLoginSuccess(data);
            } else {
                setErrorMessage(data.error || 'Error al iniciar sesión.');
            }
        } catch (error) {
            setErrorMessage('Error de conexión. Intenta más tarde.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.container}>
            <div class={styles.containerImg}>
                <img className={styles.img} src="https://i.imgur.com/4Khcmeg.jpeg" alt="logo de santo pecado" />
            </div>
            {/* <h2 className={`${styles.title} ${styles.neonText}`}>INICIA SESIÓN</h2> */}

            <label className={styles.label}>Usuario</label>
            <input
                className={styles.input}
                type="text"
                placeholder="Ingrese su usuario"
                value={username}
                onChange={e => setUsername(e.target.value)}
            />

            <label className={styles.label}>Contraseña</label>
            <div className={styles.passwordContainer}>
                <input
                    className={styles.input}
                    type={showPassword ? 'text' : 'password'}
                    placeholder="Ingrese su contraseña"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                />
                <button
                    type="button"
                    className={styles.showPasswordBtn}
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label="Mostrar u ocultar contraseña"
                >
                    {showPassword ? '🙈' : '👁️'}
                </button>
            </div>

            {errorMessage && <p className={styles.error}>{errorMessage}</p>}

            <button
                className={`${styles.button} ${!isValid ? styles.buttonDisabled : ''}`}
                onClick={handleLogin}
                disabled={!isValid || loading}
            >
                {loading ? 'Cargando...' : 'Iniciar Sesión'}
            </button>

            <p className={styles.switchText}>
                ¿No tienes cuenta?{' '}
                <button className={styles.linkButton} onClick={onSwitchToRegister}>
                    Regístrate
                </button>
            </p>
        </div>
    );
}






// {import React, { useState } from 'react';
// import { useAuth } from '../../contexts/AuthContext';
// import styles from './Login.module.css';

// const Login = ({ onToggleMode }) => {
//     const [username, setUsername] = useState('');
//     const [password, setPassword] = useState('');
//     const [error, setError] = useState('');
//     const [loading, setLoading] = useState(false);
//     const { login } = useAuth();

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         setLoading(true);
//         setError('');

//         const result = await login(username, password);
//         setLoading(false);

//         if (!result.success) {
//             setError(result.error || 'Error al iniciar sesión');
//         }
//     };

//     return (
//         <div className={styles.loginContainer}>
//             <div className={styles.loginCard}>
//                 <div className={styles.loginHeader}>
//                     <h2 className={styles.loginTitle}>SANTO PECADO</h2>
//                     <p className={styles.loginSubtitle}>correo</p>
//                 </div>

//                 <form onSubmit={handleSubmit} className={styles.loginForm}>
//                     <div className={styles.formGroup}>
//                         <label htmlFor="username" className={styles.label}>
//                             Usuario
//                         </label>
//                         <input
//                             id="username"
//                             type="text"
//                             value={username}
//                             onChange={(e) => setUsername(e.target.value)}
//                             className={styles.input}
//                             placeholder="Ingresa tu usuario"
//                             required
//                             disabled={loading}
//                         />
//                     </div>

//                     <div className={styles.formGroup}>
//                         <label htmlFor="password" className={styles.label}>
//                             Contraseña
//                         </label>
//                         <input
//                             id="password"
//                             type="password"
//                             value={password}
//                             onChange={(e) => setPassword(e.target.value)}
//                             className={styles.input}
//                             placeholder="Ingresa tu contraseña"
//                             required
//                             disabled={loading}
//                         />
//                     </div>

//                     {error && (
//                         <div className={styles.errorMessage}>
//                             {error}
//                         </div>
//                     )}

//                     <button
//                         type="submit"
//                         className={styles.loginButton}
//                         disabled={loading}
//                     >
//                         {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
//                     </button>
//                 </form>

//                 <div className={styles.registerPrompt}>
//                     <p>¿No tienes cuenta?</p>
//                     <button
//                         onClick={onToggleMode}
//                         className={styles.toggleButton}
//                     >
//                         Regístrate ahora
//                     </button>
//                 </div>
//             </div>
//         </div>
//     );
// };

// export default Login;}
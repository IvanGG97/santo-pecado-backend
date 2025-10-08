import React, { useState } from 'react';
import styles from './Register.module.css';

export default function Register({ onRegisterSuccess, onSwitchToLogin }) {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [loading, setLoading] = useState(false);

    const isValidEmail = (email) => {
        const regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return regex.test(email.toLowerCase());
    };

    const isPasswordStrong = password.length >= 6;
    const passwordsMatch = password === confirmPassword && confirmPassword !== '';

    const isFormValid =
        username.trim() !== '' &&
        firstName.trim() !== '' &&
        lastName.trim() !== '' &&
        isValidEmail(email) &&
        isPasswordStrong &&
        passwordsMatch;

    const handleRegister = async () => {
        if (!isFormValid) {
            setErrorMessage('Por favor, completa todos los campos correctamente.');
            return;
        }
        setErrorMessage('');
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/empleado/register/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username,
                    email,
                    first_name: firstName,
                    last_name: lastName,
                    password,
                }),
            });
            if (response.ok) {
                onRegisterSuccess();
            } else {
                const data = await response.json();
                setErrorMessage(data.detail || 'Error al registrar usuario.');
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
                <img className={styles.img} src="https://i.imgur.com/w8KqDWP.jpeg" alt="santo pecado letras" />
            </div>
            <h2 className={`${styles.title} ${styles.neonText}`}>REGÍSTRATE AHORA</h2>

            <label className={styles.label}>Usuario</label>
            <input
                className={styles.input}
                type="text"
                placeholder="Ingrese su usuario"
                value={username}
                onChange={e => setUsername(e.target.value)}
            />

            <label className={styles.label}>Nombre</label>
            <input
                className={styles.input}
                type="text"
                placeholder="Ingrese su nombre"
                value={firstName}
                onChange={e => setFirstName(e.target.value)}
            />

            <label className={styles.label}>Apellido</label>
            <input
                className={styles.input}
                type="text"
                placeholder="Ingrese su apellido"
                value={lastName}
                onChange={e => setLastName(e.target.value)}
            />

            <label className={styles.label}>Correo</label>
            <input
                className={styles.input}
                type="email"
                placeholder="Ingrese su correo"
                value={email}
                onChange={e => setEmail(e.target.value)}
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

            <label className={styles.label}>Confirmar Contraseña</label>
            <div className={styles.passwordContainer}>
                <input
                    className={styles.input}
                    type={showConfirmPassword ? 'text' : 'password'}
                    placeholder="Confirme su contraseña"
                    value={confirmPassword}
                    onChange={e => setConfirmPassword(e.target.value)}
                />
                <button
                    type="button"
                    className={styles.showPasswordBtn}
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    aria-label="Mostrar u ocultar contraseña"
                >
                    {showConfirmPassword ? '🙈' : '👁️'}
                </button>
            </div>

            {errorMessage && <p className={styles.error}>{errorMessage}</p>}

            <button
                className={`${styles.button} ${!isFormValid ? styles.buttonDisabled : ''}`}
                onClick={handleRegister}
                disabled={!isFormValid || loading}
            >
                {loading ? 'Cargando...' : 'Registrarse'}
            </button>

            <p className={styles.switchText}>
                ¿Ya tienes cuenta?{' '}
                <button className={styles.linkButton} onClick={onSwitchToLogin}>
                    Inicia sesión
                </button>
            </p>
        </div>
    );
}





// import React, { useState } from 'react';
// import { useAuth } from '../../contexts/AuthContext';
// import styles from './Register.module.css';

// const Register = ({ onToggleMode }) => {
//     const [formData, setFormData] = useState({
//         username: '',
//         password: '',
//         password2: '',
//         email: '',
//         first_name: '',
//         last_name: '',
//         rol: ''
//     });
//     const [error, setError] = useState('');
//     const [loading, setLoading] = useState(false);
//     const { register } = useAuth();

//     const handleChange = (e) => {
//         setFormData({
//             ...formData,
//             [e.target.name]: e.target.value
//         });
//     };

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         setLoading(true);
//         setError('');

//         if (formData.password !== formData.password2) {
//             setError('Las contraseñas no coinciden');
//             setLoading(false);
//             return;
//         }

//         const result = await register(formData);
//         setLoading(false);

//         if (!result.success) {
//             setError(result.error || 'Error en el registro');
//         }
//     };

//     return (
//         <div className={styles.registerContainer}>
//             <div className={styles.registerCard}>
//                 <div className={styles.registerHeader}>
//                     <h2 className={styles.registerTitle}>SMTO PEONDO</h2>
//                     <p className={styles.registerSubtitle}>REGISTRATE AHORA</p>
//                 </div>

//                 <form onSubmit={handleSubmit} className={styles.registerForm}>
//                     <div className={styles.formRow}>
//                         <div className={styles.formGroup}>
//                             <label htmlFor="first_name" className={styles.label}>
//                                 Nombre
//                             </label>
//                             <input
//                                 id="first_name"
//                                 name="first_name"
//                                 type="text"
//                                 value={formData.first_name}
//                                 onChange={handleChange}
//                                 className={styles.input}
//                                 required
//                                 disabled={loading}
//                             />
//                         </div>

//                         <div className={styles.formGroup}>
//                             <label htmlFor="last_name" className={styles.label}>
//                                 Apellido
//                             </label>
//                             <input
//                                 id="last_name"
//                                 name="last_name"
//                                 type="text"
//                                 value={formData.last_name}
//                                 onChange={handleChange}
//                                 className={styles.input}
//                                 required
//                                 disabled={loading}
//                             />
//                         </div>
//                     </div>

//                     <div className={styles.formGroup}>
//                         <label htmlFor="username" className={styles.label}>
//                             Usuario
//                         </label>
//                         <input
//                             id="username"
//                             name="username"
//                             type="text"
//                             value={formData.username}
//                             onChange={handleChange}
//                             className={styles.input}
//                             required
//                             disabled={loading}
//                         />
//                     </div>

//                     <div className={styles.formGroup}>
//                         <label htmlFor="email" className={styles.label}>
//                             Email
//                         </label>
//                         <input
//                             id="email"
//                             name="email"
//                             type="email"
//                             value={formData.email}
//                             onChange={handleChange}
//                             className={styles.input}
//                             required
//                             disabled={loading}
//                         />
//                     </div>

//                     <div className={styles.formRow}>
//                         <div className={styles.formGroup}>
//                             <label htmlFor="password" className={styles.label}>
//                                 Contraseña
//                             </label>
//                             <input
//                                 id="password"
//                                 name="password"
//                                 type="password"
//                                 value={formData.password}
//                                 onChange={handleChange}
//                                 className={styles.input}
//                                 required
//                                 disabled={loading}
//                             />
//                         </div>

//                         <div className={styles.formGroup}>
//                             <label htmlFor="password2" className={styles.label}>
//                                 Confirmar Contraseña
//                             </label>
//                             <input
//                                 id="password2"
//                                 name="password2"
//                                 type="password"
//                                 value={formData.password2}
//                                 onChange={handleChange}
//                                 className={styles.input}
//                                 required
//                                 disabled={loading}
//                             />
//                         </div>
//                     </div>

//                     <div className={styles.formGroup}>
//                         <label htmlFor="rol" className={styles.label}>
//                             Rol
//                         </label>
//                         <select
//                             id="rol"
//                             name="rol"
//                             value={formData.rol}
//                             onChange={handleChange}
//                             className={styles.select}
//                             disabled={loading}
//                         >
//                             <option value="">Seleccionar rol</option>
//                             <option value="Cajero">Cajero</option>
//                             <option value="Administrador">Administrador</option>
//                             <option value="Cocinero">Cocinero</option>
//                         </select>
//                     </div>

//                     {error && (
//                         <div className={styles.errorMessage}>
//                             {error}
//                         </div>
//                     )}

//                     <button
//                         type="submit"
//                         className={styles.registerButton}
//                         disabled={loading}
//                     >
//                         {loading ? 'Creando cuenta...' : 'Registrarse'}
//                     </button>
//                 </form>

//                 <div className={styles.loginPrompt}>
//                     <p>¿Ya tienes cuenta?</p>
//                     <button
//                         onClick={onToggleMode}
//                         className={styles.toggleButton}
//                     >
//                         Iniciar sesión
//                     </button>
//                 </div>
//             </div>
//         </div>
//     );
// };

// export default Register;
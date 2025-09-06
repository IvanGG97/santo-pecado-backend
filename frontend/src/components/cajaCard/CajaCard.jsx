import React from 'react';
import styles from './CajaCard.module.css';

export default function CajaCard({ caja }) {
    // Definir la clase CSS basada en el estado de la caja
    const estadoClass = caja.caja_estado === 'Abierta' 
        ? styles.estadoAbierta 
        : styles.estadoCerrada;

    return (
        <div className={styles.card}>
            <table>
                <thead>
                    <tr>
                        <th>N° Caja</th>
                        <th>Estado</th>
                        <th>Fecha Apertura</th>
                        <th>Fecha Cierre</th>
                        <th>Monto Inicial</th>
                        <th>Monto Final</th>
                        <th>Accion</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{caja.id}</td>
                        <td><p className={`${caja.caja_estado ? styles.abierta : styles.cerrada}`}>{caja.caja_estado?"Abierto":"Cerrado"}</p></td>
                        <td>{caja.caja_fecha_hora_apertura.split('T')[0]} {caja.caja_fecha_hora_apertura.split('T')[1].split('.')[0]}</td>
                        <td>{caja.caja_fecha_hora_cierre}</td>
                        <td>{caja.caja_monto_inicial}</td>
                        <td>{caja.caja_saldo_final}</td>
                        <td>
                            {/* Aquí iría el botón o enlace para la acción */}
                            <button>Acción</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    );
}
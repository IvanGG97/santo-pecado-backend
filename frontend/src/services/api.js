const API_BASE_URL = 'http://localhost:8000';

export const authAPI = {
    login: async (username, password) => {
        const response = await fetch(`${API_BASE_URL}/api/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }

        return response.json();
    },

    register: async (userData) => {
        const response = await fetch(`${API_BASE_URL}/api/registro/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        });

        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }

        return response.json();
    },

    getProfile: async (token) => {
        const response = await fetch(`${API_BASE_URL}/api/perfil/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error('Error al obtener perfil');
        }

        return response.json();
    },

    refreshToken: async (refreshToken) => {
        const response = await fetch(`${API_BASE_URL}/api/token/refresh/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh: refreshToken }),
        });

        if (!response.ok) {
            throw new Error('Error al refrescar token');
        }

        return response.json();
    },
};
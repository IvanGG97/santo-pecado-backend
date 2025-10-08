import axios from 'axios';

const cajaApi=axios.create({
    baseURL:'http://localhost:8000/api/cajas',
    headers:{
        'Content-Type':'application/json'
    }
});

export const getCajas = async () => { 
    try{
        const response = await cajaApi.get('/');
        return response.data;
    }catch(error){
        console.log(error);
        throw error;
    }  
} 

export const getCaja = async (id) =>{
    try{
        const response = await cajaApi.get(`/${id}/`);
        return response.data;
    }catch(error){
        console.log(error);
        throw error;
    }  
}

export const createCaja = async (caja) => { 
    try{
        const response = await cajaApi.post('/', caja);
        return response.data;
    }catch(error){
        console.log(error);
        throw error;
    }  
} 

export const updateCaja = async (id, caja) => { 
    try{
        const response = await cajaApi.put(`/${id}/`, caja);
        return response.data;
    }catch(error){
        console.log(error);
        throw error;
    }  
}  

export const deleteCaja = async (id) => { 
    try{
        const response = await cajaApi.delete(`/${id}/`);
        return response.data;
    }catch(error){
        console.log(error);
        throw error;
    }  
}
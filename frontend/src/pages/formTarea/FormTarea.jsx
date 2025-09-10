import React from 'react'
import { useForm } from 'react-hook-form'
export default function FormTarea() {

    const { register, handleSubmit } = useForm()
    const onSubmit =(data)=>{
        console.log(data)
    }
  return (
    <div>
        <h1>Formulario de caja</h1>
        <form onSubmit={handleSubmit(onSubmit)}> 
            <div>
                <label> Titulo: </label>
                <input type="text" {...register("titulo")} />
            </div>
            <div>
                <label>Descripcion:</label>
                <input type="text"{...register("descripcion")} />
            </div>
            <button type="submit">Enviar</button>
        </form>
    </div>
  )
}

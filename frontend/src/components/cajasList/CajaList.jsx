import React, { useEffect,useState } from 'react'
import CajaCard from '../cajaCard/CajaCard'
import { getCajas } from '../../api/caja.api'


export default function CajaList() {
    const [cajas,setCajas]=useState([])

    useEffect(() =>{
        const fetchCajas = async () => {
            const cajas = await getCajas()
            console.log(cajas)
            setCajas(cajas)
        }
        fetchCajas()
    },[])


  return (
    <div>
        <div >
            {cajas.map((caja) => (
                <CajaCard key={caja.id} caja={caja} />
            ))}
        </div>
    </div>
  )
}

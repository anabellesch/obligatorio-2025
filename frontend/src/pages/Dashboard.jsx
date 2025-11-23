import React, { useEffect, useState } from "react";
import {
    BarChart, Bar,
    LineChart, Line,
    PieChart, Pie, Cell,
    XAxis, YAxis, Tooltip, CartesianGrid, Legend,
} from "recharts";

const API = "http://localhost:5000/api/reportes";

export default function Dashboard() {

    const [usoSalas, setUsoSalas] = useState([]);
    const [turnos, setTurnos] = useState([]);
    const [promedioParticipantes, setPromedioParticipantes] = useState([]);
    const [efectividadReservas, setEfectividadReservas] = useState([]);

    const [ocupacionEdificios, setOcupacionEdificios] = useState([]);
    const [ocupacionTiposSala, setOcupacionTiposSala] = useState([]);

    const [asistencias, setAsistencias] = useState([]);
    const [sanciones, setSanciones] = useState([]);

    const [prediccion, setPrediccion] = useState([]);

    useEffect(() => {
        // Salas más reservadas -> /salas-mas-reservadas
        fetch(`${API}/salas-mas-reservadas`).then(r => r.json()).then(data => {
            // map to { sala, reservas }
            setUsoSalas((data || []).map(d => ({ sala: d.nombre_sala, reservas: d.total_reservas })));
        }).catch(()=>setUsoSalas([]));

        // Turnos más demandados -> /turnos-mas-demandados
        fetch(`${API}/turnos-mas-demandados`).then(r => r.json()).then(data => {
            setTurnos((data || []).map(d => ({ turno: `${d.hora_inicio?.substring(0,5)} - ${d.hora_fin?.substring(0,5)}`, cantidad: d.total })));
        }).catch(()=>setTurnos([]));

        // Promedio participantes -> /promedio-participantes
        fetch(`${API}/promedio-participantes`).then(r => r.json()).then(data => {
            setPromedioParticipantes((data || []).map(d => ({ sala: d.nombre_sala, promedio: Number(d.promedio_participantes) })));
        }).catch(()=>setPromedioParticipantes([]));

        // Efectividad reservas -> /efectividad-reservas (returns an object)
        fetch(`${API}/efectividad-reservas`).then(r => r.json()).then(data => {
            if (!data) { setEfectividadReservas([]); return; }
            const arr = [
                { estado: 'utilizadas', cantidad: data.utilizadas || 0 },
                { estado: 'canceladas', cantidad: data.canceladas || 0 },
                { estado: 'sin asistencia', cantidad: data.sin_asistencia || 0 },
                { estado: 'activas', cantidad: data.activas || 0 },
            ];
            setEfectividadReservas(arr);
        }).catch(()=>setEfectividadReservas([]));

        // Ocupacion por edificio -> /ocupacion-por-edificio
        fetch(`${API}/ocupacion-por-edificio`).then(r => r.json()).then(data => {
            setOcupacionEdificios((data || []).map(d => ({ edificio: d.nombre_edificio, porcentaje: Number(d.porcentaje_ocupacion || 0) })));
        }).catch(()=>setOcupacionEdificios([]));

        // Uso por tipo de sala -> /uso-por-tipo-sala
        fetch(`${API}/uso-por-tipo-sala`).then(r => r.json()).then(data => {
            // Use total_reservas as the metric for the pie
            setOcupacionTiposSala((data || []).map(d => ({ tipo: d.tipo_sala, porcentaje: Number(d.total_reservas || 0) })));
        }).catch(()=>setOcupacionTiposSala([]));

        // Participantes más activos -> usar para asistencias
        fetch(`${API}/participantes-mas-activos`).then(r => r.json()).then(data => {
            setAsistencias((data || []).map(p => ({ usuario: `${p.nombre} ${p.apellido}`, asistencias: Number(p.total_asistencias || 0) })));
            // also use this data for sanciones chart fallback (if no dedicated sanciones data)
            setSanciones((data || []).map(p => ({ usuario: `${p.nombre} ${p.apellido}`, sanciones: Number(p.total_reservas || 0) })));
        }).catch(()=>{ setAsistencias([]); setSanciones([]); });

        // Prediccion -> /prediccion-disponibilidad
        fetch(`${API}/prediccion-disponibilidad`).then(r => r.json()).then(data => {
            // Map to something the chart can use: use sala name as 'dia' and probability as 'probabilidad'
            setPrediccion((data || []).map((d, i) => ({ dia: d.nombre_sala || `Sala ${i+1}`, probabilidad: Number(d.probabilidad_disponibilidad || 0) })));
        }).catch(()=>setPrediccion([]));
    }, []);

    return (
        <div className="p-6 space-y-12" style={{ backgroundColor: '#ffffff', color: '#0b2a66', minHeight: '100vh' }}>

            <h1 className="text-3xl font-bold mb-6">Dashboard de Reportes</h1>

            {/* --- USO DE SALAS --- */}
            <section>
                <h2 className="text-xl font-semibold mb-2">Salas más reservadas</h2>
                <BarChart width={600} height={300} data={usoSalas}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="sala" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="reservas" />
                </BarChart>
            </section>

            {/* --- TURNOS --- */}
            <section>
                <h2 className="text-xl font-semibold mb-2">Turnos más demandados</h2>
                <BarChart width={600} height={300} data={turnos}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="turno" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="cantidad" />
                </BarChart>
            </section>

            {/* --- PROMEDIO PARTICIPANTES --- */}
            <section>
                <h2 className="text-xl font-semibold mb-2">Promedio de participantes por sala</h2>
                <LineChart width={600} height={300} data={promedioParticipantes}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="sala" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="promedio" />
                </LineChart>
            </section>

            {/* --- EFECTIVIDAD --- */}
            <section>
                <h2 className="text-xl font-semibold mb-2">Reservas efectivas vs canceladas/no asistidas</h2>
                <BarChart width={600} height={300} data={efectividadReservas}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="estado" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="cantidad" />
                </BarChart>
            </section>

            {/* --- OCUPACIÓN POR EDIFICIO --- */}
            <section>
                <h2 className="text-xl font-semibold mb-2">Ocupación por edificio</h2>
                {
                    // If there is no meaningful data (all zeros or empty), show a placeholder message
                    (() => {
                        const totalPerc = ocupacionEdificios.reduce((s, it) => s + (Number(it.porcentaje) || 0), 0);
                        if (!ocupacionEdificios.length || totalPerc === 0) {
                            return (
                                <div style={{ width: 600, height: 350, display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid #e6e6e6', borderRadius: 8 }}>
                                    <span style={{ color: '#0b2a66', fontWeight: 600 }}>No hay datos de ocupación para mostrar</span>
                                </div>
                            );
                        }
                        return (
                            <PieChart width={600} height={350}>
                                <Pie
                                    data={ocupacionEdificios}
                                    dataKey="porcentaje"
                                    nameKey="edificio"
                                    cx="50%"
                                    cy="50%"
                                    outerRadius={120}
                                >
                                    {ocupacionEdificios.map((_, i) => <Cell key={i} />)}
                                </Pie>
                                <Tooltip />
                            </PieChart>
                        );
                    })()
                }
            </section>

            {/* --- OCUPACIÓN POR TIPO DE SALA --- */}
            <section>
                <h2 className="text-xl font-semibold mb-2">Ocupación por tipo de sala</h2>
                <PieChart width={600} height={350}>
                    <Pie
                        data={ocupacionTiposSala}
                        dataKey="porcentaje"
                        nameKey="tipo"
                        cx="50%"
                        cy="50%"
                        outerRadius={120}
                    >
                        {ocupacionTiposSala.map((_, i) => <Cell key={i} />)}
                    </Pie>
                    <Tooltip />
                </PieChart>
            </section>

            {/* --- ASISTENCIAS --- */}
            <section>
                <h2 className="text-xl font-semibold mb-2">Asistencias de alumnos y profesores</h2>
                <LineChart width={600} height={300} data={asistencias}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="usuario" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line dataKey="asistencias" />
                </LineChart>
            </section>

            {/* --- SANCIONES --- */}
            <section>
                <h2 className="text-xl font-semibold mb-2">Sanciones por usuario</h2>
                <BarChart width={600} height={300} data={sanciones}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="usuario" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="sanciones" />
                </BarChart>
            </section>

            {/* --- PREDICCIÓN --- */}
            <section>
                <h2 className="text-xl font-semibold mb-2">Predicción de disponibilidad</h2>
                <LineChart width={600} height={300} data={prediccion}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="dia" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line dataKey="probabilidad" />
                </LineChart>
            </section>

        </div>
    );
}

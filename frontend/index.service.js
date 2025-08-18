// // Servicio para gestionar peticiones a la API
// const API_URL = 'http://localhost:5000/api/buscar';

// export async function buscarPersonas(descripcion, numResultados) {
//   const response = await fetch(API_URL, {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({ descripcion, numResultados })
//   });
//   if (!response.ok) throw new Error('Error en la petición');
//   return await response.json();
// }

// Servicio para gestionar peticiones a la API
// En Azure y en local (con la CLI) será siempre /api/buscar
const API_URL = '/api/buscar';

export async function buscarPersonas(descripcion, numResultados) {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ descripcion, numResultados })
  });
  if (!response.ok) throw new Error('Error en la petición');
  return await response.json();
}

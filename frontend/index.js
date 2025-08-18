// Transpilación rápida del TypeScript para pruebas en vivo
// (No incluye tipado ni comprobaciones avanzadas)

var peoplePool = [
  { name: 'Ana Torres', image: 'https://randomuser.me/api/portraits/women/44.jpg' },
  { name: 'Luis Gómez', image: 'https://randomuser.me/api/portraits/men/32.jpg' },
  { name: 'María López', image: 'https://randomuser.me/api/portraits/women/68.jpg' },
  { name: 'Carlos Ruiz', image: 'https://randomuser.me/api/portraits/men/15.jpg' },
  { name: 'Sofía Martínez', image: 'https://randomuser.me/api/portraits/women/21.jpg' },
  { name: 'Javier Pérez', image: 'https://randomuser.me/api/portraits/men/45.jpg' },
  { name: 'Lucía Fernández', image: 'https://randomuser.me/api/portraits/women/12.jpg' },
  { name: 'Miguel Ángel', image: 'https://randomuser.me/api/portraits/men/23.jpg' },
  { name: 'Paula Castro', image: 'https://randomuser.me/api/portraits/women/37.jpg' },
  { name: 'Diego Sánchez', image: 'https://randomuser.me/api/portraits/men/56.jpg' }
];

var form = document.getElementById('searchForm');
var input = document.getElementById('descriptionInput');
var results = document.getElementById('results');
var clearBtn = document.getElementById('clearBtn');
var numResults = document.getElementById('numResults');

// Importar el servicio
// Si usas módulos, asegúrate de que index.js se carga como type="module" en el HTML
// import { buscarPersonas } from './index.service.js';
// Si no usas módulos, puedes copiar la función buscarPersonas aquí
async function buscarPersonas(descripcion, numResultados) {
  const response = await fetch('http://localhost:5000/api/buscar', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ descripcion, numResultados })
  });
  if (!response.ok) throw new Error('Error en la petición');
  return await response.json();
}

form.addEventListener('submit', async function(e) {
  e.preventDefault();
  var desc = input.value.trim();
  var n = parseInt(numResults.value, 10);
  // Mostrar barra de carga animada y texto con puntos
  results.innerHTML = `
    <div class="progress-container">
      <div class="progress-bar indeterminate" id="progressBar"></div>
      <div class="progress-text" id="progressText">Buscando Imágenes</div>
    </div>
  `;
  let dots = 0;
  let maxDots = 3;
  let interval = setInterval(() => {
    dots = (dots + 1) % (maxDots + 1);
    let text = 'Buscando Imágenes' + '.'.repeat(dots);
    document.getElementById('progressText').textContent = text;
  }, 400);
  try {
    const data = await buscarPersonas(desc, n);
    clearInterval(interval);
    setTimeout(() => renderResults(data), 300);
  } catch (err) {
    clearInterval(interval);
    results.innerHTML = '<div style="color:#e30613;text-align:center;">Error al buscar resultados</div>';
  }
});

// ...existing code...
function renderResults(persons) {
  console.log('Renderizando resultados:', persons); // Debug
  results.innerHTML = '';
  persons.forEach(function(person, index) {
    console.log(`Persona ${index}:`, person); // Debug cada persona
    var card = document.createElement('div');
    card.className = 'person-card';
    card.innerHTML = `
      <img src="http://localhost:5000/imagenes/${person.imagen}" alt="${person.imagen || 'Sin imagen'}" />
      <div class="person-name">${person.imagen || 'Sin nombre'}</div>
      <div class="similarity">Similitud: ${(person.similitud * 100).toFixed(1)}%</div>
    `;
    results.appendChild(card);
  });
}

clearBtn.addEventListener('click', function() {
  input.value = '';
  results.innerHTML = '';
  input.focus();
});

// function renderResults(persons) {
//   results.innerHTML = '';
//   persons.forEach(function(person) {
//     var card = document.createElement('div');
//     card.className = 'person-card';
//     card.innerHTML = '\n      <img src="' + person.image + '" alt="' + person.name + '" />\n      <div class="person-name">' + person.name + '</div>\n    ';
//     results.appendChild(card);
//   });
// }

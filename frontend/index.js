// Usa el servicio
import { buscarPersonas, IMG_BASE } from './index.service.js';

const form = document.getElementById('searchForm');
const input = document.getElementById('descriptionInput');
const results = document.getElementById('results');
const clearBtn = document.getElementById('clearBtn');
const numResults = document.getElementById('numResults');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const desc = input.value.trim();
  const n = parseInt(numResults.value, 10);

  results.innerHTML = `
    <div class="progress-container">
      <div class="progress-bar indeterminate" id="progressBar"></div>
      <div class="progress-text" id="progressText">Buscando Imágenes</div>
    </div>
  `;

  let dots = 0;
  const maxDots = 3;
  const interval = setInterval(() => {
    dots = (dots + 1) % (maxDots + 1);
    document.getElementById('progressText').textContent =
      'Buscando Imágenes' + '.'.repeat(dots);
  }, 400);

  try {
    const data = await buscarPersonas(desc, n);
    clearInterval(interval);
    setTimeout(() => renderResults(data), 300);
  } catch (err) {
    clearInterval(interval);
    console.error(err);
    results.innerHTML =
      '<div style="color:#e30613;text-align:center;">Error al buscar resultados</div>';
  }
});

function renderResults(persons) {
  results.innerHTML = '';
  persons.forEach((person) => {
    const card = document.createElement('div');
    card.className = 'person-card';
    const src = `${IMG_BASE}${encodeURIComponent(person.imagen)}`;
    card.innerHTML = `
      <img src="${src}" alt="${person.imagen || 'Sin imagen'}" />
      <div class="person-name">${person.imagen || 'Sin nombre'}</div>
      <div class="similarity">Similitud: ${(person.similitud * 100).toFixed(1)}%</div>
    `;
    results.appendChild(card);
  });
}

clearBtn.addEventListener('click', () => {
  input.value = '';
  results.innerHTML = '';
  input.focus();
});

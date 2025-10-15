
const API_BASE = "http://localhost:8000/api"
const ACTUALIZAR_INTERVALO = 1000 // 1 segundo

// ELEMENTOS DEL DOM 
const canvas = document.getElementById("relojCanvas")
const ctx = canvas.getContext("2d")
const displayTiempo = document.getElementById("displayTiempo")
const btnSincronizar = document.getElementById("btnSincronizar")
const btnAjustar = document.getElementById("btnAjustar")
const modal = document.getElementById("modalAjustar")
const btnGuardar = document.getElementById("btnGuardar")
const btnCancelar = document.getElementById("btnCancelar")
const inputHoras = document.getElementById("inputHoras")
const inputMinutos = document.getElementById("inputMinutos")
const inputSegundos = document.getElementById("inputSegundos")

// VARIABLES GLOBALES 
let tiempoActual = { horas: 12, minutos: 0, segundos: 0 }

// FUNCIONES DE API
async function obtenerTiempo() {
  try {
    const response = await fetch(`${API_BASE}/tiempo`)
    const data = await response.json()
    tiempoActual = data
    actualizarDisplay()
    dibujarReloj()
  } catch (error) {
    console.error("Error al obtener tiempo:", error)
  }
}

async function sincronizarConSistema() {
  try {
    const response = await fetch(`${API_BASE}/sincronizar`)
    const data = await response.json()
    tiempoActual = data
    actualizarDisplay()
    dibujarReloj()
  } catch (error) {
    console.error("Error al sincronizar:", error)
  }
}

async function ajustarTiempo(horas, minutos, segundos) {
  try {
    const response = await fetch(`${API_BASE}/ajustar?horas=${horas}&minutos=${minutos}&segundos=${segundos}`)
    const data = await response.json()
    tiempoActual = data
    actualizarDisplay()
    dibujarReloj()
  } catch (error) {
    console.error("Error al ajustar tiempo:", error)
  }
}

//  FUNCIONES DE DIBUJO
function dibujarReloj() {
  const centerX = canvas.width / 2
  const centerY = canvas.height / 2
  const radius = 180

  // Limpiar canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  // Dibujar fondo del reloj (rosado)
  ctx.beginPath()
  ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI)
  ctx.fillStyle = "#fce7f3"
  ctx.fill()
  ctx.strokeStyle = "#ec4899"
  ctx.lineWidth = 8
  ctx.stroke()

  // Dibujar marcas de horas
  dibujarMarcasHoras(centerX, centerY, radius)

  // Dibujar números
  dibujarNumeros(centerX, centerY, radius)

  // Dibujar manecillas
  dibujarManecillaHoras(centerX, centerY, radius)
  dibujarManecillaMinutos(centerX, centerY, radius)
  dibujarManecillaSegundos(centerX, centerY, radius)

  // Dibujar centro
  ctx.beginPath()
  ctx.arc(centerX, centerY, 12, 0, 2 * Math.PI)
  ctx.fillStyle = "#ec4899"
  ctx.fill()
}

function dibujarMarcasHoras(centerX, centerY, radius) {
  ctx.strokeStyle = "#ec4899"
  ctx.lineWidth = 3

  for (let i = 0; i < 12; i++) {
    const angle = ((i * 30 - 90) * Math.PI) / 180
    const x1 = centerX + Math.cos(angle) * (radius - 20)
    const y1 = centerY + Math.sin(angle) * (radius - 20)
    const x2 = centerX + Math.cos(angle) * (radius - 10)
    const y2 = centerY + Math.sin(angle) * (radius - 10)

    ctx.beginPath()
    ctx.moveTo(x1, y1)
    ctx.lineTo(x2, y2)
    ctx.stroke()
  }
}

function dibujarNumeros(centerX, centerY, radius) {
  ctx.font = "bold 24px Arial"
  ctx.fillStyle = "#4b5563"
  ctx.textAlign = "center"
  ctx.textBaseline = "middle"

  for (let i = 1; i <= 12; i++) {
    const angle = ((i * 30 - 90) * Math.PI) / 180
    const x = centerX + Math.cos(angle) * (radius - 45)
    const y = centerY + Math.sin(angle) * (radius - 45)
    ctx.fillText(i.toString(), x, y)
  }
}

function dibujarManecillaHoras(centerX, centerY, radius) {
  const { horas, minutos } = tiempoActual
  const angle = ((((horas % 12) + minutos / 60) * 30 - 90) * Math.PI) / 180
  const length = radius * 0.5

  ctx.beginPath()
  ctx.moveTo(centerX, centerY)
  ctx.lineTo(centerX + Math.cos(angle) * length, centerY + Math.sin(angle) * length)
  ctx.strokeStyle = "#1f2937"
  ctx.lineWidth = 8
  ctx.lineCap = "round"
  ctx.stroke()
}

function dibujarManecillaMinutos(centerX, centerY, radius) {
  const { minutos } = tiempoActual
  const angle = ((minutos * 6 - 90) * Math.PI) / 180
  const length = radius * 0.7

  ctx.beginPath()
  ctx.moveTo(centerX, centerY)
  ctx.lineTo(centerX + Math.cos(angle) * length, centerY + Math.sin(angle) * length)
  ctx.strokeStyle = "#4b5563"
  ctx.lineWidth = 6
  ctx.lineCap = "round"
  ctx.stroke()
}

function dibujarManecillaSegundos(centerX, centerY, radius) {
  const { segundos } = tiempoActual
  const angle = ((segundos * 6 - 90) * Math.PI) / 180
  const length = radius * 0.8

  ctx.beginPath()
  ctx.moveTo(centerX, centerY)
  ctx.lineTo(centerX + Math.cos(angle) * length, centerY + Math.sin(angle) * length)
  ctx.strokeStyle = "#ec4899"
  ctx.lineWidth = 3
  ctx.lineCap = "round"
  ctx.stroke()
}

function actualizarDisplay() {
  const { horas, minutos, segundos } = tiempoActual
  const horasStr = horas.toString().padStart(2, "0")
  const minutosStr = minutos.toString().padStart(2, "0")
  const segundosStr = segundos.toString().padStart(2, "0")
  displayTiempo.textContent = `${horasStr}:${minutosStr}:${segundosStr}`
}

// ==================== EVENT LISTENERS ====================
btnSincronizar.addEventListener("click", () => {
  sincronizarConSistema()
})

btnAjustar.addEventListener("click", () => {
  inputHoras.value = tiempoActual.horas
  inputMinutos.value = tiempoActual.minutos
  inputSegundos.value = tiempoActual.segundos
  modal.classList.add("activo")
})

btnGuardar.addEventListener("click", () => {
  const horas = Number.parseInt(inputHoras.value)
  const minutos = Number.parseInt(inputMinutos.value)
  const segundos = Number.parseInt(inputSegundos.value)

  if (horas >= 1 && horas <= 12 && minutos >= 0 && minutos <= 59 && segundos >= 0 && segundos <= 59) {
    ajustarTiempo(horas, minutos, segundos)
    modal.classList.remove("activo")
  } else {
    alert("Por favor ingresa valores válidos")
  }
})

btnCancelar.addEventListener("click", () => {
  modal.classList.remove("activo")
})

// Cerrar modal al hacer clic fuera
modal.addEventListener("click", (e) => {
  if (e.target === modal) {
    modal.classList.remove("activo")
  }
})

// ==================== INICIALIZACIÓN ====================
// Obtener tiempo inicial
obtenerTiempo()

// Actualizar cada segundo
setInterval(obtenerTiempo, ACTUALIZAR_INTERVALO)

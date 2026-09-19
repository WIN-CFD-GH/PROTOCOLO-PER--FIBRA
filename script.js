let evaluationsData = {};
let currentEval = [];
let userData = {};
let timerInterval = null;
let timeLeft = 3600; // 60 minutos en segundos

// Navegación entre pantallas
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screenId).classList.add('active');
}

// Cargar datos del JSON
async function loadEvaluations() {
    try {
        const response = await fetch('evaluations_data.json');
        evaluationsData = await response.json();
    } catch (error) {
        console.error("Error loading evaluations:", error);
        alert("No se pudieron cargar las evaluaciones. Asegúrate de ejecutar el servidor (server.py).");
    }
}

// Inicializar la app
document.addEventListener('DOMContentLoaded', () => {
    loadEvaluations();

    // Iniciar evaluación
    document.getElementById('form-home').addEventListener('submit', (e) => {
        e.preventDefault();
        
        userData = {
            nombres: document.getElementById('nombres').value,
            apellidos: document.getElementById('apellidos').value,
            dni: document.getElementById('dni').value,
            codigo: document.getElementById('codigo').value,
            campana: document.getElementById('campana').value,
            evaluacion: document.getElementById('evaluacion').value
        };

        startEvaluation(userData.evaluacion);
    });

    // Enviar evaluación
    document.getElementById('btn-submit-quiz').addEventListener('click', () => submitQuiz(false));

    // Botón volver al inicio
    document.getElementById('btn-back-home').addEventListener('click', () => {
        document.getElementById('form-home').reset();
        showScreen('screen-home');
    });

    // Panel de Admin
    document.getElementById('admin-btn').addEventListener('click', () => {
        const pwd = prompt("Ingrese contraseña de administrador:");
        if (pwd === "admin123") { // Contraseña simple
            loadAdminData();
            showScreen('screen-admin');
        } else if (pwd !== null) {
            alert("Contraseña incorrecta.");
        }
    });

    document.getElementById('btn-admin-close').addEventListener('click', () => {
        showScreen('screen-home');
    });
});

function startEvaluation(evalName) {
    currentEval = evaluationsData[evalName];
    if (!currentEval || currentEval.length === 0) {
        alert("Esta evaluación no tiene preguntas disponibles.");
        return;
    }

    document.getElementById('quiz-title').textContent = evalName;
    const container = document.getElementById('quiz-container');
    container.innerHTML = '';

    currentEval.forEach((q, index) => {
        const block = document.createElement('div');
        block.className = 'question-block';
        
        const qTitle = document.createElement('div');
        qTitle.className = 'question-text';
        qTitle.textContent = `${index + 1}. ${q.question}`;
        
        const optionsContainer = document.createElement('div');
        optionsContainer.className = 'options-container';

        q.options.forEach((opt, optIndex) => {
            const label = document.createElement('label');
            label.className = 'option-label';
            
            const radio = document.createElement('input');
            radio.type = 'radio';
            radio.name = `q-${index}`;
            radio.value = optIndex;
            
            const span = document.createElement('span');
            span.textContent = opt;

            label.appendChild(radio);
            label.appendChild(span);
            optionsContainer.appendChild(label);
        });

        block.appendChild(qTitle);
        block.appendChild(optionsContainer);
        container.appendChild(block);
    });

    showScreen('screen-quiz');
    window.scrollTo(0, 0);

    // Iniciar temporizador
    timeLeft = 3600;
    updateTimerDisplay();
    clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        timeLeft--;
        updateTimerDisplay();
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            alert("¡Se acabó el tiempo! Tu evaluación será enviada automáticamente.");
            submitQuiz(true); // Enviar forzosamente
        }
    }, 1000);
}

function updateTimerDisplay() {
    const m = Math.floor(timeLeft / 60).toString().padStart(2, '0');
    const s = (timeLeft % 60).toString().padStart(2, '0');
    const timerSpan = document.querySelector('#timer-display span');
    if (timerSpan) {
        timerSpan.textContent = `${m}:${s}`;
    }
}

async function submitQuiz(force = false) {
    // Validar que se hayan respondido todas
    const total = currentEval.length;
    let answered = 0;
    let correct = 0;
    let errors = [];

    for (let i = 0; i < total; i++) {
        const selected = document.querySelector(`input[name="q-${i}"]:checked`);
        if (selected) {
            answered++;
            const selectedVal = parseInt(selected.value);
            if (selectedVal === currentEval[i].correctIndex) {
                correct++;
            } else {
                errors.push({
                    question: currentEval[i].question,
                    userAnswer: currentEval[i].options[selectedVal],
                    correctAnswer: currentEval[i].options[currentEval[i].correctIndex]
                });
            }
        }
    }

    if (!force && answered < total) {
        if (!confirm(`Has respondido ${answered} de ${total} preguntas. ¿Seguro que deseas enviar la evaluación?`)) {
            return;
        }
    }

    // Detener temporizador
    clearInterval(timerInterval);

    // Calcular nota proporcional a 20
    const finalScore = Math.round((correct / total) * 20);
    userData.nota = finalScore;
    userData.total = 20; // Sistema vigesimal

    // Mostrar resultados
    document.getElementById('final-score').textContent = `${finalScore}/20`;
    
    const errorsContainer = document.getElementById('errors-container');
    errorsContainer.innerHTML = '<h3>Resumen de Errores:</h3>';
    
    if (errors.length === 0) {
        errorsContainer.innerHTML += '<p style="color: var(--color-success); font-weight: 600;">¡Felicidades! No tuviste ningún error.</p>';
    } else {
        errors.forEach(err => {
            const errDiv = document.createElement('div');
            errDiv.className = 'error-item';
            errDiv.innerHTML = `
                <div class="error-q">${err.question}</div>
                <div class="error-wrong">Tu respuesta: ${err.userAnswer}</div>
                <div class="error-correct">Respuesta correcta: ${err.correctAnswer}</div>
            `;
            errorsContainer.appendChild(errDiv);
        });
    }

    // Guardar en el servidor
    try {
        await fetch('/api/save_grade', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
    } catch (e) {
        console.error("Error al guardar nota:", e);
    }

    showScreen('screen-results');
    window.scrollTo(0, 0);
}

async function loadAdminData() {
    try {
        const response = await fetch('/api/get_grades');
        const data = await response.json();
        
        const tbody = document.getElementById('admin-tbody');
        tbody.innerHTML = '';
        
        // Mostrar los últimos primero
        data.reverse().forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.Fecha || '-'}</td>
                <td>${row.nombres || '-'}</td>
                <td>${row.apellidos || '-'}</td>
                <td>${row.dni || '-'}</td>
                <td>${row.codigo || '-'}</td>
                <td>${row.campana || '-'}</td>
                <td>${row.evaluacion || '-'}</td>
                <td><strong>${row.nota || 0}/20</strong></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error("Error cargando data de admin:", e);
    }
}

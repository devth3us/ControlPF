const video = document.getElementById('webcam');
const canvas = document.getElementById('canvasFrame');
const ctx = canvas.getContext('2d');


navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => { video.srcObject = stream; })
    .catch(err => { console.error("Erro ao acessar a câmera:", err); alert("Libere o acesso à câmera!"); });


document.getElementById('btnCapturar').addEventListener('click', async () => {
    const btn = document.getElementById('btnCapturar');
    btn.innerText = "Processando Imagem...";
    btn.disabled = true;

    // Desenha o frame atual do vídeo no canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Converte para imagem base64
    const imageData = canvas.toDataURL('image/png');

    // Usa a biblioteca Tesseract.js para extrair o texto da imagem
    try {
        const { data: { text } } = await Tesseract.recognize(imageData, 'eng');
        const placaExtraida = text.replace(/[^a-zA-Z0-9]/g, ''); // Limpa caracteres estranhos
        
        if(placaExtraida.length > 4) {
            consultarBanco(placaExtraida);
        } else {
            alert("Não foi possível ler a placa com clareza. Tente aproximar o papel.");
        }
    } catch (err) {
        console.error("Erro no OCR:", err);
    }

    btn.innerText = "📸 Ler Placa na Câmera";
    btn.disabled = false;
});


document.getElementById('btnSimular').addEventListener('click', () => {
    const placa = document.getElementById('placaManual').value;
    if(placa) consultarBanco(placa);
});


async function consultarBanco(placa) {
    const response = await fetch('/api/verificar_placa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ placa: placa })
    });
    const result = await response.json();
    abrirModal(result);
}

// 5. Interface Visual (Modal e Cancela)
function abrirModal(result) {
    const modal = document.getElementById('modalProfessor');
    const statusBanner = document.getElementById('modalStatus');
    const cancela = document.getElementById('cancelaVisual');

    modal.style.display = 'flex';

    if(result.status === 'autorizado') {
        document.getElementById('modalFoto').src = result.dados.foto_url;
        document.getElementById('modalNome').innerText = result.dados.nome;
        document.getElementById('modalMateria').innerText = result.dados.materia;
        
        statusBanner.innerText = "ACESSO LIBERADO";
        statusBanner.className = "status-banner autorizado";
        cancela.classList.add('aberta');

        // Fecha a cancela e o modal automaticamente após 5 segundos
        setTimeout(() => {
            cancela.classList.remove('aberta');
            fecharModal();
        }, 5000);

    } else {
        document.getElementById('modalFoto').src = "https://via.placeholder.com/120?text=Bloqueado";
        document.getElementById('modalNome').innerText = "Desconhecido";
        document.getElementById('modalMateria').innerText = "---";
        
        statusBanner.innerText = "ACESSO NEGADO: " + result.mensagem;
        statusBanner.className = "status-banner negado";
        cancela.classList.remove('aberta');
    }
}

function fecharModal() {
    document.getElementById('modalProfessor').style.display = 'none';
    document.getElementById('placaManual').value = '';
}
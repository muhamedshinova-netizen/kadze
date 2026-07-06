const tg = window.Telegram.WebApp;
tg.ready();

document.getElementById('uploadArea').addEventListener('click', () => {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (ev) => {
            document.getElementById('preview').src = ev.target.result;
            document.getElementById('preview').style.display = 'block';
            document.getElementById('uploadText').style.display = 'none';
            document.getElementById('categories').style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});

const stylesMap = {
    portrait: ['лесной дух', 'мягкий портрет'],
    nature: ['закат над водой', 'цветущий сад'],
    city: ['улочки старого города', 'ночной квартал'],
    interior: ['уютное кафе', 'каминная'],
    fantasy: ['магический лес', 'парящие острова']
};

document.getElementById('categorySelect').addEventListener('change', (e) => {
    const styleSelect = document.getElementById('styleSelect');
    styleSelect.innerHTML = '';
    stylesMap[e.target.value].forEach(s => {
        const opt = document.createElement('option');
        opt.value = s;
        opt.text = s;
        styleSelect.appendChild(opt);
    });
});
document.getElementById('categorySelect').dispatchEvent(new Event('change'));

document.getElementById('generateBtn').addEventListener('click', () => {
    const fileInput = document.getElementById('fileInput');
    if (!fileInput.files.length) return alert('Выберите фото!');
    
    const category = document.getElementById('categorySelect').value;
    const style = document.getElementById('styleSelect').value;
    
    tg.sendData(JSON.stringify({
        action: 'generate',
        category: category,
        style: style
    }));
    
    document.getElementById('status').innerText = 'Теперь отправь это фото в чат с ботом!';
});

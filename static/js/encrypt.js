// tải file khi nhấn download
const downloadButton = document.getElementById('download-cipher');
downloadButton.addEventListener('click', () => {
    const downloadUrl = 'http://localhost:5000/download-cipher';  
    window.location.href = downloadUrl;
});

const downloadButton2 = document.getElementById('download-plain');
downloadButton2.addEventListener('click', () => {
    const downloadUrl2 = 'http://localhost:5000/download-plain';  
    window.location.href = downloadUrl2;
});




const pdfUrl = document.currentScript.getAttribute('data-pdf-url');
const pdfjsLib = window['pdfjs-dist/build/pdf'];
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.worker.min.js';

// Renderize o PDF
pdfjsLib.getDocument(pdfUrl).promise.then(pdf => {
    // Carregue a primeira página
    for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber++) {
        pdf.getPage(pageNumber).then(page => {
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');

            // Defina a escala de renderização
            const viewport = page.getViewport({ scale: 1.5 });

            // Ajuste o tamanho do canvas à escala do PDF
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            // Adicione o canvas à página
            document.getElementById('teste').appendChild(canvas);

            // Renderize a página PDF no canvas
            const renderContext = {
                canvasContext: context,
                viewport: viewport
            };
            page.render(renderContext);
        });
    }
});
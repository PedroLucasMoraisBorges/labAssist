let table = base.getTable('Processing');
const fields = ['midia', 'ocr', 'created_time'];

async function processImage(imageUrl) {
    let visionApiUrl = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyAPdNNXoixzKubOS0Lb2vVJKJj8LbJfiD0';
    let requestBody = {
        requests: [{
            image: { source: { imageUri: imageUrl } },
            features: [{ type: 'DOCUMENT_TEXT_DETECTION' }]
        }]
    };

    let visionResponse = await fetch(visionApiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
    });

    if (!visionResponse.ok) {
        throw new Error(`HTTP error! status: ${visionResponse.status}`);
    }

    let visionData = await visionResponse.json();
    if (visionData.responses[0].fullTextAnnotation) {
        return visionData.responses[0].fullTextAnnotation.text;
    } else {
        console.log('No text detected in image');
        return '';
    }
}

async function main() {
    try {
        // Get the record ID from the input variable
        const procRecordId = input.config().procRecordId;
        console.log(`Processing record ID: ${procRecordId}`);

        if (!procRecordId) {
            throw new Error('No record ID provided');
        }

        // Fetch the specific record
        let record = await table.selectRecordAsync(procRecordId);

        if (!record) {
            throw new Error(`Record with ID ${procRecordId} not found`);
        }

        let imageData = record.getCellValue('midia');
        if (!imageData) {
            throw new Error('No image data found in the record');
        }

        // Parse the JSON string to get the array of image objects
        let imageObjects = JSON.parse(imageData);

        console.log('Processing images...');
        let allOcrText = '';

        for (let imageObject of imageObjects) {
            console.log(`Processing image: ${imageObject.filename}`);
            let ocrText = await processImage(imageObject.url);
            allOcrText += `--- ${imageObject.filename} ---\n\n${ocrText}\n\n`;
        }

        if (allOcrText.trim()) {
            await table.updateRecordAsync(record, {
                'ocr': allOcrText.trim()
            });
            console.log('OCR process completed successfully for all images');
        } else {
            console.log('No text extracted from any of the images');
        }
    } catch (error) {
        console.error('An error occurred:', error.message, error.stack);
    }
}

// Run the main function
main();


function formatText(annotation) {
    let formattedText = '';
    for (let page of annotation.pages) {
        for (let block of page.blocks) {
            for (let paragraph of block.paragraphs) {
                let paragraphText = paragraph.words.map(word => word.symbols.map(s => s.text).join('')).join(' ');
                formattedText += paragraphText + '\n\n'; // Parágrafo com espaçamento
            }
        }
    }
    return formattedText.trim();
}

function organizeApostille(text) {
    const apostilleKeys = [
        'Foi assinado por:', 'Na qualidade de:', 'Tem o selo /carimbo de:', 'Em:', 
        'No dia:', 'Por:', 'N°:', 'Firma:', 'Tipo de Documento:', 'Nome do Titular:'
    ];
    let organizedText = '';
    for (let key of apostilleKeys) {
        let match = new RegExp(`${key}.*`, 'i').exec(text);
        if (match) organizedText += `${match[0]}\n`;
    }
    return organizedText.trim();
}

async function main() {
    try {
        let visionData = await processImage(imageUrl);
        if (visionData.responses[0].fullTextAnnotation) {
            let rawText = visionData.responses[0].fullTextAnnotation.text;
            let structuredText = formatText(visionData.responses[0].fullTextAnnotation);
            let finalText = organizeApostille(structuredText);

            await table.updateRecordAsync(record, {
                'ocr': finalText
            });
            console.log('Texto processado com sucesso');
        } else {
            console.log('Nenhum texto detectado');
        }
    } catch (error) {
        console.error('Erro:', error.message);
    }
}
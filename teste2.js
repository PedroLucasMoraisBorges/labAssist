// PDF Generator API configuration | Dynamically selected model ID
const apiKey = '9c762298e2a44b59f724e70ca3cce28cbd96475efd00dc27705ac9c94a09c125';
const apiSecret = 'e9b26d9c83b927589cf721aba4fd69d3da0ae1497035d542cc0956709b7fe3cd';
const apiWorkspace = 'bruno@estudio37.com.br';

// Airtable tables configuration
const certificatesTable = base.getTable('Certificates');


async function generatePdfName(record) {
    let version = record.getCellValue('version');
    let certificateType = record.getCellValue('tipo');
    let certificateName = record.getCellValue('nome_do_titular').split(' ')[0];
    let secondName = record.getCellValue('nome_do_titular').split(' ')[1];

    // Convert to a string and ensure it has at least three digits, padding with zeros if necessary
    let formattedVersion = String(version).padStart(3, '0');

    let nameDocument = `${certificateType.name}_BR_${certificateName}_${secondName}_v${formattedVersion}.pdf`;

    return nameDocument;
}

async function getTemplateId(record){
    let verso = record.getCellValue('corpo_verso')
    let url = ''
    console.log(!verso)
    if (!verso) {
        const templateId = '1318359';
        url = `https://us1.pdfgeneratorapi.com/api/v3/templates/${templateId}/output?output=url`;
    }
    else {
        const templateId = '1304687';
        url = `https://us1.pdfgeneratorapi.com/api/v3/templates/${templateId}/output?output=url`;
    }

    return url
}

async function generatePdf(record, brData) {
    const url = await getTemplateId(record)
    
    // Prepare data for the PDF template
    let pdfData = {
        certidao : record.getCellValue('certidao'),
        nome: record.getCellValue('nome'),
        matricula: record.getCellValue('matricula'),
        corpo: record.getCellValue('corpo'),
        assinatura: record.getCellValue('assinatura'),
        oficio: record.getCellValue('oficio'),
        emolumentos: record.getCellValue('emolumentos'),
        foi_assinado_por: record.getCellValue('foi_assinado_por'),
        na_qualidade_de: record.getCellValue('na_qualidade_de'),
        tem_selo_carimbo_de: record.getCellValue('tem_selo_carimbo_de'),
        em: record.getCellValue('em'),
        no_dia: record.getCellValue('no_dia'),
        por: record.getCellValue('por'),
        'num': record.getCellValue('num'),
        firma: record.getCellValue('firma'),
        tipo_de_documento: record.getCellValue('tipo_de_documento'),
        nome_do_titular: record.getCellValue('nome_do_titular')
    };

    console.log('Preparing PDF data...');
    console.log('PDF data prepared:', JSON.stringify(pdfData));

    console.log('Preparing PDF Br data...');
    console.log('PDF data prepared:', brData);

    try {
        console.log('Sending request to PDF Generator API...');
        console.log('API Key:', apiKey);
        console.log('API Workspace:', apiWorkspace);
        console.log('API Secret (first 4 chars):', apiSecret.substring(0, 4) + '...');
        const brDataJson = JSON.parse(brData);
        var body = Object.assign({}, pdfData, brDataJson);
        console.log('Body', body)

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Auth-Key': apiKey,
                'X-Auth-Secret': apiSecret,
                'X-Auth-Workspace': apiWorkspace
            },
            body: JSON.stringify(body),
        });

        console.log('Response received. Status:', response.status);

        if (!response.ok) {
            const errorBody = await response.text();
            console.error('API Response:', response.status, response.statusText);
            console.error('Response body:', errorBody);
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Full API response:', JSON.stringify(result, null, 2));

        if (typeof result.response === 'string' && result.response.startsWith('https://')) {
            console.log('PDF URL found in response:', result.response);
            return result.response;
        } else {
            console.error('PDF URL not found or invalid in the API response');
            return null;
        }
    } catch (error) {
        console.error("Failed to generate PDF:", error.message);
        console.error("Error details:", error);
        return null;
    }
}

async function main() {
    try {
        // Get the triggering record ID from the exportarData input
        const config = input.config()

        const recordId = config.exportarData;
        const brData = config.brData;

        console.log(`Record ID from input: ${recordId}`);

        if (!recordId) {
            throw new Error('No record ID provided in the exportarData');
        }

        // Fetch the specific record that triggered the automation
        const record = await certificatesTable.selectRecordAsync(recordId);
    
        console.log(`Record fetched: ${record ? 'Yes' : 'No'}`);

        if (!record) {
            throw new Error('Record not found');
        }

        const saveDocToField = await generatePdfName(record);

        const exportarValue = record.getCellValue('exportar');
        console.log(`Exportar value: ${exportarValue}`);

        if (exportarValue !== '[>>]') {
            console.log('Export trigger not set. Exiting.');
            return;
        }

        console.log('Generating PDF...');
        let pdfUrl = await generatePdf(record, brData);
        console.log(`PDF URL generated:`, pdfUrl);

        if (pdfUrl) {
            console.log('Updating record with PDF URL...');
            await certificatesTable.updateRecordAsync(record, {
                ['translation pdf']: [{url: pdfUrl, filename: saveDocToField}],
                'exportar': ''
            });
            console.log('PDF generated and attached successfully');
        } else {
            console.log('Failed to generate PDF');
        }

    } catch (error) {
        console.error('An error occurred:', error.message, error.stack);
    }
}

// Run the main function
await main();
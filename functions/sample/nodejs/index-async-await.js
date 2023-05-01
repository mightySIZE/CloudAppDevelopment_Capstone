/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY  });
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl("params.COUCH_URL");

    try {
        // Access the 'dealerships' database
        const dbName = 'dealerships';
        
        // Fetch all documents from the 'dealerships' database
        const allDocs = await cloudant.postAllDocs({
            db: dbName,
            includeDocs: true
        });

        // Extract the dealership documents
        const dealerships = allDocs.result.rows.map(row => row.doc);

        return { "dealerships": dealerships };
    } catch (error) {
        console.error('Error:', error);
        return { error: error.description };
    }
}
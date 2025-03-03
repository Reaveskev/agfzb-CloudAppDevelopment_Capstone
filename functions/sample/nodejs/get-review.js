const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {

    const authenticator = new IamAuthenticator({ apikey: "" })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl("https://7ee132cb-9734-4ac3-bd3e-a65c47e2eea7-bluemix.cloudantnosqldb.appdomain.cloud");

    let dbListPromise = getReviews(cloudant);
    return dbListPromise;
}

function getReviews(cloudant) {
    return new Promise((resolve, reject) => {
        cloudant.postAllDocs({ db: "reviews", includeDocs: true }) 
            .then((result) => {
                let code = 200;
                if (result.result.total_rows === 0) {
                    code = 404;
                }
                resolve({
                    statusCode: code,
                    headers: { "Content-Type": "application/json" },
                    body: result.result.rows.map(row => row.doc) 
                });
            })
            .catch(err => {
                console.log(err);
                reject({ err: err });
            });
    });
}
 

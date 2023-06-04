const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");

function main(params) {
    return new Promise(function (resolve, reject) {
     
      const authenticator = new IamAuthenticator({
        apikey: "", 
      });
      const cloudant = CloudantV1.newInstance({
        authenticator: authenticator,
      });
      cloudant.setServiceUrl("https://7ee132cb-9734-4ac3-bd3e-a65c47e2eea7-bluemix.cloudantnosqldb.appdomain.cloud"); // TODO: Replace with your Cloudant service URL
   
      let doc = params.review;
      doc.id = Math.floor(Math.random() * (80 - 15) + 15);
      cloudant
        .postDocument({
          db: "reviews",
          document: doc,
        })
        .then((result) => {
          let code = 201;
          resolve({
            statusCode: code,
            headers: { "Content-Type": "application/json" },
          });
        })
        .catch((err) => {
          reject(err);
        });
    });
  }
  
  
  // {
  //   "review": {
  //   "title": "Great Product",
  //   "content": "I really enjoyed using this product. It has great features and is very user-friendly.",
  //   "rating": 5
  // }
  // }
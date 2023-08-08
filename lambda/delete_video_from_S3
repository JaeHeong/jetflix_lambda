//람다 함수 작성
const aws = require("aws-sdk");

exports.handler = (event, context, callback) => {
    const s3 = new aws.S3({
    apiVersion: '2006-03-01',
    signatureVersion: 'v4',
    });
  
    console.log(event);
    const id = event.id;
    var i;
    var params = {
    Bucket: "db-jh", 
    Key: ""
    };
   
    const keyArray = [`${id}/bg.jpeg`, `${id}/post.jpeg`,`${id}/pv.mp4`,`${id}/`];
    
    for (i=0;i<keyArray.length;i++){
      params.Key = keyArray[i];
       s3.deleteObject(params, function(err, data) {
     if (err) console.log(err, err.stack); // an error occurred
     else     console.log(data);           // successful response
   });
    }
    
    const corsHeader = {
        "Access-Control-Allow-Headers":
        "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods":
        "DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT",
        "Access-Control-Allow-Origin": "*"
    };
  
    callback(null, {
        'headers': corsHeader,
        'statusCode': 200,
        // 'body': JSON.stringify(id)
    });
};


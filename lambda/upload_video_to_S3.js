//람다 함수 작성
const aws = require("aws-sdk");

exports.handler = (event, context, callback) => {
  const s3 = new aws.S3({
  apiVersion: '2006-03-01',
  signatureVersion: 'v4',
});
  const request = JSON.parse(event.body);
  
  const key = request.key;
  const type = request.type;
  const id = request.id;
  
  const params = { 
    Bucket: 'db-jh', 
    Key: `${id}/${key == "background" ? "bg" : key == "poster" ? "post" : "pv"}.${key == "background" ||  key == "poster" ? "jpeg" : "mp4"}`,
    Expires: 300,// In seconds
    // presigned URL의 유효시간의 기본값은 15분 입니다.
  };
  s3.getSignedUrl("putObject", params, function(err, url){
    if(err) return callback(err);
    callback(null,{
      statusCode: 200,
      headers:{'Access-Control-Allow-Origin':'*'},
      body: url //생성 된 presigned URL을 프론트로 보냄
    });
  });
};

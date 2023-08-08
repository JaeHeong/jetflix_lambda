import sys
import logging
import pymysql
import json
from urllib import parse

def lambda_handler(event, context):
    rds_host = "db-test.cdiqjebgtx3e.ap-northeast-2.rds.amazonaws.com"
    user_name = "admin"
    password = "cloudneta"
    db_name = "ASSETS"
    
    keyword = parse.unquote(event ["pathParameters"]["keyword"])
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    try:
        conn = pymysql.connect(
            host=rds_host, user=user_name, passwd=password, db=db_name, connect_timeout=5
        )
        logger.info("연결 성공!")
    except pymysql.MySQLError as e:
        logger.error("연결 실패!")
        logger.error(e)
        sys.exit()
        
    cur = conn.cursor()
    
    sql_insert = f"select * from ASSET where replace(title,' ','') like '%{keyword}%'"
    
    cur.execute(sql_insert)

    items = cur.fetchall()

    json_array = []
    
    for item in items:
        json_object = {
        "id": item[0],
        "title":item[1],
        "overview":item[2]
        }
        json_array.append(json_object)

    conn.close()

    return {
        "statusCode": 200,
        "body": json.dumps(json_array),
        "headers": {"Access-Control-Allow-Headers":
                "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods":
                "DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT",
            "Access-Control-Allow-Origin":
                "*"},
    }

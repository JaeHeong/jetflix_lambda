import sys
import logging
import pymysql
import json
import boto3

# Create an S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    rds_host = "db-test.cdiqjebgtx3e.ap-northeast-2.rds.amazonaws.com"
    user_name = "admin"
    password = "cloudneta"
    db_name = "ASSETS"
    
    id = event ["pathParameters"]["id"]
    
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

    sql_insert = f"delete from ASSET where ID={id}"
    
    cur.execute(sql_insert)
    conn.commit()

    conn.close()
    
    
    return {
        "id": id
    }
    

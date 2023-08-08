import sys
import logging
import pymysql
import json
import base64

def lambda_handler(event, context):
    rds_host = "db-test.cdiqjebgtx3e.ap-northeast-2.rds.amazonaws.com"
    user_name = "admin"
    password = "cloudneta"
    db_name = "ASSETS"
    
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
        
    id = json.loads(base64.b64decode((event['Records'][0]['kinesis']["data"])))['id']
    
    print()
    
    cur = conn.cursor()

    sql_update = f"update ASSET set count = count + 1 where ID={id};"
    
    cur.execute(sql_update)
    conn.commit()
    
    # sql_get_id = f"select ID from ASSET where title='{title}';"
    # cur.execute(sql_get_id)
    # id = cur.fetchall()[-1][0]

    # sql_update = f"UPDATE ASSET SET bgPath='{id}/{bgPath}', posterPath='{id}/{posterPath}', videoPath='{id}/{videoPath}' WHERE ID={id};"
    # cur.execute(sql_update)
    # conn.commit()


    conn.close()

    return {
        "statusCode": 200,
        "body": "Hello World",
        "headers": {"Access-Control-Allow-Headers":
                "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods":
                "DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT",
            "Access-Control-Allow-Origin":
                "*"},
    }

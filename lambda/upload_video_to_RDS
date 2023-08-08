import sys
import logging
import pymysql
import json

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
    
    body=json.loads(event["body"])
    
    title = body["title"]
    overview = body["overview"]
    # bgPath = event["bgPath"]
    # posterPath = event["posterPath"]
    # videoPath = event["videoPath"]

    cur = conn.cursor()

    sql_insert = f"insert into ASSET (title, overview) values('{title}', '{overview}')"
    
    cur.execute(sql_insert)
    conn.commit()
    
    sql_get_id = f"select ID from ASSET where title='{title}';"
    cur.execute(sql_get_id)
    id = cur.fetchall()[-1][0]

    # sql_update = f"UPDATE ASSET SET bgPath='{id}/{bgPath}', posterPath='{id}/{posterPath}', videoPath='{id}/{videoPath}' WHERE ID={id};"
    # cur.execute(sql_update)
    # conn.commit()


    conn.close()

    return {
        "statusCode": 200,
        "body": json.dumps( id , default=str),
        "headers": {"Access-Control-Allow-Headers":
                "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods":
                "DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT",
            "Access-Control-Allow-Origin":
                "*"},
    }

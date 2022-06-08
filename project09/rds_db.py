import pymysql
conn = pymysql.connect(
        host= "emp-database.cruq67uutafa.ap-south-1.rds.amazonaws.com", #endpoint link
        port = "3306", # 3306
        user = "admin", # admin
        password = "adminadmin", #adminadmin
        db = "empdb", #test
        
        )


def insert_details(name,email,comment,gender):
    cur=conn.cursor()
    cur.execute("INSERT INTO empdata (ename,email,ephno,exp,apt,gdscore,hrscore,location) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (ename,email,ephno,exp,apt,gdscore,hrscore,location))
    conn.commit()

def get_details():
    cur=conn.cursor()
    cur.execute("SELECT *  FROM empdata")
    details = cur.fetchall()
    return details
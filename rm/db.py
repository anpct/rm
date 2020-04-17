import mysql.connector
import datetime
import h
conn = mysql.connector.connect(
  host="****",
  user="****",
  passwd="****",
  database="****",
  port=3306
)
cur = conn.cursor(buffered=True)


def ck_details(username, password):
    try:
        cur.execute("SELECT PASSWORD FROM USERS WHERE ID='{}'".format(username))
        row = cur.fetchone()
        if row != None and h.verify_password(row[0], password):
            return True
        else:
            return False
    except Exception:
        return False


def add_rem(date, rem, uid, email):
    try:
        sql = "INSERT INTO REM VALUES ('{}', '{}', '{}', '{}')".format(uid, date, rem, email)
        cur.execute(sql)
        conn.commit()
        return
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def get_related_rem(uid):
    try:
        cur.execute("SELECT * FROM REM WHERE ID='{}' ORDER BY DATE".format(uid))
        return cur
    except Exception:
        return


def get_mails():
    try:
        x = datetime.datetime.now()
        cur.execute("SELECT ID,REMAIL,REMT FROM REM WHERE DATE='{}'".format(x.strftime("%Y-%m-%d")))
        return cur
    except Exception:
        return


def add_user(email, password):
    try:
        hpass = h.hash_password(password)
        sql = "INSERT INTO USERS VALUES ('{}', '{}')".format(email, hpass)
        cur.execute(sql)
        conn.commit()
        return
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def delete_rem(text):
    try:
        sql = "DELETE FROM REM WHERE REMT='{}'".format(text)
        cur.execute(sql)
        conn.commit()
        return
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))



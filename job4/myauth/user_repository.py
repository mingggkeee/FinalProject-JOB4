class UserRepository:

    def __init__(self):
        self.connection_info = { 'host': '13.124.236.54', 'db': 'job4', 'user': 'ssac', 'password': 'Ssac123!@#', 'charset': 'utf8' }

    def select_count_by_userid(self, name_key):

        import pymysql

        conn = pymysql.connect(**self.connection_info)
        cursor = conn.cursor()

        sql = "select count(*) cnt from myauth_user where id=%s"
        cursor.execute(sql, (name_key,))

        rows = cursor.fetchall() # 반환 값은 tuple의 list [ (...), (...), ..., (...) ]
        
        conn.close()

        return rows[0]

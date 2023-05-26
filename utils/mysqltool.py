import pymysql
import time

class MySQLTool:

    def __init__(self, host, username, password, database, timeout=60):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.timeout = timeout
        self.connection = None
        self.connect()

    def connect(self):
        self.connection = pymysql.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            db=self.database,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=self.timeout,
            autocommit=True,
            port=3306
        )

    def close(self):
        self.connection.close()

    def ping(self):
        try:
            self.connection.ping()
        except pymysql.MySQLError as e:
            print(f"Ping failed! Reconnecting due to {e}")
            self.connect()

    def select(self, table_name, columns=None, where=None, order_by=None, limit=None, group_by=None):
        self.ping()
        try:
            with self.connection.cursor() as cursor:
                sql = f"SELECT {','.join(columns) if columns else '*'} FROM {table_name}"
                if where:
                    sql += f" WHERE {where}"
                if group_by:
                    sql += f" GROUP BY {group_by}"
                if order_by:
                    sql += f" ORDER BY {order_by}"
                if limit:
                    sql += f" LIMIT {limit}"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except pymysql.Error as error:
            print(f"Failed to select data from table {table_name}. Error: {error}")
            return None
        finally:
            self.ping()
    # 其它增删改操作方法，可以在其中调用 ping() 方法
    def insert(self, table_name, data):
        try:
            with self.connection.cursor() as cursor:
                columns = ','.join(list(data.keys()))
                values = ','.join([f"'{str(value)}'" for value in data.values()])
                sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                cursor.execute(sql)
                self.connection.commit()
        except pymysql.Error as error:
            print(f"Failed to insert data into table {table_name}. Error: {error}")
        finally:
            self.ping()

    def update(self, table_name, data, where=None):
        try:
            with self.connection.cursor() as cursor:
                set_values = ','.join([f"{key}='{value}'" for key, value in data.items()])
                sql = f"UPDATE {table_name} SET {set_values}"
                if where is not None:
                    sql += f" WHERE {where}"
                cursor.execute(sql)
                self.connection.commit()
        except pymysql.Error as error:
            print(f"Failed to update data in table {table_name}. Error: {error}")
        finally:
            self.ping()

    def delete(self, table_name, where=None):
        try:
            with self.connection.cursor() as cursor:
                sql = f"DELETE FROM {table_name}"
                if where is not None:
                    sql += f" WHERE {where}"
                cursor.execute(sql)
                self.connection.commit()
        except pymysql.Error as error:
            print(f"Failed to delete data from table {table_name}. Error: {error}")
        finally:
            self.ping()


# if __name__ == '__main__':
#     # 实例化 MySQL 工具类
#     db_tool = MySQLTool(host='192.168.1.201', username='ecm', password='123456', database='ecm')

#     # 每隔 10 秒钟查询一次数据库
#     while True:
#         # 查询数据
#         result = db_tool.select(table_name='nodedata', columns=['id', 'node_name'])
#         print(result)

#         # 插入数据
#         data = {'node_name': 'Jack', 'cpu_load': 25, 'power': '178'}
#         db_tool.insert(table_name='nodedata', data=data)
#         result = db_tool.select(table_name='nodedata', columns=['id', 'node_name'])
#         print(result)

#         # 更新数据
#         data = {'node_name': 'node2', 'cpu_load': 30}
#         db_tool.update(table_name='nodedata', data=data, where="id=1")
#         result = db_tool.select(table_name='nodedata', columns=['id', 'node_name'])
#         print(result)

#         # 删除数据
#         db_tool.delete(table_name='nodedata', where="node_name='node2'")
#         time.sleep(10)
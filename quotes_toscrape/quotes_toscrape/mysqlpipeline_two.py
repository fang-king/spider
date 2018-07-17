import pymysql
from twisted.enterprise import adbapi


class MysqlPipelineTwo(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor
        )
        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        dbpool = adbapi.ConnectionPool('pymysql',**adbparams)
        # 返回实例化参数
        return cls(dbpool)

    def process_item(self,item,spider):
        # 使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        query = self.dbpool.runInteraction(self.do_insert,item)
        # 添加异常处理
        query.addCallback(self.handle_error)

    def do_insert(self,cursor,item):
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        insert_sql = """
        insert into test_zxf(quote,author,tags,born_date,born_location) VALUES(%s,%s,%s,%s,%s)
                    """
        cursor.execute(insert_sql,(item['quote'],item['author'],item['tags'],item['born_date'],
                                        item['born_location']))
        return item

    def handle_error(self,failure):
        if failure:
            # 打印错误信息
            print(failure)
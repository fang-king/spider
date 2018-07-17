import pymysql
import redis
import pandas

redis_db = redis.Redis(host='127.0.0.1',port=6379,db=1) # 连接本地redis，db数据库默认连接到0号库，写的是索引值
redis_data_dict = ''  # key的名字，里面的内容随便写，这里的key相当于字典名称，而不是key值。为了后面引用而建的


class MysqlRemovePipeline(object):
    def __init__(self):
        self.conn = pymysql.connect('localhost','root','Abcd1234','test')  # 连接mysql
        self.cursor = self.conn.cursor()  # 建立游标
        # print(redis_db)
        redis_db.flushdb()  # 清空当前数据库中的所有 key，为了后面将mysql数据库中的数据全部保存进去
        # print(redis_db)
        if redis_db.hlen(redis_data_dict) == 0:  # 判断redis数据库中的key，若不存在就读取mysql数据并临时保存在redis中
            sql = 'select url from test_zxf'  # 查询表中的现有数据
            df = pandas.read_sql(sql,self.conn)  # 读取mysql中的数据
             # print(df)
            for url in df['url'].get_values():
                redis_db.hset(redis_data_dict,url,0) # 把每个url写入field中，value值随便设，我设置的0  key field value 三者的关系

    def process_item(self,item,spider):
        """
        比较爬取的数据在数据库中是否存在，不存在则插入数据库
        :param item: 爬取到的数据
        :param spider: /
        """
        if redis_db.hexists(redis_data_dict,item['url']): # 比较的是redis_data_dict里面的field
            print("数据库已经存在该条数据，不再继续追加")
        else:
            self.do_insert(item)

    def do_insert(self, item):
        insert_sql = """
                insert into test_zxf(quote,author,tags,url,born_date,born_location) VALUES(%s,%s,%s,%s,%s,%s)
                            """
        self.cursor.execute(insert_sql, (item['quote'], item['author'], item['tags'], item['url'],
                                         item['born_date'], item['born_location']))
        self.conn.commit()  # 提交操作，提交了才真正保存到数据库中
        return item

    def close_spider(self,spider):
        self.cursor.close()  # 关闭游标
        self.conn.close()    # 关闭连接
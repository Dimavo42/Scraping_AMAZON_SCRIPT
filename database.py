import psycopg2

class Control:
    def __init__(self,host,dbname,user,password,port):
        try:
           self.con=psycopg2.connect(host=host,dbname=dbname,user=user,password=password,port=port)

        except Exception as error:
            print(error)

    def creat_and_insert(self,data,name_scraped):### CREATING AN TABLE
        cur=self.con.cursor()
        exists = self.__checkTableExists('scrapy_{}'.format(name_scraped))
        create_script = 'CREATE TABLE scrapy_{} (Name varchar(2000),Price DOUBLE PRECISION,link varchar(2000),Stars varchar(2000),Shipping varchar(2000));'.format(
            name_scraped)
        if not exists:
            cur.execute(create_script)
        insert_script = 'INSERT INTO scrapy_{} (Name,Price,link,Stars,Shipping) VALUES(%s,%s,%s,%s,%s)'.format(
            name_scraped)
        for ind, val in data.items():
            cur.execute(insert_script, tuple(val.values()))
        self.con.commit()
        cur.close()

    def __checkTableExists(self,tablename):### check if the table EXISTS
        cur = self.con.cursor()
        script = """SELECT EXISTS (
       SELECT FROM information_schema.tables 
       WHERE  table_schema = 'public'
       AND    table_name   = '{}'
       );
       """.format(tablename)
        cur.execute(script)
        if cur.fetchone()[0] == 1:
            cur.close()
            return True
        cur.close()
        return False

    def __del__(self): ### DESTRCTOUR OF CLASS
        self.con.close()

    def find_average_price(self,name):
        cur = self.con.cursor()
        exists = self.__checkTableExists('scrapy_{}'.format(name))
        if not exists:
            print('the Table is not exists')
        else:
            try:
                script = 'SELECT AVG(price) FROM scrapy_{};'.format(name)
                cur.execute(script)
                return cur.fetchone()[0]
            except Exception as error:
                print(error)
            finally:
                if cur is not None:
                    cur.close()

    def find_lowest_price_or_highst(self, name,base):  ### BASE is GETTING the ORDER 1 is ascending ~~~~~ 2 is Descending 
        cur = self.con.cursor()
        exists = self.__checkTableExists('scrapy_{}'.format(name))
        if not exists:
            print('the Table is not exists')
        else:
            if(base==1):
                order='ASC'
            else:
                order = 'DESC'
            script = """ 
              SELECT  Name,Price,link,Stars,Shipping 
              FROM scrapy_{}
              WHERE (Price >0)
               ORDER BY Price {};
            """.format(name,order)
            try:
                cur.execute(script)
                for name in cur.fetchall():
                    yield {'name':name[0],'price':name[1]}
                cur.close()
            except Exception as error:
                print(error)
            finally:
                if cur is not None:
                    cur.close()







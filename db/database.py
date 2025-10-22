import psycopg
from requirment.logs import logger
from os import getenv

class Connection:
    __DATABASE = "passenger"
    __USERNAME = "tina"
    __PASSWORD = 1111
    __HOST = "localhost"
    __PORT = 5432

    def __enter__(self):
        try:
            self.__connection = psycopg.connect(
                dbname=self.__DATABASE,
                user=self.__USERNAME,
                password=self.__PASSWORD,
                host=self.__HOST,
                port=self.__PORT,
            )
            self.__curser = self.__connection.cursor()
            
            return self
        except Exception as e:
            logger.critical(f"{e}; Connection To Database Failed")

    def __exit__(self, a, b, c):
        if self.__curser:
            self.__curser.close()
        if self.__connection:
            self.__connection.close()
        

    def GET(self, query):
        try:
            self.__curser.execute(query)
            
            return self.__curser.fetchall()
        except Exception as e:
            logger.critical(f"Could Not GET Data")

    def POST(self, *query):
        try:
            for q in query:
                self.__curser.execute(q)
            self.__connection.commit()
            
        except Exception as e:
            self.__connection.rollback()
            logger.critical(f"Could Not POST Data {e}")
            raise e
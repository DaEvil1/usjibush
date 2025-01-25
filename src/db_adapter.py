import psycopg, os

class DBAdapter:

    def __init__(self, db_config, logger):
        self.db_config = db_config
        self.logger = logger
        self.current_id = 0

    async def connect(self):
        self.logger.info("Connecting to database")
        self.conn = psycopg.connect(**self.db_config)
        self.cur = self.conn.cursor()
        self.logger.info("Connected to database")

    async def init(self):
        self.logger.info("Initializing database")
        current_dir = os.path.dirname(os.path.realpath(__file__))
        sql_file = open(current_dir + "/schema.sql", "r")
        sql = sql_file.read()
        self.cur.execute(sql)
        self.conn.commit()
        self.logger.info("Initialized database")

    async def close(self):
        self.logger.info("Closing database connection")
        self.cur.close()
        self.conn.close()
        self.logger.info("Closed database connection")

    async def execute(self, query, args=None):
        self.current_id += 1
        id = self.current_id
        self.logger.info(f"id: {id} - Executing query: {query}")
        self.cur.execute(query, args)
        self.logger.info("id: {id} - Query executed")
        return self.cur.fetchall()

    async def execute_one(self, query, args=None):
        self.current_id += 1
        id = self.current_id
        self.logger.info(f"id: {self.current_id} - Executing query: {query}")
        self.cur.execute(query, args)
        self.logger.info("id: {id} - Query executed")
        return self.cur.fetchone()

    async def fetchall(self):
        self.current_id += 1
        id = self.current_id
        self.logger.info(f"id: {id} - Fetching all results")
        result = self.cur.fetchall()
        self.logger.info(f"id: {id} - Fetched all results")
        return result

    async def fetchone(self):
        self.current_id += 1
        id = self.current_id
        self.logger.info(f"id: {id} - Fetching one result")
        result = self.cur.fetchone()
        self.logger.info(f"id: {id} - Fetched one result")
        return result

    async def commit(self):
        self.conn.commit()
        self.logger.info("Committed transaction")

    async def rollback(self):
        self.conn.rollback()
        self.logger.info("Rolled back transaction")
import psycopg, os

class DBAdapter:

    def __init__(self, db_config, logger):
        self.db_config = db_config
        self.logger = logger
        self.current_id = 0

    async def connect(self):
        self.logger.info("Connecting to database")
        self.logger.info("Connected to database")

    async def init(self):
        self.logger.info("Initializing database")
        current_dir = os.path.dirname(os.path.realpath(__file__))
        sql_file = open(current_dir + "/schema.sql", "r")
        sql = sql_file.read()
        async with await psycopg.AsyncConnection.connect(**self.db_config) as connection:
            async with connection.cursor() as cur:
                await cur.execute(sql)
            await connection.commit()
        self.logger.info("Initialized database")

    async def close(self):
        pass

    async def execute(self, query: str, args: dict = None):
        self.current_id += 1
        id = self.current_id
        self.logger.info(f"job id: {id} - Executing query: {query}")
        columns: list = []
        result: list = []
        async with await psycopg.AsyncConnection.connect(**self.db_config) as connection:
            async with connection.cursor() as cur:
                await cur.execute(query, args)
                if cur.description:
                    columns: list = [desc[0] for desc in cur.description]
                    result = await self.cursor.fetchall()
        self.logger.info("job id: {id} - Query executed")
        return await self._return_result(result, columns)

    async def execute_one(self, query: str, args: dict = None):
        self.current_id += 1
        id = self.current_id
        self.logger.info(f"job id: {self.current_id} - Executing query: {query}")
        columns: list = []
        result: list = []
        async with await psycopg.AsyncConnection.connect(**self.db_config) as connection:
            async with connection.cursor() as cur:
                await cur.execute(query, args)
                if cur.description:
                    columns: list = [desc[0] for desc in cur.description]
                    result = await self.cursor.fetchone()
        self.logger.info("job id: {id} - Query executed")
        return await self._return_result(result, columns)

    async def fetchall(self, query: str, args: dict = None):
        self.current_id += 1
        id = self.current_id
        self.logger.info(f"job id: {id} - Fetching all results")
        async with await psycopg.AsyncConnection.connect(**self.db_config) as connection:
            async with connection.cursor() as cur:
                await cur.execute(query, args)
                result = await cur.fetchall()
                columns: list = [desc[0] for desc in cur.description]
        self.logger.info(f"job id: {id} - Fetched all results")
        return await self._return_result(result, columns)

    async def fetchone(self, query: str, args: dict = None):
        self.current_id += 1
        id = self.current_id
        self.logger.info(f"job id: {id} - Fetching one result")
        async with await psycopg.AsyncConnection.connect(**self.db_config) as connection:
            async with connection.cursor() as cur:
                await cur.execute(query, args)
                result = await cur.fetchone()
                result = [result] if result else []
                columns: list = [desc[0] for desc in cur.description]
        self.logger.info(f"job id: {id} - Fetched one result")
        return await self._return_result(result, columns)

    async def commit(self):
        async with await psycopg.AsyncConnection.connect(**self.db_config) as connection:
            await connection.commit()
        self.logger.info("Committed transaction")

    async def rollback(self):
        async with await psycopg.AsyncConnection.connect(**self.db_config) as connection:
            await connection.rollback()
        self.logger.info("Rolled back transaction")

    async def _return_result(self, result, columns):
        return [dict(zip(columns, row)) for row in result]
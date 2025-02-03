class QueryBuilderService:
    def __init__(self, connection, table):  # Fixed here (double underscores)
        self.connection = connection
        self.table = table
        self.select_columns = '*'
        self.joins = []
        self.where_clauses = []
        self.limit_value = None
        self.offset_value = None

    def select(self, *columns):
        if columns:
            self.select_columns = ', '.join(columns)
        return self

    def leftJoin(self, table, on):
        self.joins.append(f"LEFT JOIN {table} ON {on}")
        return self

    def where(self, column, value):
        self.where_clauses.append(f"{column} = '{value}'")
        return self

    def whereIn(self, column, values):
        values_list = ', '.join(f"'{v}'" for v in values)
        self.where_clauses.append(f"{column} IN ({values_list})")
        return self

    def limit(self, limit):
        self.limit_value = limit
        return self

    def offset(self, offset):
        self.offset_value = offset
        return self

    def get(self):
        query = f"SELECT {self.select_columns} FROM {self.table} "
        if self.joins:
            query += ' '.join(self.joins) + ' '
        if self.where_clauses:
            query += "WHERE " + ' AND '.join(self.where_clauses) + ' '
        if self.limit_value is not None:
            query += f"LIMIT {self.limit_value} "
        if self.offset_value is not None:
            query += f"OFFSET {self.offset_value} "
        return self.execute_query(query)

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
class QueryBuilderService:
    def __init__(self, connection, table):
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
        query = self.build_query()
        return self.execute_query(query)

    def first(self):
        self.limit_value = 1  # Fetch only one record
        query = self.build_query()
        results = self.execute_query(query)
        return results[0] if results else None

    def paginate(self, per_page=10, page=1):
        offset = (page - 1) * per_page
        self.limit_value = per_page
        self.offset_value = offset

        # Total count
        total_query = f"SELECT COUNT(*) FROM {self.table} " + self.build_where_clause()
        total = self.execute_scalar(total_query)

        # Paginated data
        data = self.get()

        return {
            "total": total,
            "per_page": per_page,
            "current_page": page,
            "last_page": (total + per_page - 1) // per_page,
            "data": data
        }

    def build_query(self):
        query = f"SELECT {self.select_columns} FROM {self.table} "
        if self.joins:
            query += ' '.join(self.joins) + ' '
        query += self.build_where_clause()
        if self.limit_value is not None:
            query += f"LIMIT {self.limit_value} "
        if self.offset_value is not None:
            query += f"OFFSET {self.offset_value} "
        return query

    def build_where_clause(self):
        return "WHERE " + ' AND '.join(self.where_clauses) + ' ' if self.where_clauses else ''

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        cursor.close()
        return [dict(zip(columns, row)) for row in results]

    def execute_scalar(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()[0]
        cursor.close()
        return result

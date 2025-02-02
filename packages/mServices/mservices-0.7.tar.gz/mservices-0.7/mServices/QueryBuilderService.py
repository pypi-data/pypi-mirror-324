from django.db.models import Q

class QueryBuilderService:
    def __init__(self, model):
        self.model = model
        self.select_fields = []
        self.joins = []
        self.conditions = []
        self.where_in_conditions = []
        self.order_by = []
        self.limit = None
        self.offset = None

    def select(self, *args):
        # Allow the use of table aliases in the select clause
        self.select_fields = args
        return self

    def left_join(self, table_name, related_column, parent_column):
        # Add a left join to the query, using the table names and column references
        self.joins.append({
            'type': 'LEFT JOIN',
            'table_name': table_name,
            'related_column': related_column,
            'parent_column': parent_column
        })
        return self

    def where(self, field, value):
        self.conditions.append((field, value))
        return self

    def where_in(self, field, values):
        self.where_in_conditions.append((field, values))
        return self

    def order_by(self, *fields):
        self.order_by = fields
        return self

    def paginate(self, limit, offset):
        self.limit = limit
        self.offset = offset
        return self

    def get(self):
        query = self.model.objects.all()

        # Apply joins (manually created left joins)
        for join in self.joins:
            if join['type'] == 'LEFT JOIN':
                table_name = join['table_name']
                related_column = join['related_column']
                parent_column = join['parent_column']

                # This would manually add the join for SQL syntax
                query = query.extra(select={f'{table_name}_{related_column}': f'{table_name}.{related_column}'})  # Add the join column

        # Apply filters (where conditions)
        for condition in self.conditions:
            field = condition[0]
            if '.' in field:  # Split for table.column format
                table, column = field.split('.')
                query = query.filter(**{f'{table}__{column}': condition[1]})
            else:
                query = query.filter(**{condition[0]: condition[1]})

        # Apply WHERE IN conditions
        for condition in self.where_in_conditions:
            query = query.filter(**{f'{condition[0]}__in': condition[1]})

        # Apply order by
        if self.order_by:
            query = query.order_by(*self.order_by)

        # Apply pagination (LIMIT and OFFSET)
        if self.limit:
            query = query[:self.limit]
        if self.offset:
            query = query[self.offset:]

        # Apply select fields (if any)
        if self.select_fields:
            query = query.values(*self.select_fields)

        return query

    def first(self):
        return self.get().first()
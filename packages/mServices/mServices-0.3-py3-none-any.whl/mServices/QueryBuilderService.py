from django.db import models

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

    # Select specific fields
    def select(self, *args):
        self.select_fields = args
        return self

    # Left Join with custom column mapping (mimicking Laravel's leftJoin(table, table.col, parentTable.col))
    def left_join(self, related_model, related_column, parent_column):
        self.joins.append({
            'type': 'LEFT JOIN',
            'model': related_model,
            'related_column': related_column,
            'parent_column': parent_column
        })
        return self

    # Where condition
    def where(self, field, value):
        self.conditions.append((field, value))
        return self

    # WhereIn condition (to match a field with a list of values)
    def where_in(self, field, values):
        self.where_in_conditions.append((field, values))
        return self

    # Order by condition (for sorting)
    def order_by(self, *fields):
        self.order_by = fields
        return self

    # Pagination (LIMIT and OFFSET)
    def paginate(self, limit, offset):
        self.limit = limit
        self.offset = offset
        return self

    # Execute the query and fetch the results
    def get(self):
        query = self.model.objects.all()

        # Apply joins (if any)
        for join in self.joins:
            query = query.prefetch_related(
                models.Prefetch(
                    join['model']._meta.model_name,
                    queryset=join['model'].objects.all(),
                    to_attr=join['model']._meta.model_name
                )
            )

        # Apply filters (where conditions)
        for condition in self.conditions:
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

    # Fetch the first result
    def first(self):
        return self.get().first()
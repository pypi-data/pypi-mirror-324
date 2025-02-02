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

    def left_join(self, related_model, related_column, parent_column):
        # Add a left join to the query
        self.joins.append({
            'type': 'LEFT JOIN',
            'model': related_model,
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

        # Apply joins (if any)
        for join in self.joins:
            if join['type'] == 'LEFT JOIN':
                related_model = join['model']
                related_column = join['related_column']
                parent_column = join['parent_column']
                
                # Handle related model joins
                query = query.select_related(related_model)  # Assuming ForeignKey, you could extend this for more complex joins

        # Apply filters (where conditions)
        for condition in self.conditions:
            field = condition[0]  # Get the field name
            if '.' in field:  # If the field is in the format 'table.field'
                table, column = field.split('.')
                query = query.filter(**{f'{column}': condition[1]})
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
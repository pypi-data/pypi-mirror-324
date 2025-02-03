import re
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db.models import Model

class ValidatorService:
    def __init__(self, data, rules, custom_messages=None):
        self.data = data
        self.rules = rules
        self.custom_messages = custom_messages or {}
        self.errors = {}

    def validate(self):
        for field, rule_string in self.rules.items():
            rules = rule_string.split('|')
            value = self.data.get(field)

            for rule in rules:
                rule_parts = rule.split(':')
                rule_name = rule_parts[0]
                rule_param = rule_parts[1] if len(rule_parts) > 1 else None

                # Check each rule
                validator = getattr(self, f'validate_{rule_name}', None)
                if validator:
                    validator(field, value, rule_param)
                else:
                    raise NotImplementedError(f"Rule '{rule_name}' is not implemented.")
                    
        if self.errors:
            raise ValidationError(self.errors)

    # Validation Methods
    def validate_required(self, field, value, _):
        if value is None or value == '':
            self.add_error(field, 'required', f"{field} is required.")

    def validate_email(self, field, value, _):
        if value and not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            self.add_error(field, 'email', f"{field} must be a valid email address.")

    def validate_min(self, field, value, param):
        if value and len(str(value)) < int(param):
            self.add_error(field, 'min', f"{field} must be at least {param} characters.")

    def validate_max(self, field, value, param):
        if value and len(str(value)) > int(param):
            self.add_error(field, 'max', f"{field} cannot exceed {param} characters.")

    def validate_same(self, field, value, param):
        if value != self.data.get(param):
            self.add_error(field, 'same', f"{field} must be the same as {param}.")

    def validate_required_if(self, field, value, param):
        other_field, expected_value = param.split(',')
        if self.data.get(other_field) == expected_value and not value:
            self.add_error(field, 'required_if', f"{field} is required when {other_field} is {expected_value}.")

    def validate_numeric(self, field, value, _):
        if value and not str(value).isdigit():
            self.add_error(field, 'numeric', f"{field} must be a number.")

    def validate_regex(self, field, value, param):
        if value and not re.match(param, value):
            self.add_error(field, 'regex', f"{field} format is invalid.")

    def validate_unique(self, field, value, param):
        model_name, field_name = param.split(',')
        model_class = globals().get(model_name)
        if model_class and issubclass(model_class, Model):
            if model_class.objects.filter(**{field_name: value}).exists():
                self.add_error(field, 'unique', f"{field} must be unique.")

    def validate_date(self, field, value, _):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except (ValueError, TypeError):
            self.add_error(field, 'date', f"{field} must be a valid date (YYYY-MM-DD).")

    def validate_between(self, field, value, param):
        min_val, max_val = map(int, param.split(','))
        if value and not (min_val <= int(value) <= max_val):
            self.add_error(field, 'between', f"{field} must be between {min_val} and {max_val}.")

    def add_error(self, field, rule, default_message):
        key = f"{field}.{rule}"
        message = self.custom_messages.get(key, default_message)
        self.errors.setdefault(field, []).append(message)

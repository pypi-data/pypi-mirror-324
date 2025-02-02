# validator_service/validator.py

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from datetime import datetime, date

class ValidatorService:
    @staticmethod
    def validate(request, rules, custom_messages=None):
        errors = {}
        data = request.POST if request.method == 'POST' else request.GET

        for field, rule in rules.items():
            value = data.get(field)
            rules_list = rule.split('|')

            for r in rules_list:
                if r == 'required':
                    if not value:
                        errors[field] = custom_messages.get(f'{field}.required', _('This field is required.'))
                elif r.startswith('min:'):
                    min_value = int(r.split(':')[1])
                    if value and len(value) < min_value:
                        errors[field] = custom_messages.get(f'{field}.min', _(f'This field must be at least {min_value} characters long.'))
                elif r.startswith('max:'):
                    max_value = int(r.split(':')[1])
                    if value and len(value) > max_value:
                        errors[field] = custom_messages.get(f'{field}.max', _(f'This field must be no more than {max_value} characters long.'))
                elif r == 'email':
                    try:
                        validate_email(value)
                    except ValidationError:
                        errors[field] = custom_messages.get(f'{field}.email', _('Enter a valid email address.'))
                elif r.startswith('unique:'):
                    model, column = r.split(':')[1].split(',')
                    model_class = ValidatorService.get_model_class(model)
                    if model_class.objects.filter(**{column: value}).exists():
                        errors[field] = custom_messages.get(f'{field}.unique', _(f'This {field} is already taken.'))
                elif r.startswith('same:'):
                    other_field = r.split(':')[1]
                    if value != data.get(other_field):
                        errors[field] = custom_messages.get(f'{field}.same', _(f'This field must match the {other_field} field.'))
                elif r == 'date':
                    try:
                        datetime.strptime(value, '%Y-%m-%d')
                    except ValueError:
                        errors[field] = custom_messages.get(f'{field}.date', _('Enter a valid date.'))
                elif r == 'today':
                    try:
                        input_date = datetime.strptime(value, '%Y-%m-%d').date()
                        if input_date != date.today():
                            errors[field] = custom_messages.get(f'{field}.today', _('The date must be today.'))
                    except ValueError:
                        errors[field] = custom_messages.get(f'{field}.today', _('Enter a valid date.'))
                elif r.startswith('after:'):
                    try:
                        input_date = datetime.strptime(value, '%Y-%m-%d').date()
                        after_date = datetime.strptime(data.get(r.split(':')[1]), '%Y-%m-%d').date()
                        if input_date <= after_date:
                            errors[field] = custom_messages.get(f'{field}.after', _(f'This field must be after {r.split(":")[1]}.'))
                    except (ValueError, TypeError):
                        errors[field] = custom_messages.get(f'{field}.after', _('Enter a valid date.'))
                elif r.startswith('required_if:'):
                    other_field, other_value = r.split(':')[1].split(',')
                    if data.get(other_field) == other_value and not value:
                        errors[field] = custom_messages.get(f'{field}.required_if', _(f'This field is required when {other_field} is {other_value}.'))

        if errors:
            return errors
        return None

    @staticmethod
    def get_model_class(model_name):
        from django.apps import apps
        return apps.get_model(model_name)
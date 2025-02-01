from typing import Any
from django.db.models import ManyToManyField, OneToOneField
from django.db.models.fields.json import JSONField
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.forms.fields import DateTimeField

EXCLUDE = {
    '__fallback__': {"BinaryField", "GeneratedField", "JSONField"}
}

# we do filter mainly becase django-listpy-filter-ui front end currently doesn't
# implement them (such as `in`, `range`)
def default_lookup_filter(_field: type, field_name: str):
    """
    For custom lookup filter function:
    
    You can use `list(field.get_lookups().keys())` to get all lookups associated with
    that field.
    """
    BasicLookups = [
        "exact", "isnull",
        
    ]

    if field_name in {
        "AutoField", "BigAutoField", "BigIntegerField", "SmallAutoField", "SmallIntegerField",
        "DecimalField", "DurationField", "FloatField", "IntegerField",
        "PositiveBigIntegerField", "PositiveIntegerField", "PositiveSmallIntegerField",
        "URLField", "UUIDField",
    }:
        return BasicLookups + [
            "gt", "gte", "lt", "lte",
        ]
    elif field_name == "BooleanField":
        return BasicLookups
    elif field_name in {
        "CharField", "EmailField", "EmailField", "FileField",
        "FilePathField", "GenericIPAddressField", "ImageField",
        "SlugField", "TextField", 
    }:
        return BasicLookups + [
            "iexact", "contains", "icontains",
            "startswith", "istartswith", "endswith", "iendswith",
            "regex", "iregex",
        ]
    elif field_name in ("DateField", "DateTimeField", "TimeField", ):
        return BasicLookups + [
            "gt", "gte", "lt", "lte",
        ]
    
    return BasicLookups

    
def get_model_schema(
    model_class: type,
    excludes: set[str] = set(),
    lookup_filter_fn = default_lookup_filter,
):
    schema: dict[str, Any] = {
        '__rel': [],
        '__verbose_name': model_class._meta.verbose_name,
    }

    lookups: dict[str, list[str]] = {}
    
    for field in model_class._meta.get_fields():
        if field.name in excludes:
            continue
        
        if isinstance(field, (
            ForeignObjectRel, # reverse relationship
            ForeignKey, ManyToManyField, OneToOneField,
        )):
            schema['__rel'].append(field.name)
            continue

        field_class_name = type(field).__name__
        
        # don't use verbose_name as key, since we may assign a gettext_lazy as
        # verbvose_name value
        schema[field.name] = {
            'verbose_name': field.verbose_name,
            'class': field_class_name,
            'choices': dict(field.get_choices()) if field.choices else None,
        }

        if field_class_name not in lookups:
            lookups[field_class_name] = lookup_filter_fn(field, field_class_name)

    return schema, lookups

        

def get_models_schema(
    model_classes: list[type],
    excludes: dict[str, set[str]] = EXCLUDE,
    lookup_filter_fn = default_lookup_filter,
):
    schema_models: dict[str, Any] = {}
    schema_lookups: dict[str, Any] = {}
    
    for model_class in model_classes:
        model_schema, model_lookups = get_model_schema(
            model_class,
            excludes.get(model_class.__name__, excludes.get("__fallback__", set())),
            lookup_filter_fn
        )
        schema_models[model_class.__name__.lower()] = model_schema
        for key, value in model_lookups.items():
            if key not in schema_lookups:
                schema_lookups[key] = value
                
    return {
        'models': schema_models,
        'lookups': schema_lookups
    }

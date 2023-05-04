from django.contrib.contenttypes.models import ContentType


def get_polymorphic_base_content_type(obj):
    """
    Helper function to return the base polymorphic content type id. This should used with django-guardian and the
    GUARDIAN_GET_CONTENT_TYPE option.

    See the django-guardian documentation for more information:

    https://django-guardian.readthedocs.io/en/latest/configuration.html#guardian-get-content-type
    """
    if not hasattr(obj, "polymorphic_model_marker"):
        return ContentType.objects.get_for_model(obj)

    try:
        superclasses = list(obj.__class__.mro())
    except TypeError:
        # obj is an object so mro() need to be called with the obj.
        superclasses = list(obj.__class__.mro(obj))

    polymorphic_superclasses = [
        sclass
        for sclass in superclasses
        if hasattr(sclass, "polymorphic_model_marker")
    ]
        # PolymorphicMPTT adds an additional class between polymorphic and base class.
    root_polymorphic_class = (
        polymorphic_superclasses[-3]
        if hasattr(obj, "can_have_children")
        else polymorphic_superclasses[-2]
    )
    return ContentType.objects.get_for_model(root_polymorphic_class)

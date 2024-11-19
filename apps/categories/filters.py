from django.contrib.admin import SimpleListFilter

class CategoryFilter(SimpleListFilter):
    """
    Custom filter to categorize categories based on their parent-child relationship.

    This filter allows filtering of categories by their degree, i.e.,
    whether they are main categories (parent is null) or lower categories
    (parent is not null).
    """
    title = 'Category Degree'  # Title for the filter in the admin interface
    parameter_name = 'category'  # The name of the parameter used in the URL

    def lookups(self, request, model_admin):
        """
        Provides the options for the filter dropdown in the admin interface.

        Args:
            request (HttpRequest): The incoming request object.
            model_admin (ModelAdmin): The model admin class handling the queryset.

        Returns:
            list: A list of tuples representing the filter options.
        """
        return [
            ('main_cat', 'Main category'),
            ('low_cat', 'Lower category'),
        ]

    def queryset(self, request, queryset):
        """
        Filters the queryset based on the selected filter value.

        Args:
            request (HttpRequest): The incoming request object.
            queryset (QuerySet): The initial queryset to filter.

        Returns:
            QuerySet: The filtered queryset based on the selected category degree.
        """
        match self.value():
            case 'main_cat':
                return queryset.filter(parent__isnull=True)
            case 'low_cat':
                return queryset.filter(parent__isnull=False)
        return queryset

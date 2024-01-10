from django.contrib import admin

# Register your models here.
from sunat.models import RUC, DNI


class GeneralAdmin(admin.ModelAdmin):

    def get_model_fields(self, model):
        fields = model._meta.fields
        many_to_many_fields = model._meta.many_to_many

        return [field.name for field in fields if not field.primary_key] + [field.name for field in many_to_many_fields]

    def get_all_model_fields(self, model):
        fields = model._meta.fields
        many_to_many_fields = model._meta.many_to_many

        return [field.name for field in fields] + [field.name for field in many_to_many_fields]

        return [field.name for field in model._meta.fields]

    def get_list_display(self, request):
        model = self.model
        fields = self.get_all_model_fields(model)
        return fields

    def get_fields(self, request, obj=None):
        model = self.model
        fields = self.get_model_fields(model)
        return fields

    def get_fieldsets(self, request, obj=None):
        model = self.model
        fields = self.get_model_fields(model)
        return [(None, {'fields': fields})]

    def get_search_fields(self, request):
        model = self.model
        fields = self.get_model_fields(model)
        return fields

    def get_list_filter(self, request):
        model = self.model
        fields = self.get_model_fields(model)
        return fields


admin.site.register(RUC, GeneralAdmin)
admin.site.register(DNI, GeneralAdmin)

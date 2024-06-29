from django.contrib import admin
from .models import Churches, People, Ministries, Positions, Membership

@admin.register(Churches)
class ChurchesAdmin(admin.ModelAdmin):
    list_display = ('name', 'acronym', 'address', 'phone', 'cnpj')
    search_fields = ('name', 'acronym', 'address', 'phone', 'cnpj')

@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviated_name', 'phone', 'date_of_birth', 'is_member', 'status', 'church')
    list_filter = ('status', 'is_member', 'church')
    search_fields = ('name', 'abbreviated_name', 'phone', 'church__name')

@admin.register(Ministries)
class MinistriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'acronym', 'church')
    list_filter = ('church',)
    search_fields = ('name', 'acronym', 'church__name')

@admin.register(Positions)
class PositionsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('person', 'ministry', 'position')
    list_filter = ('ministry', 'position')
    search_fields = ('person__name', 'ministry__name', 'position__name')

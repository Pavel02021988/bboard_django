from django.contrib import admin
import datetime
from .models import AdvUser, SuperRubric, SubRubric, Bb, AdditionalImage
from .models import Comment
from .utilities import send_activation_notification
from .forms import SubRubricForm

# функция для рассылки писем с просьбой выполнить активацию
def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма с оповещениями отправлены')
send_activation_notifications.short_description = 'Отправка писем с оповещениями об активации'

# фильтрация пользователей выполнивших активацию и не выполнивших ее в течении 3 дней и недели
class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'actstate'
    
    def lookups(self, request, model_admin):
        return (
                   ('activated', 'Прошли'),
                   ('threedays', 'Не прошли более 3 дней'),
                   ('week', 'Не прошли более недели'),
               )
    
    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)

# класс редактора
class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (('username', 'email'), ('first_name', 'last_name'),
              ('send_messages', 'is_active', 'is_activated'), ('is_staff', 'is_superuser'),
              'groups', 'user_permissions', ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)

# регистрация моделей
admin.site.register(AdvUser, AdvUserAdmin)

# редактор подрубрик
class SubRubricInline(admin.TabularInline):
    model = SubRubric

# редактор надрубрик
class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)

# регистрация моделей
admin.site.register(SuperRubric, SuperRubricAdmin)

class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm

# регистрация моделей
admin.site.register(SubRubric, SubRubricAdmin)

# встроенный редактор для работы с дополнительными иллюстрациями
class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage

# редактор для работы с объявлениями
class BbAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'title', 'content', 'author', 'created_at')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content', 'author')
    date_hierarchy = 'created_at'
    fields = (('rubric', 'author'), 'title', 'content', 'price', 'contacts', 'image', 'is_active')
    inlines = (AdditionalImageInline,)

# регистрация моделей
admin.site.register(Bb, BbAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at', 'is_active')
    list_display_links = ('author', 'content')
    list_filter = ('is_active',)
    search_fields = ('author', 'content',)
    date_hierarchy = 'created_at'
    fields = ('author', 'content', 'is_active', 'created_at')
    readonly_fields = ('created_at',)

# регистрация моделей
admin.site.register(Comment, CommentAdmin)

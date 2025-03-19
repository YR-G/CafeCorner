from django.contrib import admin
from users.models import Administrator  # 确保导入你的 Administrator 模型

@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')  # 可在 Admin 界面显示的字段
    search_fields = ('email', 'first_name', 'last_name')  # 允许搜索

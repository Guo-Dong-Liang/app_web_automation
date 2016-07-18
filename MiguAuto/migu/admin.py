# coding=utf-8
from django.contrib import admin
from migu.models import script, task, task_type, task_status, task_record, script_test


# from migu.models import AutoUser

# Register your models here.
class tasktypeInline(admin.TabularInline):
	model = task_type


def makeCando(self, request, queryset):
	rowsUpdated = queryset.update(task_status=1)
	if rowsUpdated == 1:
		self.message_user(request, u'执行成功')
	else:
		self.message_user(request, u'执行失败')
makeCando.short_description = u'重置任务为可执行'


class scriptAdmin(admin.ModelAdmin):
	fields = ['script_name', 'script_path', 'script_appiumport', 'script_udid', 'script_description']
	list_display = (
		'script_name', 'script_path', 'script_appiumport', 'script_udid', 'script_description', 'script_createtime')
	list_display_links = ('script_name',)
	# list_editable=('scriptpath',)
	search_fields = ['script_name']


class script_testAdmin(admin.ModelAdmin):
	list_display = ('script_test_scriptid', 'script_test_name', 'script_test_description', 'script_test_createtime')
	search_fields = ['script_test_name']


class taskAdmin(admin.ModelAdmin):
	fields = ['task_name', 'task_description', 'task_script_id', 'task_status', 'task_type']
	list_display = ('task_name', 'task_description', 'task_status', 'task_createtime')
	list_display_links = ('task_name',)
	list_filter = ['task_type', 'task_status']
	# list_editable=('scriptpath',)
	search_fields = ['task_name']
	actions = [makeCando]


class task_recordAdmin(admin.ModelAdmin):
	list_display = ('task_record_task_id', 'task_record_user_id', 'task_record_status', 'task_record_result_path',
	                'task_record_createtime')
	list_display_links = ('task_record_task_id',)
	list_filter = ['task_record_task_id', 'task_record_user_id']
	# list_editable=('scriptpath',)
	# search_fields = ['task__task_name']


admin.site.register(script_test, script_testAdmin)
admin.site.register([task_status, task_type])
admin.site.register(script, scriptAdmin)
admin.site.register(task, taskAdmin)
admin.site.register(task_record, task_recordAdmin)

# 路由文件

from apps.admin.auth.login_views import app as auth_app
from apps.admin.auth.admin_views import app as admin_auth_app
from apps.admin.system.admin_views import app as admin_system_app
from apps.admin.record.admin_views import app as admin_record_app
from apps.admin.workplace.admin_views import app as admin_workplace_app
from apps.admin.analysis.admin_views import app as admin_analysis_app
from apps.admin.help.admin_views import app as admin_help_app
from apps.admin.resource.admin_views import app as admin_resource_app

# 引入应用中的路由
urlpatterns = [
    {"ApiRouter": auth_app, "prefix": "/auth", "tags": ["系统认证"]},
    {"ApiRouter": admin_auth_app, "prefix": "/admin/auth", "tags": ["权限管理"]},
    {"ApiRouter": admin_system_app, "prefix": "/admin/system", "tags": ["系统管理"]},
    {"ApiRouter": admin_record_app, "prefix": "/admin/record", "tags": ["记录管理"]},
    {"ApiRouter": admin_workplace_app, "prefix": "/admin/workplace", "tags": ["工作区管理"]},
    {"ApiRouter": admin_analysis_app, "prefix": "/admin/analysis", "tags": ["数据分析管理"]},
    {"ApiRouter": admin_help_app, "prefix": "/admin/help", "tags": ["帮助中心管理"]},
    {"ApiRouter": admin_resource_app, "prefix": "/admin/resource", "tags": ["资源管理"]},
]

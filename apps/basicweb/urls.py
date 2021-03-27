from django.urls import path
# 引入当前app的views
from basicweb.views import faculty, major

# ==== 匹配当前app中的url ====
urlpatterns = [
    # ====院系管理====
    path('faculty', faculty.index, name='faculty'),
    path('faculty/list/', faculty.list_values, name='list_faculty'),  # 获取院系
    path('faculty/add/', faculty.add_value, name='add_faculty'),  # 添加院系
    path('faculty/edit/', faculty.edit_value, name='edit_faculty'),  # 修改院系
    path('faculty/del/', faculty.del_value, name='del_faculty'),  # 删除院系

    # ====专业管理====
    path('major', major.index, name='major'),
    path('major/list/', major.list_values, name='list_major'),  # 获取专业
    path('major/add/', major.add_value, name='add_major'),  # 添加专业
    path('major/edit/', major.edit_value, name='edit_major'),  # 编辑专业
    path('major/del/', major.del_value, name='del_major'),  # 删除专业
    path('major/query/', major.query_value, name='query_major'),  # 根据院系查专业
]

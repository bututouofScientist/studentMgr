# 引入模块
from django.shortcuts import render
# 引入models的类
from basicweb.models import Major, Faculty
from django.http import JsonResponse
from django.db.models import Q


def index(requests):
    return render(requests, 'basic/major.html')


def list_values(requests):
    """获取专业数据"""
    # 获取传递过来的两个参数
    page = int(requests.POST.get('page', 0))
    limit = int(requests.POST.get('limit', 0))
    q_str = requests.POST.get('inputStr', "")
    # 获取所有数据
    objs = list(Major.objects.filter(Q(name__icontains=q_str) | Q(faculty__name__icontains=q_str)).values('id', 'name', 'faculty__name','faculty_id'))
    # 获取当前页的数据
    objs_one_page = objs[(page - 1) * limit: page * limit]
    # 定义一个返回值类型: code 状态 count：总数 用于分页 data：返回的数据
    res = {"code": "0", 'count': len(objs), "data": objs_one_page}
    return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})


def add_value(requests):
    """添加专业"""
    # 获取前台传递过来的值
    faculty = requests.POST.get('faculty')
    major = requests.POST.get('major')
    # 操作数据库
    try:
        Major.objects.create(faculty_id=faculty, name=major)
        return JsonResponse({'status': True})
    except Exception as e:
        return JsonResponse({'status': False, 'error':  "添加专业数据异常，具体原因" + str(e)})


def edit_value(requests):
    """修改"""
    # 获取传递过来的值
    rec = requests.POST
    # 获取当前操作对象
    try:
        obj = Major.objects.filter(id=rec.get('major_id')).first()
        # 修改专业
        obj.name = rec.get('major')
        # 修改院系
        obj.faculty = Faculty.objects.filter(id=rec.get('faculty')).first()
        # 保存
        obj.save()
        # 返回
        return JsonResponse({'status': True})
    except Exception as e:
        return JsonResponse({'status': False, 'error': "修改数据异常，具体原因" + str(e)})


def del_value(requests):
    """删除"""
    # 接收传过来的ID
    id = requests.POST.get("id")
    # 到数据库删除
    try:
        Major.objects.filter(id=id).first().delete()
        return JsonResponse({'status': True})
    except Exception as e:
        return JsonResponse({'status': False, 'error': "删除数据异常，具体原因" + str(e)})


def query_value(request):
    """通过院系查专业"""
    # 获取传过来的院系ID
    q_id = request.POST.get("id")
    try:
        # 根据院系ID获取专业数据
        objs = list(Major.objects.filter(faculty_id=q_id).values("id", "name"))
        return JsonResponse({'status': True, 'data': objs})
    except Exception as e:
        return JsonResponse({'status': False, 'error': "获取专业数据出现异常，具体原因：" + str(e)})

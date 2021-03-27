# 引入模块
from django.shortcuts import render
# 引用数据库通用类
from apps.utils import sqlhelper
from basicweb.models import Faculty
from django.http import JsonResponse


def index(requests):
    return render(requests, 'basic/faculty.html')


def list_values(request):
    """ 获取院系数据"""
    # 接受查询的条件
    q_str = request.POST.get('queryStr', "")
    # 准备SQL语句
    sql = """
        Select T3.Id,T3.Name, Count(T3.id2) As 'Number' 
        From 
        (
            Select T1.Id, T1.Name, T2.Id As "id2"
            from Basicweb_faculty As T1
            Left Join Basicweb_major As T2 On T1.id = T2.faculty_id
    			  where T1.Name Like '%s'
        ) AS T3
        Group By T3.Id,T3.Name
        """ % ('%' + q_str + '%')
    # 开始执行sql语句
    response = sqlhelper.get_db_data_dict(sql, ['id', 'name', 'number'])
    if response['status']:
        return JsonResponse({'status': True, 'data': response['data']})
    else:
        return JsonResponse({'status': True, 'error': response['error']})


def add_value(requests):
    """添加"""
    # 接受传递过来的名称
    name = requests.POST.get('name')
    # 写入数据库
    try:
        Faculty.objects.create(name = name)
        return JsonResponse({'status': True})
    except Exception as e:
        return JsonResponse({'status': False, 'error': "写入数据库出现异常，具体原因：" + str(e)})


def edit_value(requests):
    """修改"""
    # 获取传递过来的数据
    id = requests.POST.get('id', '')
    name = requests.POST.get('name', '')
    # 到数据库修改数据
    try:
        obj = Faculty.objects.get(id=id)
        obj.name = name
        obj.save()
        return JsonResponse({'status': True})
    except Exception as e:
        return JsonResponse({'status': False, 'error': '修改提交到数据库出现异常，具体原因：' + str(e)})


def del_value(requests):
    """删除"""
    # 获取Id
    id = requests.POST.get('id')
    # 到数据库中删除数据
    try:
        Faculty.objects.get(id=id).delete()
        return JsonResponse({'status': True})
    except Exception as e:
        return JsonResponse({'status': False, 'error':  "删除异常！具体原因" + str(e)})


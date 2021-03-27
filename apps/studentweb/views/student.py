from django.shortcuts import render
from studentweb.models import Student
from basicweb.models import Faculty, Major
from django.http import JsonResponse
from django.db.models import Q
# Create your views here.


def index(request):
    return render(request, 'student/student.html')


def list_values(request):
    """展示数据"""
    # 接受page和limit参数
    page = int(request.POST.get("page", 0))
    limit = int(request.POST.get("limit", 0))
    # 查询的条件获取
    q_sno_name = request.POST.get('q_sno_name')  # 模糊查询学号 or 模糊查询姓名
    q_faculty = request.POST.get('q_faculty')  # 匹配院系信息
    q_major = request.POST.get('q_major')  # 匹配专业信息
    q_status = request.POST.get('q_status')  # 匹配学生状态

    # 第一次过滤： --模糊学号查询 or 模糊姓名查询
    filter_data = Student.objects.filter(Q(sno__icontains=q_sno_name) | Q(name__icontains=q_sno_name))
    # 第二次过滤： --查询院系
    if len(q_faculty) > 0:
        filter_data = filter_data.filter(faculty_id=q_faculty)
    # 第三次过滤： --查询专业
    if len(q_major) > 0:
        filter_data = filter_data.filter(major_id=q_major)
    # 第四次过滤： --查询学生状态
    if q_status == "true":
        filter_data = filter_data.filter(status="在校")
    # 处理数据
    objs = list(filter_data.values('sno', 'name', 'gender', 'birthday', 'mobile', 'email', 'address',
                                         'major', 'faculty', 'major__name', 'faculty__name', 'start_date', 'status'))
    # 构建返回的数据
    res = {"code": 0, "count": len(objs), "data": objs}
    if page != 0 and limit != 0:
        one_page_objs = objs[(page - 1) * limit:page * limit]  # 单页数据对象
        res["data"] = one_page_objs
    return JsonResponse(res)


def is_sno_exists(request):
    """校验学号是否存在"""
    # 获取学号
    sno = request.POST.get("sno")
    # 判断
    is_exist = Student.objects.filter(sno=sno).exists()
    # 返回
    return JsonResponse({"data":is_exist})


def add_values(request):
    """完成学生信息的添加"""
    # 接收传递的值
    rec = request.POST
    # 添加操作
    try:
        Student.objects.create(sno=rec['sno'], name=rec["name"], gender=rec["gender"], birthday=rec['birthday'],
                               mobile=rec['mobile'], email=rec['email'], address=rec['address'],
                               faculty=Faculty.objects.get(id=rec["faculty"]),
                               major=Major.objects.get(id=rec["major"]),
                               start_date=rec['start_date'], status=rec['status']
                               )
        return JsonResponse({"status": True})
    except Exception as e:
        return JsonResponse({"status": False, "error": "添加学生提交到数据库异常，具体原因" + str(e)})


def edit_values(request):
    """完成学生信息的修改"""
    # 接收传递的值
    rec = request.POST
    try:
        # 获取当前的对象
        obj = Student.objects.get(sno=rec["sno"])
        # 逐一修改属性
        obj.name = rec['name']
        obj.gender = rec['gender']
        obj.birthday = rec['birthday']
        obj.mobile = rec['mobile']
        obj.email = rec['email']
        obj.address = rec['address']
        obj.faculty = Faculty.objects.get(id=rec['faculty'])
        obj.major = Major.objects.get(id=rec['major'])
        obj.start_date = rec['start_date']
        obj.status = rec['status']
        # 保存
        obj.save()
        return JsonResponse({"status": True})
    except Exception as e:
        return JsonResponse({"status": False, "error": "修改学生提交到数据库异常，具体原因" + str(e)})


def del_values(request):
    """完成学生信息的删除"""
    # 接收传递的值
    sno = request.POST.get("sno")
    try:
        # 获取当前的对象并删除
        Student.objects.get(sno=sno).delete()
        return JsonResponse({"status": True})
    except Exception as e:
        return JsonResponse({"status": False, "error": "删除学生提交到数据库异常，具体原因" + str(e)})

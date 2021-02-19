from django.shortcuts import render,redirect
from pss_homepage.models import *
from tools.common import my_login_required
from tools.forms import FileUploadFormSourceData,FormToolBorrowInfo,FormToolReturnInfo,FormEmployeeInfo
from django.db import transaction
from django.utils import timezone
import xlrd

# Create your views here.

#管理员页面
@my_login_required
def manager_views(request,user):
      
    return render(request,'manager.html',locals())

@my_login_required
def tool_borrow_views(request,user):

    #如果是post提交
    if request.method == "POST":
        print("post request")
        myform = FormToolBorrowInfo(request.POST)

        if myform.is_valid():
            #获取前端传过来的文件信息
            tool_encoding = request.POST.get('tool_encoding', '')
            employee_number = request.POST.get('employee_number', '')
            
            print('tool_encoding = ',tool_encoding)
            print('employee_number = ',employee_number)

            try:
                with transaction.atomic():
                    #获取工具信息
                    #toolinfo = ToolInfo.objects.get(tool_encoding=tool_encoding)
                    toolinfo = ToolInfo.objects.filter(tool_encoding=tool_encoding)
                    if not toolinfo.exists():
                        error_info = '该工具信息不存在!'
                        form = FormToolBorrowInfo()
                        what = "工具借出"
                        return render(request,'tool-borrow.html',locals())
                    
                    #检查该工具状态是否正常
                    #ToolState.objects.get(tool_state_number=toolinfo[0].tool_state).tool_state_name == '借出'
                    toolinfo = ToolInfo.objects.get(tool_encoding=tool_encoding)
                    if toolinfo.tool_state.tool_state_name == '借出':
                        error_info = '该工具已经借出,无法重复借出!'
                        form = FormToolBorrowInfo()
                        what = "工具借出"
                        return render(request,'tool-borrow.html',locals())

                    #ToolDamageExtent.objects.get(tool_damage_extent_number=toolinfo[0].tool_damage_extent).tool_damage_extent_name == '损坏'
                    if toolinfo.tool_damage_extent.tool_damage_extent_name == '损坏':
                        error_info = '该工具损坏程度为损坏,无法使用!'
                        form = FormToolBorrowInfo()
                        what = "工具借出"
                        return render(request,'tool-borrow.html',locals())

                    if toolinfo.tool_damage_extent.tool_damage_extent_name == '报废':
                        error_info = '该工具损坏程度为报废,无法使用!'
                        form = FormToolBorrowInfo()
                        what = "工具借出"
                        return render(request,'tool-borrow.html',locals())

                    #检查该员工是否存着,员工状态是否正常
                    #employee = Employee.objects.get(employee_number=employee_number)
                    employee = Employee.objects.filter(employee_number=employee_number)
                    if not employee.exists():
                        error_info = '该员工信息不存在!'
                        form = FormToolBorrowInfo()
                        what = "工具借出"
                        return render(request,'tool-borrow.html',locals())

                    #一切正常,先更新工具状态
                    toolinfo.tool_state = ToolState.objects.get(tool_state_name='借出')
                    toolinfo.tool_borrow_employee = Employee.objects.get(employee_number=employee_number)
                    toolinfo.save()
                    #然后记录借出的信息
                    toolborrowreturnrecord = ToolBorrowReturnRecord()
                    toolborrowreturnrecord.toolinfo = ToolInfo.objects.get(tool_encoding=tool_encoding)
                    toolborrowreturnrecord.employee = Employee.objects.get(employee_number=employee_number)
                    toolborrowreturnrecord.createdate = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
                    toolborrowreturnrecord.tool_state = ToolState.objects.get(tool_state_name='借出')
                    toolborrowreturnrecord.tool_damage_extent = ToolDamageExtent.objects.get(tool_damage_extent_name='正常')
                    toolborrowreturnrecord.save()

                    return render(request, "manager-success.html", locals())

            except Exception as err:
                #print(type(err))
                print('错误信息是: ',err)
                error_info = '工具借出失败! 错误信息是: '+str(err)
                form = FormToolBorrowInfo()
                what = "工具借出"

        else:
            error_info = '工具借出失败!'
            form = FormToolBorrowInfo()
            what = "工具借出"

    else:
        print("get request")
        #context = {'form': myform, 'what': "借出工具"}
        form = FormToolBorrowInfo()
        what = "工具借出"

    return render(request,'tool-borrow.html',locals())

@my_login_required
def tool_return_views(request,user):

    #如果是post提交
    if request.method == "POST":
        print("post request")
        myform = FormToolReturnInfo(request.POST)

        if myform.is_valid():
            #获取前端传过来的文件信息
            tool_encoding = request.POST.get('tool_encoding', '')
            employee_number = request.POST.get('employee_number', '')
            tool_damage_extent = request.POST.get('tool_damage_extent', '')
            
            print('tool_encoding = ',tool_encoding)
            print('employee_number = ',employee_number)
            print('tool_damage_extent = ',tool_damage_extent)

            try:
                with transaction.atomic():
                    #获取工具信息
                    #toolinfo = ToolInfo.objects.get(tool_encoding=tool_encoding)
                    toolinfo = ToolInfo.objects.filter(tool_encoding=tool_encoding)
                    if not toolinfo.exists():
                        error_info = '该工具信息不存在!'
                        form = FormToolReturnInfo()
                        what = "工具归还"
                        return render(request,'tool-return.html',locals())
                    
                    #检查该工具状态是否正常
                    toolinfo = ToolInfo.objects.get(tool_encoding=tool_encoding)
                    if toolinfo.tool_state.tool_state_name != '借出':
                        error_info = '该工具还未借出过,无法归还!'
                        form = FormToolReturnInfo()
                        what = "工具归还"
                        return render(request,'tool-return.html',locals())
                    
                    #检查该员工是否存着,员工状态是否正常
                    #employee = Employee.objects.get(employee_number=employee_number)
                    employee = Employee.objects.filter(employee_number=employee_number)
                    if not employee.exists():
                        error_info = '该员工信息不存在!'
                        form = FormToolReturnInfo()
                        what = "工具归还"
                        return render(request,'tool-return.html',locals())

                    #检查是否是该员工借用的工具
                    #record_employee_number = Employee.objects.get(id=toolinfo[0].tool_borrow_employee).employee_number
                    record_employee_number = toolinfo.tool_borrow_employee.employee_number

                    if employee_number != record_employee_number:
                        error_info = '该工具不是该员工借用的,无法归还!'
                        form = FormToolReturnInfo()
                        what = "工具归还"
                        return render(request,'tool-return.html',locals())

                    #一切正常,先更新工具状态,如果工具损坏或者报废要更新
                    toolinfo.tool_state = ToolState.objects.get(tool_state_name='归还')
                    if tool_damage_extent == 'TDE2' or tool_damage_extent == 'TDE3':
                        toolinfo.tool_damage_extent = ToolDamageExtent.objects.get(tool_damage_extent_number=tool_damage_extent)
                    toolinfo.save()

                    #然后记录借出的信息
                    toolborrowreturnrecord = ToolBorrowReturnRecord()
                    toolborrowreturnrecord.toolinfo = ToolInfo.objects.get(tool_encoding=tool_encoding)
                    toolborrowreturnrecord.employee = Employee.objects.get(employee_number=employee_number)
                    toolborrowreturnrecord.createdate = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
                    toolborrowreturnrecord.tool_state = ToolState.objects.get(tool_state_name='归还')
                    toolborrowreturnrecord.tool_damage_extent = ToolDamageExtent.objects.get(tool_damage_extent_number=tool_damage_extent)
                    toolborrowreturnrecord.save()

                    return render(request, "manager-success.html", locals())

            except Exception as err:
                #print(type(err))
                print('错误信息是: ',err)
                error_info = '工具归还失败! 错误信息是: '+str(err)
                form = FormToolReturnInfo()
                what = "工具归还"

        else:
            error_info = '工具归还失败!'
            form = FormToolReturnInfo()
            what = "工具归还"

    else:
        print("get request")
        #myform = FormToolReturnInfo()
        #context = {'form': myform, 'what': "工具归还"}
        #form = myform
        form = FormToolReturnInfo()
        what = "工具归还"

    return render(request,'tool-return.html',locals())

@my_login_required
def manager_tool_data_upload_views(request,user):
    '''
    :param request:
    :return: 上传文件excel表格 ,并进行解析
    '''
    if request.method == "POST":
        print("post request")
        myform = FileUploadFormSourceData(request.POST, request.FILES)
        
        #print("myform = ",myform)
        
        #在这里可以添加筛选excel的机制
        if myform.is_valid():
            #获取前端传过来的文件信息
            file_name = request.POST.get('file_name', '')
            file_describe = request.POST.get('file_describe', '')
            file_additional_info = request.POST.get('file_additional_info', '')
            f = request.FILES['my_file']
            
            print('file_name = ',file_name)
            print('file_describe = ',file_describe)
            print('file_additional_info = ',file_additional_info)
            print('f = ',f)
            
            try:
                with transaction.atomic():
                    #创建一条工具记录,如果后面的数据有错误,事务会回滚
                    tooldatauploadinfo = ToolDataUploadInfo()
                    tooldatauploadinfo.tool_file_name = file_name
                    tooldatauploadinfo.tool_file_describe = file_describe
                    tooldatauploadinfo.tool_file_additional_info = file_additional_info
                    tooldatauploadinfo.save()
                    #开始解析上传的excel表格
                    wb = xlrd.open_workbook(filename=None, file_contents=f.read())  #关键点在于这里
                    #打开第一张表
                    table = wb.sheets()[0]
                    nrows = table.nrows  #行数
                    ncole = table.ncols  #列数
                    print("row:%s, cole:%s" % (nrows, ncole))
                    print('tooldatauploadinfo_foreignkey = ',tooldatauploadinfo.id)
                    
                    for i in range(1, nrows):
                        toolinfo = ToolInfo()
                        rowValues = table.row_values(i)  #一行的数据
                        
                        #print('tool_name = ',rowValues[0])
                        #print('tool_type = ',rowValues[1])
                        #print('tool_encoding = ',rowValues[2])
                        
                        toolinfo.tool_name = rowValues[0]
                        toolinfo.tool_type = rowValues[1]
                        toolinfo.tool_encoding = rowValues[2]
                        toolinfo.tool_state = ToolState.objects.get(tool_state_name='没有记录')
                        toolinfo.tool_damage_extent = ToolDamageExtent.objects.get(tool_damage_extent_name='正常')
                        toolinfo.save()

                    return render(request, "manager-success.html", locals())
                    
            except Exception as err:
                #print(type(err))
                print('错误信息是: ',err)
                error_info = '上传文件失败! 错误信息是: '+str(err)
                form = FileUploadFormSourceData()
                what = "文件传输"
                   
        else:
            error_info = '上传文件失败!'
            form = FileUploadFormSourceData()
            what = "文件传输"
        
    else:
        print("get request")
        #context = {'form': myform, 'what': "文件传输"}
        form = FileUploadFormSourceData()
        what = "文件传输"
        
    return render(request, 'manager-tool-data-upload.html', locals())

@my_login_required
def manager_success_views(request,user):
      
    return render(request,'manager-success.html',locals())

@my_login_required
def manager_tool_data_query_views(request,user):

    #如果是post提交
    if request.method == "POST":
        print("post request")

        #获取前端传过来的查询信息
        tool_name = request.POST.get('tool_name', '')
        tool_type = request.POST.get('tool_type', '')
        tool_state = request.POST.get('tool_state', '')
        tool_damage_extent = request.POST.get('tool_damage_extent', '')
        
        print('tool_name = ',tool_name)
        print('tool_type = ',tool_type)
        print('tool_state = ',tool_state)
        print('tool_damage_extent = ',tool_damage_extent)

        try:
            with transaction.atomic():
                
                #获取工具信息
                #toolinformationlist = ToolInfo.objects.get(tool_encoding=tool_encoding)
                toolinformationlist = ToolInfo.objects.filter(tool_name=tool_name).filter(tool_type=tool_type).filter(tool_state=tool_state).filter(tool_damage_extent=tool_damage_extent)

                return render(request,'manager-tool-data-query.html',locals())

        except Exception as err:
            #print(type(err))
            #error_info = '工具借出失败! 错误信息是: '+str(err)
            print('错误信息是: ',err)
            
    else:
        print("get request")
        #获取工具信息
        toolinformationlist = ToolInfo.objects.all()

    return render(request,'manager-tool-data-query.html',locals())

@my_login_required
def manager_employee_add_views(request,user):

    #如果是post提交
    if request.method == "POST":
        print("post request")
        myform = FormEmployeeInfo(request.POST)

        if myform.is_valid():
            #获取前端传过来的文件信息
            employee_number = request.POST.get('employee_number', '')
            employee_name = request.POST.get('employee_name', '')
            employee_tele = request.POST.get('employee_tele', '')
            #employee_dentification = request.POST.get('employee_dentification', '')
            
            print('employee_number = ',employee_number)
            print('employee_name = ',employee_name)
            print('employee_tele = ',employee_tele)
            #print('employee_dentification = ',employee_dentification)

            try:
                with transaction.atomic():
                    #检查该员工是否已存着
                    employee = Employee.objects.filter(employee_number=employee_number)
                    if employee.exists():
                        error_info = '该员工信息已存在!'
                        form = FormEmployeeInfo()
                        what = "添加员工信息"
                        return render(request,'manager-employee-add.html',locals())
                    
                    #保存员工信息
                    employeeinfo = Employee()
                    employeeinfo.employee_number = employee_number
                    employeeinfo.employee_name = employee_name
                    employeeinfo.employee_tele = employee_tele
                    #employeeinfo.employee_dentification = employee_dentification
                    employeeinfo.save()

                    return render(request, "manager-success.html", locals())

            except Exception as err:
                #print(type(err))
                print('错误信息是: ',err)
                error_info = '添加员工信息失败! 错误信息是: '+str(err)
                form = FormEmployeeInfo()
                what = "添加员工信息"

        else:
            error_info = '添加员工信息失败!'
            form = FormEmployeeInfo()
            what = "添加员工信息"

    else:
        print("get request")
        #context = {'form': myform, 'what': "工具归还"}
        form = FormEmployeeInfo()
        what = "添加员工信息"
      
    return render(request,'manager-employee-add.html',locals())

@my_login_required
def manager_employee_query_views(request,user):

    employeelist = Employee.objects.all()
      
    return render(request,'manager-employee-query.html',locals())

@my_login_required
def manager_user_jurisdiction_query_views(request,user):

    userlist = User.objects.all()
      
    return render(request,'manager-user-jurisdiction-query.html',locals())

@my_login_required
def tool_br_data_statistics_views(request,user):

    toolborrowreturnrecordlist = ToolBorrowReturnRecord.objects.all()
      
    return render(request,'tool-br-data-statistics.html',locals())

@my_login_required
def tool_br_data_analysis_views(request,user):

    toolborrowreturnrecordlist = ToolBorrowReturnRecord.objects.all()
      
    return render(request,'tool-br-data-analysis.html',locals())

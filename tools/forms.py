from django import forms

class FileUploadFormSourceData(forms.Form):
    #required=True 是否必填,label=None Label内容.
    file_name = forms.CharField(max_length=30,min_length=1,label='文件名称:')
    file_describe = forms.CharField(max_length=30,min_length=1,required=False,label='文件描述:')
    file_additional_info = forms.CharField(max_length=30,min_length=1,required=False,label='附加信息:')
    my_file = forms.FileField(label='上传文件:')

class FormToolBorrowInfo(forms.Form):
    #required=True 是否必填,label=None Label内容.
    tool_encoding = forms.CharField(max_length=30,min_length=2,required=True,label='工具编号:')
    employee_number = forms.CharField(max_length=30,min_length=2,required=True,label='员工编号:')

class FormToolReturnInfo(forms.Form):
    #required=True 是否必填,label=None Label内容.
    tool_encoding = forms.CharField(max_length=30,min_length=2,required=True,label='工具编号:')
    employee_number = forms.CharField(max_length=30,min_length=2,required=True,label='员工编号:')
    #单select,choices=() 选项,widget=None 插件 默认select插件,initial=None 初始值,help_text='' 帮助提示.
    tool_damage_extent = forms.ChoiceField(choices=(('TDE1', '正常'),('TDE2', '损坏'),('TDE3', '报废')),required=True,initial=1,widget=None,label='工具损坏程度:')
      
class FormEmployeeInfo(forms.Form):
    #required=True 是否必填,label=None Label内容.
    employee_number = forms.CharField(max_length=20,min_length=2,required=True,label='员工编号:')
    employee_name = forms.CharField(max_length=20,min_length=2,required=True,label='员工姓名:')
    employee_tele = forms.CharField(max_length=20,min_length=8,required=True,label='联系电话:')
    #employee_dentification = forms.CharField(max_length=20,min_length=0,required=False,label='员工身份证号:')
    
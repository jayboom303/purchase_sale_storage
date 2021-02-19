from django.db import models

# Create your models here.
#1权限表
class Permission(models.Model):
    
    permission_level = models.CharField(max_length=30, unique=True, verbose_name='权限级别', null=False)
    permission_note = models.CharField(max_length=80, unique=True, verbose_name='权限说明', null=True, blank=True)

    def __str__(self):
        return self.permission_level

    class Meta:
        verbose_name_plural = '权限表'

#2角色表
class Role(models.Model):
    
    role_name = models.CharField(max_length=30, unique=True, verbose_name='角色名称', null=False)
    role_number = models.CharField(max_length=30, unique=True, verbose_name='角色名称编号', null=False)
    role_note = models.CharField(max_length=80, unique=True, verbose_name='角色说明', null=True, blank=True)
    permission= models.ForeignKey('Permission', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name='权限')

    def __str__(self):
        return self.role_name

    class Meta:
        verbose_name_plural = '角色表'

#3用户状态表
class UserState(models.Model):
    
    user_state_name = models.CharField(max_length=30, verbose_name='用户状态表名称', null=False)
    user_state_number = models.CharField(max_length=30, verbose_name='用户状态表名称编号', null=False)
    user_state_note = models.CharField(max_length=30, verbose_name='用户状态表名称说明', null=False)
    
    def __str__(self):
        return self.user_state_name

    class Meta:
        verbose_name_plural = '状态表'

#4用户表
class User(models.Model):

    account = models.CharField(max_length=30, unique=True, verbose_name='用户账号', null=False)
    upwd = models.CharField(max_length=30, verbose_name='用户密码', null=False)
    name = models.CharField(max_length=30, verbose_name='用户姓名', null=False)
    tele = models.CharField(max_length=30, unique=True, verbose_name='用户联系电话', null=False)
    createdate = models.DateField(auto_now=True, verbose_name='创建时间')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    role = models.ForeignKey('Role', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name='角色')
    user_state = models.ForeignKey('UserState', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name='人员状态')

    def __str__(self):
        return self.account

    class Meta:
        verbose_name_plural = '用户表'

#5员工表
class Employee(models.Model):

    employee_number = models.CharField(max_length=30, unique=True, verbose_name='员工编号', null=False)
    employee_name = models.CharField(max_length=30, verbose_name='员工姓名', null=False)
    employee_tele = models.CharField(max_length=30, unique=True, verbose_name='员工电话', null=False)
    #employee_dentification = models.CharField(max_length=30, unique=True, verbose_name='员工身份证号', null=False)

    def __str__(self):
        return self.employee_name

    class Meta:
        verbose_name_plural = '员工表'

#6上传工具信息表
class ToolDataUploadInfo(models.Model):

    tool_file_name = models.CharField(max_length=30, verbose_name='工具名称', null=False)
    tool_file_describe = models.CharField(max_length=30, verbose_name='文件描述', null=False)
    tool_file_additional_info = models.CharField(max_length=30, verbose_name='附加信息', null=False)

    def __str__(self):
        return self.tool_file_name

    class Meta:
        verbose_name_plural = '上传工具信息表'

#7工具信息表
class ToolInfo(models.Model):

    tool_name = models.CharField(max_length=30, verbose_name='工具名称', null=False)
    tool_type = models.CharField(max_length=30, verbose_name='工具类型', null=False)
    tool_encoding = models.CharField(max_length=30, unique=True, verbose_name='工具编码', null=False)
    tool_state = models.ForeignKey('ToolState', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name='工具借出状态表')
    tool_borrow_employee = models.ForeignKey('Employee', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name='工具借出员工表')
    tool_damage_extent = models.ForeignKey('ToolDamageExtent', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name='工具损坏程度表')

    def __str__(self):
        return self.tool_name

    class Meta:
        verbose_name_plural = '工具信息表'

#8工具借出状态表
class ToolState(models.Model):

    tool_state_name = models.CharField(max_length=30, unique=True, verbose_name='工具状态表名称', null=False)
    tool_state_number = models.CharField(max_length=30, unique=True, verbose_name='工具状态表名称编号', null=False)
    tool_state_note = models.CharField(max_length=30, verbose_name='工具状态表名称说明', null=False)
    
    def __str__(self):
        return self.tool_state_name

    class Meta:
        verbose_name_plural = '工具借出状态表'

#9工具损坏程度表
class ToolDamageExtent(models.Model):

    tool_damage_extent_name = models.CharField(max_length=30, unique=True, verbose_name='工具损坏程度名称', null=False)
    tool_damage_extent_number = models.CharField(max_length=30, unique=True, verbose_name='工具损坏程度名称编号', null=False)
    tool_damage_extent_note = models.CharField(max_length=30, verbose_name='工具损坏程度名称说明', null=False)
    
    def __str__(self):
        return self.tool_damage_extent_name

    class Meta:
        verbose_name_plural = '工具损坏程度表'

#10工具借出记录表
class ToolBorrowReturnRecord(models.Model):

    toolinfo = models.ForeignKey('ToolInfo', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name='工具编码')
    employee = models.ForeignKey('Employee', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name='员工编号')
    createdate = models.DateField(auto_now_add=True, verbose_name='创建时间')
    tool_state = models.ForeignKey('ToolState', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name='工具借出状态')
    tool_damage_extent = models.ForeignKey('ToolDamageExtent', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name='工具损坏程度')

    def __str__(self):
        return self.tool_encoding

    class Meta:
        verbose_name_plural = '工具借出记录表'


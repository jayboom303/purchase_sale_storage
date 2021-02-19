# Generated by Django 3.1.5 on 2021-02-09 01:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_number', models.CharField(max_length=30, unique=True, verbose_name='员工编号')),
                ('employee_name', models.CharField(max_length=30, verbose_name='员工姓名')),
                ('employee_tele', models.CharField(max_length=30, unique=True, verbose_name='员工电话')),
                ('employee_dentification', models.CharField(max_length=30, unique=True, verbose_name='员工身份证号')),
            ],
            options={
                'verbose_name_plural': '员工表',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_level', models.CharField(max_length=30, unique=True, verbose_name='权限级别')),
                ('permission_note', models.CharField(blank=True, max_length=80, null=True, unique=True, verbose_name='权限说明')),
            ],
            options={
                'verbose_name_plural': '权限表',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=30, unique=True, verbose_name='角色名称')),
                ('role_number', models.CharField(max_length=30, unique=True, verbose_name='角色名称编号')),
                ('role_note', models.CharField(blank=True, max_length=80, null=True, unique=True, verbose_name='角色说明')),
                ('permission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pss_homepage.permission', verbose_name='权限')),
            ],
            options={
                'verbose_name_plural': '角色表',
            },
        ),
        migrations.CreateModel(
            name='ToolDamageExtent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tool_damage_extent_name', models.CharField(max_length=30, verbose_name='工具损坏程度名称')),
                ('tool_damage_extent_number', models.CharField(max_length=30, verbose_name='工具损坏程度名称编号')),
                ('tool_damage_extent_note', models.CharField(max_length=30, verbose_name='工具损坏程度名称说明')),
            ],
            options={
                'verbose_name_plural': '工具损坏程度表',
            },
        ),
        migrations.CreateModel(
            name='ToolDataUploadInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tool_file_name', models.CharField(max_length=30, verbose_name='工具名称')),
                ('tool_file_describe', models.CharField(max_length=30, verbose_name='文件描述')),
                ('tool_file_additional_info', models.CharField(max_length=30, verbose_name='附加信息')),
            ],
            options={
                'verbose_name_plural': '上传工具信息表',
            },
        ),
        migrations.CreateModel(
            name='ToolState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tool_state_name', models.CharField(max_length=30, verbose_name='工具状态表名称')),
                ('tool_state_number', models.CharField(max_length=30, verbose_name='工具状态表名称编号')),
                ('tool_state_note', models.CharField(max_length=30, verbose_name='工具状态表名称说明')),
            ],
            options={
                'verbose_name_plural': '工具借出状态表',
            },
        ),
        migrations.CreateModel(
            name='UserState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_state_name', models.CharField(max_length=30, verbose_name='用户状态表名称')),
                ('user_state_number', models.CharField(max_length=30, verbose_name='用户状态表名称编号')),
                ('user_state_note', models.CharField(max_length=30, verbose_name='用户状态表名称说明')),
            ],
            options={
                'verbose_name_plural': '状态表',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=30, unique=True, verbose_name='用户账号')),
                ('upwd', models.CharField(max_length=30, verbose_name='用户密码')),
                ('name', models.CharField(max_length=30, verbose_name='用户姓名')),
                ('tele', models.CharField(max_length=30, unique=True, verbose_name='用户联系电话')),
                ('createdate', models.DateField(auto_now=True, verbose_name='创建时间')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否激活')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pss_homepage.role', verbose_name='角色')),
                ('user_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pss_homepage.userstate', verbose_name='人员状态')),
            ],
            options={
                'verbose_name_plural': '用户表',
            },
        ),
        migrations.CreateModel(
            name='ToolInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tool_name', models.CharField(max_length=30, verbose_name='工具名称')),
                ('tool_type', models.CharField(max_length=30, verbose_name='工具类型')),
                ('tool_encoding', models.CharField(max_length=30, unique=True, verbose_name='工具编码')),
                ('tool_damage_extent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pss_homepage.tooldamageextent', verbose_name='工具损坏程度表')),
                ('tool_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pss_homepage.toolstate', verbose_name='工具借出状态表')),
            ],
            options={
                'verbose_name_plural': '工具信息表',
            },
        ),
        migrations.CreateModel(
            name='ToolBorrowReturnRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdate', models.DateField(auto_now=True, verbose_name='创建时间')),
                ('employee_number', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pss_homepage.employee', verbose_name='员工编号')),
                ('tool_damage_extent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pss_homepage.tooldamageextent', verbose_name='工具损坏程度')),
                ('tool_encoding', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pss_homepage.toolinfo', verbose_name='工具编码')),
                ('tool_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pss_homepage.toolstate', verbose_name='工具借出状态')),
            ],
            options={
                'verbose_name_plural': '工具借出记录表',
            },
        ),
    ]

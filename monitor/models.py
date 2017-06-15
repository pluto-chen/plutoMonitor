from django.db import models
from monitor import auth
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

# Create your models here.

class Host(models.Model):

    hostname = models.CharField(u'主机名',max_length=64,unique=True)
    ipaddr = models.GenericIPAddressField(unique=True)
    hostgroups  = models.ManyToManyField('HostGroup',blank=True)
    templates = models.ManyToManyField('Template',blank=True)
    monitor_mode_choices = (
        ('agent',u'客户端'),
        ('snmp','Snmp'),
        ('wget','Wget')
    )
    monitor_mode = models.CharField(u'监控方式',max_length=32,choices=monitor_mode_choices)
    status_choices = (
        (1,'Online'),
        (2,'Offline'),
        (3,'Down'),
        (4,'Unreachable'),
        (5,'Problem'),
    )
    status = models.IntegerField(u'状态',choices=status_choices)
    memo = models.TextField(u'备注',blank=True,null=True)

    def __str__(self):
        return self.hostname

class HostGroup(models.Model):
    groupname = models.CharField(u'主机组名',max_length=64,unique=True)
    templates = models.ManyToManyField('Template', blank=True)
    memo = models.TextField(u'备注',blank=True,null=True)

    def __str__(self):
        return self.groupname

class Template(models.Model):

    tname = models.CharField(u'模板名',max_length=64,unique=True)
    services = models.ManyToManyField('Service')
    triggers = models.ManyToManyField('Trigger')

    def __str__(self):
        return self.tname

class Service(models.Model):

    sname = models.CharField(u'服务名',max_length=64,unique=True)
    interval = models.IntegerField(u'监控间隔',default=60)
    plugin_name = models.CharField(u'插件名',max_length=64,default='n/a')
    items = models.ManyToManyField('ServiceIndex',verbose_name=u'监控指标',blank=True)
    memo = models.TextField(u'备注',blank=True,null=True)

    def __str__(self):
        return self.sname

class ServiceIndex(models.Model):

    iname = models.CharField(u'指标名',max_length=64)
    key = models.CharField(u'指标key',max_length=64)
    data_type_choices = (
        ('int','int'),
        ('float','float'),
        ('str','string'),
    )
    data_type = models.CharField(u'数据类型',max_length=64,choices=data_type_choices,default=int)
    memo = models.TextField(u'备注',blank=True,null=True)

    def __str__(self):
        return '%s:%s' % (self.iname,self.key)

class Trigger(models.Model):

    name = models.CharField(u'触发器名称',max_length=64)
    severity_choices = (
        (1,'information'),
        (2,'warning'),
        (3,'high'),
        (4,'disaster'),
    )
    severity = models.IntegerField(u'告警级别',choices=severity_choices)
    enabled = models.BooleanField(default=True)
    memo = models.TextField(u'备注',blank=True,null=True)

    def __str__(self):
        return '<trigger:%s severity:%s>' % (self.name,self.get_severity_display())

class TriggerExpression(models.Model):

    trigger = models.ForeignKey('Trigger',verbose_name=u'所属触发器')
    service = models.ForeignKey('Service',verbose_name=u'关联服务')
    service_index = models.ForeignKey('ServiceIndex',verbose_name=u'服务指标')
    threshold = models.IntegerField(u'阈值')
    operator_choices = (
        ('eq','='),
        ('lt','<'),
        ('gt','>'),
    )
    operator = models.CharField(u'运算符号',max_length=32,choices=operator_choices)
    mode_choices = (
        ('avg','Average'),
        ('max','Max'),
        ('hit','Hit'),
        ('last','Last'),
    )
    mode = models.CharField(u'取值方式',max_length=32,choices=mode_choices)
    func_args = models.CharField(u'传入参数',max_length=64)
    logic_type_choices = (
        ('or','OR'),
        ('and','AND'),
    )
    logic_type = models.CharField(u'逻辑关系',choices=logic_type_choices,max_length=16,blank=True,null=True)

    def __str__(self):
        return '%s:%s %s %s' %(self.service_index.iname,self.mode,self.operator,self.threshold)

class UserProfile(auth.AbstractBaseUser, auth.PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,

    )
    password = models.CharField(_('password'), max_length=128,
                                help_text=mark_safe('''<a class='btn-link' href='password'>重置密码</a>'''))

    phone = models.BigIntegerField(blank=True,null=True)
    weixin = models.CharField(max_length=64,blank=True,null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        verbose_name='staff status',
        default=True,
        help_text='Designates whether the user can log into this admin site.',
    )
    name = models.CharField(max_length=32)
    #role = models.ForeignKey("Role",verbose_name="权限角色")

    memo = models.TextField('备注', blank=True, null=True, default=None)
    date_joined = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name','token','department','tel','mobile','memo']
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __str__ on Python 2
        return self.email

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True
    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    @property
    def is_superuser(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


    objects = auth.UserManager()

    class Meta:
        verbose_name = '账户'
        verbose_name_plural = '账户'


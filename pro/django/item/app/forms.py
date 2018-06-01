from django.core.exceptions import ValidationError
from django import forms


def password_validator(password):
    """
    判断密码的长度
    """
    if len(password) < 8:
        raise ValidationError('密码长度不能小于16个字符')
    #复杂度
    chars = set(password)
    nums = set('0123456789')
    upper = set(chr(i) for i in range(65, 91))
    lower = set(chr(i) for i in range(97, 123))
    puncts = set(chr(i) for i in range(33, 48))
    #passed状态吗记录password是否满足一下条件，抛出相应异常
    passed = True
    errmsg = []
    if not chars & nums:
        passed = False
        errmsg.append('密码必须包含数字')
    if not chars & upper:
        passed = False
        errmsg.append('密码必须包含大写字母')
    if not chars & lower:
        passed = False
        errmsg.append('密码必须包含小写字母')
    if not chars & puncts:
        passed = False
        errmsg.append('密码必须包含标点符号')
    if not passed:
        raise ValidationError(', '.join(errmsg))


class SignupForm(forms.Form):
    username = forms.CharField(max_length=8)
    password = forms.CharField(min_length=8, widget=forms.widgets.PasswordInput)
#validators=[password_validator]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=8)
    password = forms.CharField(min_length=8, widget=forms.widgets.PasswordInput)
    captcha = forms.CharField(max_length=12)

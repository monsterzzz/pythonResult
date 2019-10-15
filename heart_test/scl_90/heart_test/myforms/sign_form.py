from django import forms

class SignForm(forms.Form):
    account = forms.IntegerField(error_messages={'required':u'帐号不能为空'},widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(error_messages={'required':u'密码不能为空'},max_length=15,min_length=6,widget=forms.PasswordInput(attrs={'class':'form-control'}))


class FullMsg(forms.Form):
    name = forms.CharField(error_messages={'required':u'密码不能为空'},max_length=15,min_length=2,widget=forms.TextInput(attrs={'class':'form-control'}))
    sex = forms.ChoiceField(choices=(((u'1', u'男'), (u'2', u'女'))),label=None,widget=forms.Select(attrs={'class':'form-control'}))
    age = forms.IntegerField(error_messages={'required':u'学号不能为空'},max_value=120,min_value=0,widget=forms.TextInput(attrs={'class':'form-control'}))
    family = forms.ChoiceField(choices=(((u'1', u'否'), (u'2', u'是'))),label=None,widget=forms.Select(attrs={'class':'form-control'}))
    address_type = forms.ChoiceField(choices=(((u'1', u'城镇'), (u'2', u'乡村'))),label=None,widget=forms.Select(attrs={'class':'form-control'}))
    marry_type = forms.ChoiceField(choices=(((u'1', u'未婚'), (u'2', u'已婚'),(u'3', u'离异'))),label=None,widget=forms.Select(attrs={'class':'form-control'}))
    #性别年龄户籍类型(城镇，乡村)是否单亲，是否离异

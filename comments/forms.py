from django import forms



class CommentForm(forms.Form):
    user = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control my-form-control"}), label='ВАШЕ ИМЯ')
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    parent_id  = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField( widget=forms.Textarea(attrs={'class': "form-control"}), label='ВАШ КОММЕНТАРИЙ')

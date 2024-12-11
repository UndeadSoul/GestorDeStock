from django import forms
from crud.models import addMovements
from crud.models import product
from registerlogin.models import Profile


class addmov_form(forms.ModelForm):
    product=forms.ModelChoiceField(queryset=product.objects.all(), label="Producto")
    incharge=forms.ModelChoiceField(queryset=Profile.objects.all(), label="Encargado")
    addmov_prodQuantity=forms.IntegerField(label="Cantidad", min_value=1)
    class Meta:
        model=addMovements
        fields=['product','addmov_prodQuantity','incharge']
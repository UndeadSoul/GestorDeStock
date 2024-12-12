from django import forms
from crud.models import addMovements, removeMovements
from crud.models import product
from registerlogin.models import Profile
from django.contrib.auth.models import User


class addmov_form(forms.ModelForm):
    product=forms.ModelChoiceField(queryset=product.objects.all(), label="Producto")
    incharge=forms.ModelChoiceField(queryset=Profile.objects.all(), label="Encargado")
    addmov_prodQuantity=forms.IntegerField(label="Cantidad", min_value=1)
    class Meta:
        model=addMovements
        fields=['product','addmov_prodQuantity','incharge']

class removemov_form(forms.ModelForm):
    product=forms.ModelChoiceField(queryset=product.objects.all(), label="Producto")
    incharge=forms.ModelChoiceField(queryset=Profile.objects.all(), label="Encargado")
    removemov_prodQuantity=forms.IntegerField(label="Cantidad", min_value=1)
    class Meta:
        model=removeMovements
        fields=['product','removemov_prodQuantity','incharge']

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        removemov_prodQuantity = cleaned_data.get('removemov_prodQuantity')

        if product and removemov_prodQuantity:  # Validar que ambos campos estén llenos
            if removemov_prodQuantity > product.product_stock:
                raise forms.ValidationError(
                    f"La cantidad a retirar ({removemov_prodQuantity}) no puede ser mayor al stock disponible ({product.product_stock})."
                )
        return cleaned_data

class addproduct_form(forms.ModelForm):
    product=forms.ModelChoiceField(queryset=product.objects.all(), label="Producto")
    incharge=forms.ModelChoiceField(queryset=Profile.objects.all(), label="Encargado")
    removemov_prodQuantity=forms.IntegerField(label="Cantidad", min_value=1)
    class Meta:
        model=removeMovements
        fields=['product','removemov_prodQuantity','incharge']

    
class UserCreationForm(forms.ModelForm):
    username = forms.CharField(required=True, label="Nombre de usuario")
    first_name = forms.CharField(required=True, label="Nombre")
    last_name = forms.CharField(required=True, label="Apellido")
    email = forms.EmailField(required=True, label="Correo electrónico")

    # Campos del modelo Profile
    rut = forms.CharField(required=False, label="RUT")
    telephone = forms.CharField(required=False, label="Teléfono")
    name = forms.CharField(required=False, label="Nombre completo")
    image = forms.ImageField(required=False, label="Imagen de perfil")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
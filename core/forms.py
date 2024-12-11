from django import forms
from crud.models import addMovements, removeMovements
from crud.models import product
from registerlogin.models import Profile


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
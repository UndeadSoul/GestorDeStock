from django.db import models
from registerlogin.models import Profile
from django.db import transaction

class employee(models.Model):
    employee_id=models.AutoField(primary_key=True)
    employee_rut=models.CharField(max_length=12)
    employee_name=models.CharField(max_length=50)
    employee_contactnumber=models.CharField(max_length=20)
    employee_email=models.CharField(max_length=50)
    employee_password=models.CharField(max_length=30)

class storage(models.Model):
    storage_id=models.AutoField(primary_key=True)
    storage_address=models.CharField(max_length=50)
    storage_schedule=models.CharField(max_length=50)

    def __str__(self):
        return f'N°{self.storage_id} {self.storage_address}'

class product(models.Model):
    product_id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=50)
    product_image=models.ImageField()
    product_stock=models.PositiveIntegerField()
    product_price=models.PositiveIntegerField()
    product_desc=models.CharField(max_length=50)
    storage=models.ForeignKey(storage, on_delete=models.CASCADE, verbose_name=("storage"), default=1)

    def __str__(self):
        return self.product_name

class addMovements(models.Model):
    addmov_id=models.AutoField(primary_key=True)
    addmov_date=models.DateTimeField(auto_now_add=True)
    addmov_prodQuantity=models.PositiveIntegerField()
    # product=models.ManyToManyField(product, verbose_name=("product"))
    # incharge=models.ManyToManyField(employee, verbose_name=("employee"))
    product=models.ForeignKey(product, on_delete=models.CASCADE, verbose_name=("product"), default=1)
    incharge=models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=("profile"), default=1)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            product=self.product
            product.product_stock += self.addmov_prodQuantity
            product.save()
            super().save(*args, **kwargs)

class removeMovements(models.Model):
    removemov_id=models.AutoField(primary_key=True)
    removemov_date=models.DateTimeField(auto_now_add=True)
    removemov_prodQuantity=models.PositiveIntegerField()
    # product=models.ManyToManyField(product, on_delete=models.CASCADE, verbose_name=("product"))
    # incharge=models.ManyToManyField(employee, on_delete=models.CASCADE, verbose_name=("employee"))
    product=models.ForeignKey(product, on_delete=models.CASCADE, verbose_name=("product"), default=1)
    incharge=models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=("profile"), default=1)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            product=self.product
            product.product_stock -= self.removemov_prodQuantity
            product.save()
            super().save(*args, **kwargs)

# class sendedMails(models.Model):
#     emailDate=models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return "Mandado"+self.emailDate
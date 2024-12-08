from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from crud.models import addMovements,removeMovements,employee,storage,product
from datetime import datetime, timedelta
from django.db.models import Q


# Home
def home(request):
    # Obtener los últimos movimientos
    lastInMovements = addMovements.objects.all().order_by('-addmov_id')[:5]
    lastOutMovements = removeMovements.objects.all().order_by('-removemov_id')[:5]
    # Obtener stocks críticos
    critical = product.objects.filter(product_stock__lt=5)

    return render(request, "core/home.html", {
        "inmov": lastInMovements,
        "outmov": lastOutMovements,
        "criticalStock": critical
    })

def usermanage(request):
    return render(request,"core/usermanage.html",{})

# Records
def records(request):
    # Obtener el periodo que se quiere consultar
    period=request.GET.get("periodoftime")
    # Entregar los elementos en base al periodo obtenido
    if period=="day":
        #obtener fecha de hoy
        today=datetime.now().date()
        #filtrar los registros de hoy
        recordsoftodayadd=addMovements.objects.filter(addmov_date=today)
        recordsoftodayremove=removeMovements.objects.filter(removemov_date=today)
        recordsadd=recordsoftodayadd
        recordsremove=recordsoftodayremove

    elif period=="week":
        #obtener fecha de hace una semana
        today=datetime.now().date()
        lastweek=today-timedelta(days=7)
        #filtrar los registros de la ultima semana
        recordsoflastweekadd=addMovements.objects.filter(addmov_date__gte=lastweek)
        recordsoflastweekremove=removeMovements.objects.filter(removemov_date__gte=lastweek)
        recordsadd=recordsoflastweekadd
        recordsremove=recordsoflastweekremove

    elif period=="month":
        #obtener fecha de hace un mes
        today=datetime.now().date()
        lastmonth=today-timedelta(days=31)
        #filtrar los registros del ultimo mes
        recordsoflastmonthadd=addMovements.objects.filter(removemov_date=lastmonth)
        recordsoflastmonthremove=removeMovements.objects.filter(removemov_date=lastmonth)
        recordsadd=recordsoflastmonthadd
        recordsremove=recordsoflastmonthremove

    elif period=="year":
        #obtener fecha de hace un año
        today=datetime.now().date()
        lastyear=today-timedelta(days=365)
        #filtrar los registros del ultimo año
        recordsoflastyearadd=addMovements.objects.filter(removemov_date=lastyear)
        recordsoflastyearremove=removeMovements.objects.filter(removemov_date=lastyear)
        recordsadd=recordsoflastyearadd
        recordsremove=recordsoflastyearremove

    elif period=="all":
        #obtener todos los registros
        recordsadd=addMovements.objects.all()
        recordsremove=removeMovements.objects.all()

    else: 
        #obtener fecha de hoy
        today=datetime.now().date()
        #filtrar los registros de hoy
        recordsoftodayadd=addMovements.objects.filter(addmov_date=today)
        recordsoftodayremove=removeMovements.objects.filter(removemov_date=today)
        recordsadd=recordsoftodayadd
        recordsremove=recordsoftodayremove
        pass

    return render(request,"core/records.html",{
        "recordsadd":recordsadd,
        "recordsremove":recordsremove
    })

# Inventory
def inventory(request):
    #Obtener los productos en inventario y ordenarlos por cantidad
    products=product.objects.all().order_by('product_stock')
    return render(request,"core/inventory.html",{
        "products":products,
    })

# Move stock
def movestock(request):
    return render(request,"core/movestock.html",{})

### Add stock
def addstock(request):
    return render(request,"core/addstock.html",{})

def addproduct(request):
    return render(request,"core/addproduct.html",{})

### Remove stock
def removestock(request):
    return render(request,"core/removestock.html",{})

def confirmremove(request):
    return render(request,"core/confirmremove.html",{})

# Confirm
def finalconfirm(request):
    return render(request,"core/finalconfirm.html",{})
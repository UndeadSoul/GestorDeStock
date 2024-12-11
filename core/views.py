from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from crud.models import addMovements,removeMovements,employee,storage,product
from datetime import datetime, timedelta
from django.db.models import Q
from django.views.generic import TemplateView,CreateView
from .forms import addmov_form, removemov_form
from django.contrib import messages
from registerlogin.models import Profile


# Home
def home(request):
    # Obtener los últimos movimientos
    lastInMovements = addMovements.objects.all().order_by('-addmov_id')[:5]
    lastOutMovements = removeMovements.objects.all().order_by('-removemov_id')[:5]
    # Obtener stocks críticos
    critical = product.objects.filter(product_stock__lt=5)
    # Obtener el perfil del usuario
    # Verificar si el usuario está autenticado y obtener el perfil
    user_profile = None
    if request.user.is_authenticated:  # Verifica si el usuario está autenticado
        user_profile = Profile.objects.filter(user=request.user)

    return render(request, "core/home.html", {
        "inmov": lastInMovements,
        "outmov": lastOutMovements,
        "criticalStock": critical,
        "userprofile":user_profile
    })

def usermanage(request):
    #lista con los usuarios
    users=User.objects.all()
    #si es que se seleccionó un usuario
    selectedUserId=request.GET.get("userid",users[0])
    selectedUser=User.objects.filter(id=selectedUserId)

    #si es que se está añadiendo un usuario
    adduser=request.GET.get("addUser",False)
    return render(request,"core/usermanage.html",{
        "users":users,
        "selectedUser":selectedUser,
        "adduser":adduser,
    })

# Records
def records(request):
    # Obtener el periodo que se quiere consultar
    period=request.GET.get("periodoftime")
    # Entregar los elementos en base al periodo obtenido
    if period=="day":
        # Obtener el rango del día de hoy
        today = datetime.now()
        day_start = datetime.combine(today.date(), datetime.min.time())  # 00:00:00
        day_end = datetime.combine(today.date(), datetime.max.time())    # 23:59:59
        #filtrar los registros de hoy
        recordsoftodayadd=addMovements.objects.filter(addmov_date__range=(day_start, day_end)).order_by('-addmov_date')
        recordsoftodayremove=removeMovements.objects.filter(removemov_date__range=(day_start, day_end)).order_by('-removemov_date')
        recordsadd=recordsoftodayadd
        recordsremove=recordsoftodayremove
        print("add",recordsadd)
        print("remove",recordsremove)

    elif period=="week":
        #obtener fecha de hace una semana
        today=datetime.now().date()
        lastweek=today-timedelta(days=7)
        #filtrar los registros de la ultima semana
        recordsoflastweekadd=addMovements.objects.filter(addmov_date__gte=lastweek).order_by('-addmov_date')
        recordsoflastweekremove=removeMovements.objects.filter(removemov_date__gte=lastweek).order_by('-removemov_date')
        recordsadd=recordsoflastweekadd
        recordsremove=recordsoflastweekremove

    elif period=="month":
        #obtener fecha de hace un mes
        today=datetime.now().date()
        lastmonth=today-timedelta(days=31)
        #filtrar los registros del ultimo mes
        recordsoflastmonthadd=addMovements.objects.filter(addmov_date__gte=lastmonth).order_by('-addmov_date')
        recordsoflastmonthremove=removeMovements.objects.filter(removemov_date__gte=lastmonth).order_by('-removemov_date')
        recordsadd=recordsoflastmonthadd
        recordsremove=recordsoflastmonthremove

    elif period=="year":
        #obtener fecha de hace un año
        today=datetime.now().date()
        lastyear=today-timedelta(days=365)
        #filtrar los registros del ultimo año
        recordsoflastyearadd=addMovements.objects.filter(addmov_date__gte=lastyear).order_by('-addmov_date')
        recordsoflastyearremove=removeMovements.objects.filter(removemov_date__gte=lastyear).order_by('-removemov_date')
        recordsadd=recordsoflastyearadd
        recordsremove=recordsoflastyearremove

    elif period=="all":
        #obtener todos los registros
        recordsadd=addMovements.objects.all()
        recordsremove=removeMovements.objects.all()

    else: 
# Obtener el rango del día de hoy
        today = datetime.now()
        day_start = datetime.combine(today.date(), datetime.min.time())  # 00:00:00
        day_end = datetime.combine(today.date(), datetime.max.time())    # 23:59:59
        #filtrar los registros de hoy
        recordsoftodayadd=addMovements.objects.filter(addmov_date__range=(day_start, day_end)).order_by('-addmov_date')
        recordsoftodayremove=removeMovements.objects.filter(removemov_date__range=(day_start, day_end)).order_by('-removemov_date')
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
    #Si hay productos obtener el primero para mostrar por defecto
    if len(products)==0:
        #en caso de que no hayan productos, retornará vacío
        selectedProd=""
    else:
        #obtiene la id seleccionada (por defecto la id 0)
        selectedId=request.GET.get("selectedId",0)
        selectedProd=product.objects.filter(product_id=selectedId)

    return render(request,"core/inventory.html",{
        "products":products,
        "selectedProd":selectedProd,
    })

# Move stock
def movestock(request):
    return render(request,"core/movestock.html",{})

### Add stock
def addstock(request):
    #Cargar los productos para mostrarlos como opcion de producto a aumentar el stock
    products=product.objects.all()
    return render(request,"core/addstock.html",{
        "products":products,
    })

class addStockCreateView(CreateView):
    model=addMovements
    form_class=addmov_form
    template_name='core/addstock.html'
    success_url=reverse_lazy('movestock')

    def form_valid(self,form):
        messages.success(self.request, "El movimiento se ha guardado correctamente")
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.success(self.request, "El movimiento no se ha guardado")
        return self.render_to_response(self.get_context_data(form=form))


def addproduct(request):
    #? las id se aumentan automatico, así que no es necesario hacer las consuultas
    return render(request,"core/addproduct.html",{})

### Remove stock
def removestock(request):
    #Aqui solo se introducen los datos del movimiento y en confirmar remove depende si es queda la cantidad necesaria
    return render(request,"core/removestock.html",{})

class removeStockCreateView(CreateView):
    model=addMovements
    form_class=removemov_form
    template_name='core/addstock.html'
    success_url=reverse_lazy('movestock')

    def form_valid(self,form):
        messages.success(self.request, "El movimiento se ha guardado correctamente")
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.success(self.request, "El movimiento no se ha guardado")
        return self.render_to_response(self.get_context_data(form=form))


def confirmremove(request):
    #el html debe hacer la diferencia de si es que queda el stock suficiente
    #obtener el id
    productid=request.GET.get("id")
    #obtener la cantidad
    productamount=request.GET.get("amount")
    #hay suficiente stock?
    selectedprod=product.objects.filter(product_id=productid)
    if (selectedprod[0]-productamount)>=0:
        stock="yes"
    else:
        stock="no"

    return render(request,"core/confirmremove.html",{
        "stock":stock,
        "selectedprod":selectedprod,
        "productamount":productamount,
    })

# Confirm
def finalconfirm(request):
    #Envía a una pagina que confirma que la transaccion fue exitosa y redirige a home
    return render(request,"core/finalconfirm.html",{})
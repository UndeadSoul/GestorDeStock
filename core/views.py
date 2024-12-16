from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from crud.models import addMovements,removeMovements,employee,storage,product
from datetime import datetime, timedelta
from django.db.models import Q
from django.views.generic import TemplateView,CreateView
from .forms import addmov_form, removemov_form,UserCreationForm,addproduct_form
from django.contrib import messages
from registerlogin.models import Profile
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage

# FUNCION PARA CONVERTIR EL PLURAL DE UN GRUPO A SU SINGULAR
def plural_to_singular(plural):
    # Diccionario de palabras
    plural_singular = {
        "trabajadores": "trabajador",
        "jefes": "jefe",
        "administrador": "administrador",
    }
    return plural_singular.get(plural, "error")

# Home
def home(request):
    is_admin_or_jefe = request.user.groups.filter(name__in=['administrador', 'jefes']).exists()
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
        "userprofile":user_profile,
        "is_admin_or_jefe":is_admin_or_jefe,
    })

def usermanage(request):
    is_admin_or_jefe = request.user.groups.filter(name__in=['administrador', 'jefes']).exists()
    #Obtener una lista con los usuarios
    users=Profile.objects.all()
    selectedId=request.GET.get("selectedId",users[0].id)
    selecteduser=Profile.objects.filter(id=selectedId)
    selected=User.objects.get(id=selectedId)
    algo=selected.groups.all()
    
    return render(request,"core/usermanage.html",{
        "users":users,
        "selectedUser":selecteduser,
        "is_admin_or_jefe":is_admin_or_jefe,
        "algo":algo
    })

class AddUserView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "core/adduser.html"
    success_url = reverse_lazy("usermanage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = Group.objects.all()
        singular_groups = [plural_to_singular(group.name).capitalize() for group in groups]
        context["groups"] = zip(groups, singular_groups)
        is_admin_or_jefe= self.request.user.groups.filter(name__in=['administrador', 'jefes']).exists()
        context["is_admin_or_jefe"] = is_admin_or_jefe
        return context

    def form_valid(self, form):
        # Obtener el grupo seleccionado
        group_id = self.request.POST.get("group")
        group = Group.objects.get(id=group_id)

        # Crear el usuario
        user = form.save(commit=False)
        user.set_password("contra1234")
        if group_id != "1":
            user.is_staff = True
        user.save()
        user.groups.clear()
        user.groups.add(group)

        # Actualizar el perfil asociado
        profile = user.profile  # Relación OneToOneField
        profile.rut = form.cleaned_data.get("rut")
        profile.telephone = form.cleaned_data.get("telephone")
        profile.name = form.cleaned_data.get("name")
        profile.image = self.request.FILES.get("image", "users/usuario_defecto.jpg")
        profile.email=user.email
        profile.save()

        return super().form_valid(form)
    
# Records
def records(request):
    # Obtener el periodo que se quiere consultar
    period=request.GET.get("periodoftime")
    # Entregar los elementos en base al periodo obtenido
    if period=="day":
        # Obtener el rango del día de hoy
        today = datetime.now()
        period_start = datetime.combine(today.date(), datetime.min.time())  # 00:00:00
        period_end = datetime.combine(today.date(), datetime.max.time())    # 23:59:59
        #filtrar los registros de hoy
        recordsoftodayadd=addMovements.objects.filter(addmov_date__range=(period_start, period_end)).order_by('-addmov_date')
        recordsoftodayremove=removeMovements.objects.filter(removemov_date__range=(period_start, period_end)).order_by('-removemov_date')
        recordsadd=recordsoftodayadd
        recordsremove=recordsoftodayremove
        print("add",recordsadd)
        print("remove",recordsremove)

    elif period=="week":
        #obtener fecha de hace una semana
        today=datetime.now().date()
        lastweek=today-timedelta(days=7)
        period_start=today
        period_end=lastweek
        #filtrar los registros de la ultima semana
        recordsoflastweekadd=addMovements.objects.filter(addmov_date__gte=lastweek).order_by('-addmov_date')
        recordsoflastweekremove=removeMovements.objects.filter(removemov_date__gte=lastweek).order_by('-removemov_date')
        recordsadd=recordsoflastweekadd
        recordsremove=recordsoflastweekremove

    elif period=="month":
        #obtener fecha de hace un mes
        today=datetime.now().date()
        lastmonth=today-timedelta(days=31)
        period_start=today
        period_end=lastmonth
        #filtrar los registros del ultimo mes
        recordsoflastmonthadd=addMovements.objects.filter(addmov_date__gte=lastmonth).order_by('-addmov_date')
        recordsoflastmonthremove=removeMovements.objects.filter(removemov_date__gte=lastmonth).order_by('-removemov_date')
        recordsadd=recordsoflastmonthadd
        recordsremove=recordsoflastmonthremove

    elif period=="year":
        #obtener fecha de hace un año
        today=datetime.now().date()
        lastyear=today-timedelta(days=365)
        period_start=today
        period_end=lastyear
        #filtrar los registros del ultimo año
        recordsoflastyearadd=addMovements.objects.filter(addmov_date__gte=lastyear).order_by('-addmov_date')
        recordsoflastyearremove=removeMovements.objects.filter(removemov_date__gte=lastyear).order_by('-removemov_date')
        recordsadd=recordsoflastyearadd
        recordsremove=recordsoflastyearremove

    elif period=="all":
        #obtener todos los registros
        today = datetime.now()
        period_start=today
        period_end="Inicio"
        recordsadd=addMovements.objects.all()
        recordsremove=removeMovements.objects.all()

    else: 
# Obtener el rango del día de hoy
        today = datetime.now()
        period_start = datetime.combine(today.date(), datetime.min.time())  # 00:00:00
        period_end = datetime.combine(today.date(), datetime.max.time())    # 23:59:59
        #filtrar los registros de hoy
        recordsoftodayadd=addMovements.objects.filter(addmov_date__range=(period_start, period_end)).order_by('-addmov_date')
        recordsoftodayremove=removeMovements.objects.filter(removemov_date__range=(period_start, period_end)).order_by('-removemov_date')
        recordsadd=recordsoftodayadd
        recordsremove=recordsoftodayremove

    if request.method=="POST":
        #obtener los datos del usuario activo
        user_profile = Profile.objects.get(user=request.user)
        #realizar formato de email
        message="Movimientos de entrada:\n"
        for record in recordsadd:
            message+=" - [{}] {}: {} {} {}\n".format(record.addmov_date.strftime("%d/%m/%Y %H:%M:%S"), "Entrada", record.addmov_prodQuantity, record.product.product_name,record.incharge.name)
        message+="\nMovimientos de salida\n"
        for record in recordsremove:
            message+=" - [{}] {}: {} {} {}\n".format(record.removemov_date.strftime("%d/%m/%Y %H:%M:%S"), "Salida", record.removemov_prodQuantity, record.product.product_name,record.incharge.name)

        email=EmailMessage(
            "Registros de Movimientos - {} / {}".format(period_start,period_end),
            "Mensaje enviado por {} <{}>:\n\n{}".format(user_profile.name,user_profile.email,message),
            #sender
            "{}".format(user_profile.email),
            #destinatario
            ["c986c7998ae9f6@inbox.mailtrap.io",user_profile.email]
        )
        try:
            email.send()
            print("se mandó")
            return redirect(reverse_lazy("finalconfirm"))
        except:
            print("no se mandó")
            return redirect(reverse_lazy("finalconfirm"))


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
    success_url=reverse_lazy('finalconfirm')

    def form_valid(self,form):
        messages.success(self.request, "El movimiento se ha guardado correctamente")
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.success(self.request, "El movimiento no se ha guardado")
        return self.render_to_response(self.get_context_data(form=form))


class addProductCreateView(CreateView):
    model=product
    form_class=addproduct_form
    template_name='core/addproduct.html'
    success_url=reverse_lazy('finalconfirm')

    def form_valid(self,form):
        messages.success(self.request, "El producto se ha guardado correctamente")
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.success(self.request, "El producto no se ha guardado")
        return self.render_to_response(self.get_context_data(form=form))

### Remove stock
def removestock(request):
    #Aqui solo se introducen los datos del movimiento y en confirmar remove depende si es queda la cantidad necesaria
    return render(request,"core/removestock.html",{})

class removeStockCreateView(CreateView):
    model=removeMovements
    form_class=removemov_form
    template_name='core/removestock.html'
    success_url=reverse_lazy('finalconfirm')

    def form_valid(self,form):
        #obtener el producto del que se hace el movimiento
        movement=form.instance
        product=movement.product
        prodquant=movement.removemov_prodQuantity
        #obtener el restante del producto
        updatedStock=product.product_stock-prodquant
        #si el restante del producto es <=5 mandar un mensaje
        if updatedStock<=5:
            #obtener los datos del usuario activo
            user_profile = Profile.objects.get(user=self.request.user)
            #realizar formato de email
            message="El siguiente producto se encuentra con stock crítico\n"
            #obtener los perfiles con rango de jefe
            # Obtener el grupo "jefes"
            jefes_group = Group.objects.get(name="jefes")
            # Filtrar perfiles cuyos usuarios estén en el grupo "jefes"
            jefes_profiles = Profile.objects.filter(user__groups=jefes_group)
            # Obtener los correos de los perfiles
            emails = jefes_profiles.values_list('email', flat=True)
            # Mensaje 
            message+="Nombre producto: {}\nStock restante: {}\nDescripción: \n{}\n".format(product.product_name,updatedStock,product.product_desc)
            email=EmailMessage(
                #asunto
                "Alerta de stock - {}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                #cuerpo
                "Mensaje enviado por {} <{}>:\n\n{}".format(user_profile.name,user_profile.email,message),
                #sender
                "{}".format(user_profile.email),
                #destinatario
                ["c986c7998ae9f6@inbox.mailtrap.io",user_profile.email]+list(emails)
            )
            try:
                email.send()
                print("El correo se mandó")
            except:
                print("El correo no se mandó")
                pass
        messages.success(self.request, "El movimiento se ha guardado correctamente")

        return super().form_valid(form)
    def form_invalid(self,form):
        messages.success(self.request, "El movimiento no se ha guardado")
        return self.render_to_response(self.get_context_data(form=form))

# Confirm
def finalconfirm(request):
    #Envía a una pagina que confirma que la transaccion fue exitosa y redirige a home
    return render(request,"core/finalconfirm.html",{})
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Producto, Paciente, Consulta, Pedido, PedidoDetalle, Turnos
from .form import ProductoCreate, PedidoCreate, PedidoDetalleCreate, ConsultaCreate, Turno_Form
from django.urls import reverse, reverse_lazy
from .form import ProductoCreate, PedidoCreate, PedidoDetalleCreate, PedidoUpdate, PedidoView, ConsultaCreate, TurnosCreate, Paciente_Form
from .models import Producto, Paciente, Consulta, Pedido, PedidoDetalle, Turnos, User
from .form import ProductoCreate, PedidoCreate, PedidoDetalleCreate, PedidoUpdate, PedidoView, ConsultaCreate, TurnosCreate
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django import forms

import django_filters
from .filters import TurnosFilter
import datetime

# from .models import Turnos
# from .form import TurnosCreate

# Create your views here.
def index(request):
    #De acuerdo al perfil debemos redeireccionarlo
    return render(request, "index.html")


def productos(request):
    return render(request, "productos.html", {
        "productos": Producto.objects.all()
    })

def producto(request, producto_id):
        unProducto = Producto.objects.get(id=producto_id)
        return render(request, "producto.html",{
            "producto": unProducto
        })

def agregar(request):
    upload  = ProductoCreate()
    if request.method == 'POST':
        upload = ProductoCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('clinica:productos')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'clinica:productos'}}">reload</a>""")
    else:
        return render(request, 'agregar.html', {'upload_form':upload})



def eliminar(request, producto_id):
    producto_id= int(producto_id)
    try:
        producto_sel = Producto.objects.get(id = producto_id)
        
    except Producto.DoesNotExist:
        return redirect('clinica:productos')
    producto_sel.delete()
    return render(request, "eliminar.html")



def actualizar(request, producto_id):
     producto_id = int(producto_id)
     try:
         producto_sel = Producto.objects.get(id = producto_id)
     except Producto.DoesNotExist:
         return redirect('index')
     producto_form = ProductoCreate(request.POST or None, instance = producto_sel)
     if producto_form.is_valid():
        producto_form.save()
        return redirect('clinica:productos')
     return render(request, 'agregar.html', {'upload_form':producto_form })

####################################################################################################
def turnos (request):
     return render(request, "turnos.html", {
        "turno": Turnos.objects.all()
    })
       

def crearTurno(request):
    upload  = TurnosCreate()
    if request.method == 'POST':
        upload = TurnosCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('clinica:turnos')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'clinica:turnos'}}">reload</a>""")
    else:
        return render(request, 'agregarturno.html', {'upload_form':upload})



def borrarTurno(request, turno_id):
    turno_id = int(turno_id)
    try:
        turno_elegido = Turnos.objects.get(id = turno_id)
        
    except Turnos.DoesNotExist:
        return redirect('clinica:turnos')
    turno_elegido.delete()
    return render(request, "eliminarturno.html")



def actualizarTurno(request, turno_id):
    turno_id = int(turno_id)
    try:
        turno_elegido = Producto.objects.get(id = turno_id)
    except Turnos.DoesNotExist:
        return redirect('index')
    turno_form = TurnosCreate(request.POST or None, instance = turno_elegido)
    if turno_form.is_valid():
        turno_form.save()
        return redirect('clinica:turnos')
    return render(request, 'actualizarturno.html', {'upload_form':turno_form })

#########################################################################################################

def pacientes(request):
#    usuario = {'usuario': request.User} 
# NO me deja pasar nunca igual...
#    if not usuario==True:
# Aca hay un problema con la url del httpresponse para volver a loguearse si no es medico
#        return HttpResponse("""Usted no es medico. Si lo es vuelva a <a href = " {{ url : 'usuarios:loguin'}}">loguearse</a> loguearse""")
    return render(request, "pacientes.html", {
        "pacientes": Paciente.objects.all()
    })

def historial(request, paciente_id):
# habria q agregar un if 
    paciente = Paciente.objects.get(id=paciente_id)
    consultasTotales = Consulta.objects.all()
    consultas = consultasTotales.filter(paciente_id=paciente_id)
    return render(request, "historial.html",{
        "consultas": consultas,
        "paciente": paciente,
    })

def agregar_consulta(request):
    upload  = ConsultaCreate()
    if request.method == 'POST':
        upload = ConsultaCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('clinica:pacientes')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'clinica:pacientes' }}" >Recargar</a>""")
    else:
        return render(request, 'agregar_consulta.html', {'upload_form':upload})

def eliminar_consulta(request, consulta_id):
    consulta_id= int(consulta_id)
    try:
        consulta_sel = Consulta.objects.get(id = consulta_id)
        
    except Consulta.DoesNotExist:
        return redirect('clinica:pacientes')
    consulta_sel.delete()
    return render(request, "eliminar_consulta.html")

def modificar_consulta(request, consulta_id):
     consulta_id = int(consulta_id)
     try:
         consulta_sel = Consulta.objects.get(id = consulta_id)
     except Consulta.DoesNotExist:
         return redirect('pacientes')
     consulta_form = ConsultaCreate(request.POST or None, instance = consulta_sel)
     if consulta_form.is_valid():
        consulta_form.save()
        return redirect('clinica:pacientes')
     return render(request, 'agregar_consulta.html', {'upload_form':consulta_form })

def pedidos(request):
    if request.user.es_ventas:
        return render(request, "pedidos.html", {
            "pedidos": Pedido.objects.filter(vendedor=request.user).order_by('-id')
        })
    if request.user.es_taller:
        return render(request, "pedidos.html", {
            "pedidos": Pedido.objects.filter(estado='PT').order_by('-id')
        })

def pedido(request, pedido_id):    
    unPedido = Pedido.objects.get(id=pedido_id)
    return render(request, "pedido.html",{
        "pedido": unPedido
    })

def agregar_pedido(request):
    #instanciar la fecha actual
    # upload = PedidoCreate(initial={'estado': 'PT','vendedor': request.user})
    upload = PedidoCreate()
    # upload.vendedor = request.user
    # upload.fields['vendedor'].disabled = True
    # upload.estado = 'PT'
    if request.method == 'POST':
        upload = PedidoCreate(request.POST, request.FILES)
        if upload.is_valid():
            f = upload.save(commit=False)
            f.vendedor = request.user
            f.fecha = datetime.datetime.now()
            f.subtotal = 0
            f.estado = 'PT'
            f.save()
            # pedido = Pedido.objects.last()
            return redirect('clinica:detalle_pedido', f.id)
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'clinica:pedidos'}}">reload</a>""")
    else:
        return render(request, 'agregar_pedido.html', {'upload_form':upload})

def eliminar_pedido(request, pedido_id):
    pedido_id= int(pedido_id)
    try:
        pedido_sel = Pedido.objects.get(id = pedido_id)
        
    except Pedido.DoesNotExist:
        return redirect('clinica:pedidos')
    pedido_sel.delete()
    # return render(request, "eliminar_pedido.html")
    return redirect('clinica:pedidos')

def actualizar_pedido(request, pedido_id):
     pedido_id = int(pedido_id)
     try:
         pedido_sel = Pedido.objects.get(id = pedido_id)
     except Pedido.DoesNotExist:
         return redirect('index')
     pedido_form = ProductoCreate(request.POST or None, instance = pedido_sel)
     if pedido_form.is_valid():
        pedido_form.save()
        return redirect('clinica:pedidos')
     return render(request, 'agregar.html', {'upload_form':pedido_form })
        
def pedido_items(request, pedido_id):
     unPedido = Pedido.objects.get(id=pedido_id)
     items = PedidoDetalle.objects.filter(pedido_id=unPedido.id)
     f = formAgregarProducto()
     return render(request, 'pedido_items.html', {'pedido':unPedido, 'items':items, 'form':f})

def agregar_item(request, pedido_id):
    unPedido = Pedido.objects.get(id=pedido_id)
    upload  = PedidoDetalleCreate(instance=unPedido)
    # upload.initial['pedido_id'] = 4
    if request.method == 'POST':
        upload = PedidoDetalleCreate(request.POST, request.FILES)
        if upload.is_valid():
            
            upload.save()
            return redirect('clinica:pedidos')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'clinica:pedidos'}}">reload</a>""")
    else:
        f=formAgregarProducto();
        return render(request, 'agregar_item.html', {'upload_form':upload})

#  viaje de seba con los generic views 
class TurnosListView(generic.ListView):
    model = Turnos

    def get_queryset(self):
        qs = self.model.objects.all()
        turnos_filtered_list = TurnosFilter(self.request.GET, queryset=qs)
        return turnos_filtered_list.qs

class TurnoDetailView(generic.DetailView):
    model = Turnos
    context_object_name= 'turnos'
    queryset= Turnos.objects.all()

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context["turnos_list"] = Turnos.objects.all()
#        return context
    
    def get_object(self):
        turno= super().get_object()
        turno.save()
        return turno
    

class TurnoCreate(CreateView):
    model = Turnos
    fields = ['Paciente', 'HoraTurno', 'FechaTurno', 'Asistencia']
    
    def get_form(self):
        form = super().get_form()
        form.fields['FechaTurno'].widget = DatePickerInput(format='%d/%m/%Y')
        form.fields['HoraTurno'].widget = TimePickerInput()
        return form
    

class TurnoUpdate(UpdateView):
    model = Turnos
    fields = ['Paciente', 'HoraTurno', 'FechaTurno', 'Asistencia']

class TurnoDelete(DeleteView):
    model = Turnos
    success_url = reverse_lazy('clinica:turnos')

def turnos_reporte(request):
    filter = TurnosFilter(request.GET, queryset=Turnos.objects.all())
    return render(request, 'clinica/turnos-reporte.html', {'filter': filter})

class formAgregarProducto(forms.Form):
    cantidad = forms.IntegerField(label="Cantidad")
    

def detalle_pedido(request, pedido_id):
    unPedido = Pedido.objects.get(id=pedido_id)
    # formPedido = PedidoView(instance=unPedido)
    # if (request.user.is_authenticated):
    #     formPedido.fields['estado'].disabled = False
    items = PedidoDetalle.objects.filter(pedido_id=unPedido.id).order_by('-id')
    #hay que obtener sólo los productos que no están en el pedido
    productos_disponibles = Producto.objects.all()
    # return render(request, 'pedido_items.html', {'pedido': unPedido, 'items': items, 'productos_disponibles': productos_disponibles,'formPedido': formPedido})
    return render(request, 'pedido_items.html', {'pedido': unPedido, 'items': items, 'productos_disponibles': productos_disponibles})
     
def agregar_producto(request, pedido_id):
    unPedido = Pedido.objects.get(id=pedido_id)
    # formPedido = PedidoView(instance=unPedido)
    # if (request.user.is_authenticated and request.user.es_vendedor()):
    # formPedido.fields['estado'].disabled = False

    detalle_item = PedidoDetalle()
    detalle_item.pedido = unPedido    
    
    if request.method == 'POST':
        producto = Producto.objects.get(id=int(request.POST["productos"]))
        detalle_item.producto = producto
        detalle_item.cantidad = int(request.POST["cantidad"])
        detalle_item.total = round(detalle_item.cantidad * producto.precio, 2)
        # creo que necesitamos commit false hasta que el pedido se actualice el precio?
        detalle = detalle_item.save()
        # actualizar unPedido.subtotal+detalle_item.total el total del pedido y guardar
        unPedido.subtotal = float(unPedido.subtotal) + round(detalle_item.total, 2)
        # unPedido.estado = request.POST["estado"]
        unPedido.save()
        # formPedido = PedidoView(instance=unPedido)
        # formPedido.fields['estado'].disabled = False
        items = PedidoDetalle.objects.filter(pedido_id=unPedido.id).order_by('-id')
        #hay que obtener sólo los productos que no están en el pedido
        productos_disponibles = Producto.objects.all()
        # return render(request, 'pedido_items.html', {'pedido': unPedido, 'items': items, 'productos_disponibles': productos_disponibles,'formPedido': formPedido})
        return HttpResponseRedirect(reverse("clinica:detalle_pedido", args=(pedido_id,)))
        # return render(request, 'pedido_items.html', {'pedido': unPedido, 'items': items, 'productos_disponibles': productos_disponibles})
    else:
        return render(request, 'pedido_items.html', {'pedido': unPedido, 'items': items, 'productos_disponibles': productos_disponibles})

class PacienteCreate(generic.CreateView): 
    model = Paciente
    fields = ['nombre', 'apellido', 'direccion', 'telefono', 'email',]


class PacienteUpdate(generic.UpdateView):
    model = Paciente
    fields = [
        'nombre',
        'apellido',
        'direccion',
        'telefono',
        'email',
    ]

class PacienteDelete(generic.DeleteView):
    model = Paciente
    success_url = reverse_lazy('clinica:pacientes')
    
def eliminar_producto(request, detalle_pedido_id):
    detalle = PedidoDetalle.objects.get(id=int(detalle_pedido_id))
    unPedido = Pedido.objects.get(id=detalle.pedido.id)
    unPedido.subtotal = float(unPedido.subtotal) - float(round(detalle.total, 2))
    unPedido.save()
    detalle.delete()
    productos_disponibles = Producto.objects.all()
    items = PedidoDetalle.objects.filter(pedido_id=unPedido.id).order_by('-id')
    return render(request, 'pedido_items.html', {'pedido': unPedido, 'items': items, 'productos_disponibles': productos_disponibles})



# def add(request):
#     # Creamos un formulario vacío
#     form = PersonaForm()

#     # Comprobamos si se ha enviado el formulario
#     if request.method == "POST":
#         # Añadimos los datos recibidos al formulario
#         form = PersonaForm(request.POST)
#         # Si el formulario es válido...
#         if form.is_valid():
#             # Guardamos el formulario pero sin confirmarlo,
#             # así conseguiremos una instancia para manejarla
#             instancia = form.save(commit=False)
#             # Podemos guardarla cuando queramos
#             instancia.save()
#             # Después de guardar redireccionamos a la lista
#             return redirect('/')

#     # Si llegamos al final renderizamos el formulario
#     return render(request, "core/add.html", {'form': form})

# def edit(request, persona_id):
#     # Recuperamos la instancia de la persona
#     instancia = Persona.objects.get(id=persona_id)

#     # Creamos el formulario con los datos de la instancia
#     form = PersonaForm(instance=instancia)

#     # Comprobamos si se ha enviado el formulario
#     if request.method == "POST":
#         # Actualizamos el formulario con los datos recibidos
#         form = PersonaForm(request.POST, instance=instancia)
#         # Si el formulario es válido...
#         if form.is_valid():
#             # Guardamos el formulario pero sin confirmarlo,
#             # así conseguiremos una instancia para manejarla
#             instancia = form.save(commit=False)
#             # Podemos guardarla cuando queramos
#             instancia.save()

#     # Si llegamos al final renderizamos el formulario
#     return render(request, "core/edit.html", {'form': form})

# def delete(request, persona_id):
#     # Recuperamos la instancia de la persona y la borramos
#     instancia = Persona.objects.get(id=persona_id)
#     instancia.delete()

#     # Después redireccionamos de nuevo a la lista
#     return redirect('/')

# <ul>
#     {% for persona in personas %}
#     <li>
#         {{ persona.nombre }}, {{ persona.edad }} años
#         <a href="/edit/{{ persona.id }}">Editar</a>
#         <a href="/delete/{{ persona.id }}" 
#           onClick="return confirm('¿Seguro que quieres borrar a {{persona.nombre}}?');">
#             Borrar
#         </a>
#     </li>
#     {% endfor %}
# </ul>


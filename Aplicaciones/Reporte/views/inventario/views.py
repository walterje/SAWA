from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import TemplateView
from Aplicaciones.Reporte.forms import *
from Aplicaciones.Producto.models import *

from django.db.models.functions import Coalesce
from django.db.models import Sum

class ReporteInventarioView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/reporte.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data =[]
                start_date = request.POST.get('start_date','')
                end_date = request.POST.get('end_date','')#si no encuentra valor con post le asignamos vacio
                search = MovimientoStock.objects.all()
                #obtengo todos los datos de mi orden de Compra 
                if len(start_date) and len(end_date):#si  el rango tiene valor
                    search = search.filter(fecha_mov__range=[start_date, end_date])
                for i in search:
                    print(i.producto.tipo_producto)
                    data.append([
                        i.id,
                        i.fecha_mov.strftime('%Y-%m-%d'),
                        i.producto.nombre_producto,
                        i.producto.cant_stock,
                        i.descripcion,
                        format(i.cant_mov, '.0f'),
                    ])
                cant_mov = search.aggregate(r=Coalesce(Sum('cant_mov'), 0)).get('r')
                data.append([
                    ' ',
                    ' ',
                    ' ',
                    ' ',
                    ' ',
                    format(cant_mov, '.0f'),
                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Movimiento Inventario'
        context['entity'] = 'Reporte'
        context['list_url'] = reverse_lazy('Reporte:inventario_reporte')
        context['form'] = ReporteForm()
        return context


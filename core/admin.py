
from django.contrib import admin
from .models import Evento, Categoria, Inscripcion
import locale

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'fecha_inscripcion')
    list_filter = ('evento',)
    search_fields = ('usuario__username', 'evento__titulo')


class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 0
    readonly_fields = ('usuario', 'fecha_inscripcion')
    can_delete = False
    verbose_name = "Asistente"
    verbose_name_plural = "Listado de Asistentes"

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    
    
    list_display = (
        'titulo', 
        'fecha_hora', 
        'plazas_info',        
        'dinero_recaudado',    
        'dinero_potencial'     
    )
    
    search_fields = ('titulo', 'lugar')
    list_filter = ('fecha_hora', 'categoria')
    inlines = [InscripcionInline]

  
    def plazas_info(self, obj):
        inscritos_count = obj.inscritos.count()
        total_plazas = inscritos_count + obj.plazas_disponibles
        return f'{obj.plazas_disponibles} libres de {total_plazas}'
    plazas_info.short_description = 'Plazas Disponibles'

    
    def _format_currency(self, amount):
        try:
       
            locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
        except locale.Error:
         
            locale.setlocale(locale.LC_ALL, '') 
        
        return locale.currency(amount, grouping=True, symbol='$')


    def dinero_recaudado(self, obj):
        inscritos_count = obj.inscritos.count()
        recaudacion = inscritos_count * obj.valor
        return self._format_currency(recaudacion)
    dinero_recaudado.short_description = 'Recaudado (Actual)'

  
   
    def dinero_potencial(self, obj):
        inscritos_count = obj.inscritos.count()
        total_plazas = inscritos_count + obj.plazas_disponibles
        potencial = total_plazas * obj.valor
        return self._format_currency(potencial)
    dinero_potencial.short_description = 'Potencial (Total)'
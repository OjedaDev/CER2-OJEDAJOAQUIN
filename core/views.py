
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Evento, Inscripcion
from django.db import transaction 
from django.contrib.auth.models import User
from django.utils import timezone


def index(request):

    now = timezone.now()

    eventos_list = Evento.objects.filter(
        plazas_disponibles__gt=0,
        fecha_hora__gt=now  
    ).order_by('fecha_hora')


    eventos_list = Evento.objects.filter(plazas_disponibles__gt=0).order_by('fecha_hora')

    otros_eventos = eventos_list
    
    featured_evento = eventos_list.first() 

    eventos_totales = Evento.objects.count()
    usuarios_registrados = User.objects.count()
    inscripciones_totales = Inscripcion.objects.count()

    context = {
        'featured_evento': featured_evento, 
        'otros_eventos': otros_eventos,     
        'stats_eventos': eventos_totales,
        'stats_usuarios': usuarios_registrados,
        'stats_inscripciones': inscripciones_totales,
    }
    return render(request, 'core/index.html', context)


def evento_detalle(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    ya_inscrito = False
    if request.user.is_authenticated:
        ya_inscrito = Inscripcion.objects.filter(usuario=request.user, evento=evento).exists()

    evento_finalizado = evento.fecha_hora < timezone.now()
    context = {
        'evento': evento,
        'ya_inscrito': ya_inscrito,
        'evento_finalizado': evento_finalizado 
    }

    return render(request, 'core/evento_detalle.html', {
        'evento': evento,
        'ya_inscrito': ya_inscrito
    })


@login_required
@transaction.atomic
def inscribir_evento(request, evento_id):
    if request.method == 'POST':
        evento = get_object_or_404(Evento, id=evento_id)
        
        if evento.fecha_hora < timezone.now():
            messages.error(request, 'Este evento ya ha finalizado. No puedes inscribirte.')
            return redirect('evento_detalle', evento_id=evento.id)
        
        if Inscripcion.objects.filter(usuario=request.user, evento=evento).exists():
            messages.warning(request, 'Ya estás inscrito en este evento.')
            return redirect('evento_detalle', evento_id=evento.id)
            
        
        if evento.plazas_disponibles <= 0:
            messages.error(request, 'No quedan plazas disponibles.')
            return redirect('evento_detalle', evento_id=evento.id)
            
        
        Inscripcion.objects.create(usuario=request.user, evento=evento)
        evento.plazas_disponibles -= 1
        evento.save()
        
        messages.success(request, f'¡Inscripción exitosa en {evento.titulo}!')
        return redirect('mis_eventos')
    return redirect('index')


@login_required
def mis_eventos(request):
    inscripciones = Inscripcion.objects.filter(usuario=request.user).order_by('evento__fecha_hora')
    return render(request, 'core/mis_eventos.html', {'inscripciones': inscripciones})

@login_required
@transaction.atomic
def anular_inscripcion(request, inscripcion_id):
    if request.method == 'POST':
        inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id, usuario=request.user)
        evento = inscripcion.evento
        

        evento.plazas_disponibles += 1
        evento.save()
        

        inscripcion.delete()
        
        messages.success(request, f'Has anulado tu inscripción para {evento.titulo}.')
    return redirect('mis_eventos')
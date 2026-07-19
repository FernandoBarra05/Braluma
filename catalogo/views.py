from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.utils import timezone
from django.conf import settings
import urllib.parse
from datetime import timedelta
import json

from .models import Espejo, Categoria, Lead, ImagenProducto, ConfiguracionHero

def home_narrative_view(request):
    """Página principal (Home / /): Narrativa de marca estilo Apple en 5 actos, sin precios ni grilla de productos."""
    hero_config = ConfiguracionHero.objects.filter(activo=True).first()
    destacados = Espejo.objects.filter(activo=True, destacado=True).prefetch_related('imagenes')[:3]

    context = {
        'hero_config': hero_config,
        'destacados': destacados,
    }
    return render(request, 'catalogo/home.html', context)


def coleccion_catalog_view(request):
    """Página de colección y tienda (/coleccion/): Grilla de productos con filtros, precios y fichas técnicas."""
    forma_filter = request.GET.get('forma', '')
    
    espejos = Espejo.objects.filter(activo=True).prefetch_related('imagenes')
    
    if forma_filter in dict(Espejo.FORMA_CHOICES):
        espejos = espejos.filter(forma=forma_filter)

    context = {
        'espejos': espejos,
        'forma_actual': forma_filter,
        'formas': Espejo.FORMA_CHOICES,
    }
    return render(request, 'catalogo/coleccion.html', context)


def product_detail_view(request, slug):
    """Ficha técnica de producto (/espejo/<slug>/), dial de Kelvin y captura de lead a WhatsApp."""
    espejo = get_object_or_404(Espejo, slug=slug, activo=True)
    imagenes = espejo.imagenes.order_by('orden')

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        email = request.POST.get('email', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()

        if nombre and telefono:
            # Guardar el lead en base de datos antes de redirigir
            Lead.objects.create(
                nombre=nombre,
                telefono=telefono,
                email=email if email else None,
                espejo_interes=espejo,
                mensaje=mensaje,
                canal='whatsapp',
                estado='nuevo'
            )

            # Construir mensaje precargado para WhatsApp
            mensaje_wa = (
                f"¡Hola Braluma! Mi nombre es {nombre}.\n"
                f"Me interesa cotizar el espejo LED: *{espejo.nombre}* "
                f"({espejo.ancho_cm}x{espejo.alto_cm} cm).\n"
            )
            if mensaje:
                mensaje_wa += f"Mensaje adicional: {mensaje}\n"
            
            mensaje_wa += "Quedo atento a su respuesta. ¡Gracias!"

            texto_encoded = urllib.parse.quote(mensaje_wa)
            wa_number = getattr(settings, 'WHATSAPP_NUMBER', '51924280775')
            wa_url = f"https://wa.me/{wa_number}?text={texto_encoded}"
            
            return redirect(wa_url)

    context = {
        'espejo': espejo,
        'imagenes': imagenes,
        'whatsapp_num': getattr(settings, 'WHATSAPP_NUMBER', '51924280775'),
    }
    return render(request, 'catalogo/detail.html', context)


@staff_member_required
def dashboard_metricas_view(request):
    """Dashboard de analítica interna para el equipo de Braluma (solo staff)."""
    now = timezone.now()
    
    # KPIs principales
    total_leads = Lead.objects.count()
    leads_nuevos = Lead.objects.filter(estado='nuevo').count()
    productos_activos = Espejo.objects.filter(activo=True).count()
    
    # Métricas de leads por semana (últimas 8 semanas)
    semanas_labels = []
    semanas_data = []
    
    for i in range(7, -1, -1):
        inicio_semana = now - timedelta(days=(i+1)*7)
        fin_semana = now - timedelta(days=i*7)
        
        label = f"Sem {-i if i > 0 else 'Actual'}"
        if i == 0:
            label = "Esta Sem."
        else:
            label = f"Hace {i} sem"
            
        count = Lead.objects.filter(creado_en__gte=inicio_semana, creado_en__lt=fin_semana).count()
        semanas_labels.append(label)
        semanas_data.append(count)

    # Espejos más consultados (Top 5 por cantidad de leads)
    top_espejos_qs = Espejo.objects.annotate(num_leads=Count('leads')).order_by('-num_leads')[:5]
    top_espejos_labels = [e.nombre for e in top_espejos_qs]
    top_espejos_data = [e.num_leads for e in top_espejos_qs]

    context = {
        'total_leads': total_leads,
        'leads_nuevos': leads_nuevos,
        'productos_activos': productos_activos,
        'semanas_labels_json': json.dumps(semanas_labels),
        'semanas_data_json': json.dumps(semanas_data),
        'top_espejos_labels_json': json.dumps(top_espejos_labels),
        'top_espejos_data_json': json.dumps(top_espejos_data),
    }
    return render(request, 'dashboard/metricas.html', context)

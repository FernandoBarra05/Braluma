from django.contrib import admin
from django.utils.html import mark_safe
from .models import Categoria, Espejo, ImagenProducto, Lead, ConfiguracionHero

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1
    fields = ('imagen', 'vista_previa', 'alt_text', 'orden')
    readonly_fields = ('vista_previa',)

    def vista_previa(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" style="max-height: 70px; max-width: 100px; border-radius: 4px; object-fit: cover;" />')
        return "(Sin imagen)"
    vista_previa.short_description = "Vista previa"


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Espejo)
class EspejoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'forma', 'precio', 'stock', 'activo', 'destacado', 'vista_miniatura')
    list_editable = ('precio', 'stock', 'activo', 'destacado')
    list_filter = ('categoria', 'forma', 'activo', 'destacado', 'regulable', 'antivaho')
    search_fields = ('nombre', 'descripcion')
    prepopulated_fields = {'slug': ('nombre',)}
    inlines = [ImagenProductoInline]
    list_per_page = 20

    def vista_miniatura(self, obj):
        img_url = obj.primera_imagen
        if img_url:
            return mark_safe(f'<img src="{img_url}" style="height: 40px; width: 40px; border-radius: 50%; object-fit: cover; border: 1px solid #ffb066;" />')
        return mark_safe('<span style="color:#999;">Sin foto</span>')
    vista_miniatura.short_description = "Imagen"


@admin.action(description="Marcar leads seleccionados como 'Contactado'")
def marcar_como_contactado(modeladmin, request, queryset):
    updated = queryset.update(estado='contactado')
    modeladmin.message_user(request, f"{updated} lead(s) fueron marcados como 'Contactado'.")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email', 'espejo_interes', 'canal', 'estado_badge', 'creado_en')
    list_filter = ('estado', 'canal', 'creado_en')
    search_fields = ('nombre', 'telefono', 'email', 'mensaje')
    actions = [marcar_como_contactado]
    readonly_fields = ('creado_en', 'actualizado_en')
    list_per_page = 25

    def estado_badge(self, obj):
        colors = {
            'nuevo': '#e67e22',
            'contactado': '#2980b9',
            'cerrado': '#27ae60',
        }
        color = colors.get(obj.estado, '#7f8c8d')
        return mark_safe(f'<span style="background-color: {color}; color: #fff; padding: 4px 8px; border-radius: 12px; font-weight: bold; font-size: 11px;">{obj.get_estado_display()}</span>')
    estado_badge.short_description = "Estado"


@admin.register(ConfiguracionHero)
class ConfiguracionHeroAdmin(admin.ModelAdmin):
    list_display = ('titulo_principal', 'activo', 'posicion_imagen', 'vista_previa_hero')
    list_editable = ('activo', 'posicion_imagen')
    readonly_fields = ('vista_previa_hero', 'guia_tamano_imagen')
    
    fieldsets = (
        ("📌 Especificaciones de Contenido y Formato del Hero", {
            'fields': ('guia_tamano_imagen', 'vista_previa_hero'),
            'description': 'Información sobre el recorte circular automático y proporciones óptimas.'
        }),
        ("🖼️ Archivo de Imagen & Encuadre", {
            'fields': ('imagen_hero', 'posicion_imagen'),
        }),
        ("✏️ Textos de Portada", {
            'fields': ('titulo_eyebrow', 'titulo_principal', 'subtitulo', 'espejo_vinculado', 'activo'),
        }),
    )

    def vista_previa_hero(self, obj):
        img_url = obj.get_imagen_url
        return mark_safe(
            f'<div style="background: #111318; padding: 12px; border-radius: 10px; display: inline-block; border: 1px solid #ffb066; text-align: center;">'
            f'<img src="{img_url}" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; object-position: {obj.posicion_imagen}; border: 2px solid #ffb066; box-shadow: 0 0 15px rgba(255, 176, 102, 0.4);" />'
            f'<br/><small style="color: #ffb066; font-size: 11px; margin-top: 6px; display: block;">Recorte circular automático (1:1)</small>'
            f'</div>'
        )
    vista_previa_hero.short_description = "Vista Previa en Admin"

    def guia_tamano_imagen(self, obj):
        return mark_safe(
            '<div style="background: #1a1d24; color: #eae6de; padding: 15px; border-left: 4px solid #ffb066; border-radius: 6px; font-size: 13px; line-height: 1.6;">'
            '<h4 style="margin: 0 0 8px 0; color: #ffb066; font-size: 14px;">📐 Recomendaciones para la Imagen del Hero:</h4>'
            '<ul>'
            '<li><strong>Proporción recomendada:</strong> Cuadrada 1:1, resolución mínima <strong>1200 × 1200 px</strong> con el espejo centrado.</li>'
            '<li><strong>Recorte inteligente:</strong> El sistema aplica automáticamente un contenedor circular con <code>object-fit: cover</code> para garantizar que cualquier foto (horizontal o vertical) se adapte perfectamente sin deformarse.</li>'
            '<li><strong>Imagen por defecto:</strong> Si no subes un archivo, el sistema utilizará la fotografía realista oficial de Braluma.</li>'
            '</ul>'
            '</div>'
        )
    guia_tamano_imagen.short_description = "Guía Técnica"

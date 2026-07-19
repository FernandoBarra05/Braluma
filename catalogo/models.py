from django.db import models
from django.utils.text import slugify

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=120)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Espejo(models.Model):
    FORMA_CHOICES = [
        ('redondo', 'Redondo'),
        ('ovalado', 'Ovalado'),
        ('rectangular', 'Rectangular'),
        ('arco', 'Arco'),
    ]

    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='espejos')
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True, help_text="Visibilidad en el catálogo público")
    destacado = models.BooleanField(default=False, help_text="Destacar en catálogo / portada")
    forma = models.CharField(max_length=20, choices=FORMA_CHOICES, default='redondo')
    
    # Temperatura LED en Kelvin (ej. 2700K a 6500K)
    temperatura_min_k = models.PositiveIntegerField(default=3000, help_text="Temperatura mínima en Kelvin (ej. 2700)")
    temperatura_max_k = models.PositiveIntegerField(default=6500, help_text="Temperatura máxima en Kelvin (ej. 6500)")
    
    regulable = models.BooleanField(default=True, verbose_name="Luz Regulable / Dimmable")
    antivaho = models.BooleanField(default=False, verbose_name="Sistema Antivaho Integrated")
    ancho_cm = models.PositiveIntegerField(help_text="Ancho en centímetros")
    alto_cm = models.PositiveIntegerField(help_text="Alto en centímetros")
    stock = models.PositiveIntegerField(default=10)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Espejo"
        verbose_name_plural = "Espejos"
        ordering = ['-destacado', '-creado_en']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    @property
    def primera_imagen(self):
        img = self.imagenes.order_by('orden').first()
        return img.imagen.url if img else None


class ImagenProducto(models.Model):
    espejo = models.ForeignKey(Espejo, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/')
    alt_text = models.CharField(max_length=200, blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Imagen de Producto"
        verbose_name_plural = "Imágenes de Producto"
        ordering = ['orden', 'id']

    def __str__(self):
        return f"Imagen #{self.orden} de {self.espejo.nombre}"


class Lead(models.Model):
    CANAL_CHOICES = [
        ('formulario', 'Formulario Web'),
        ('whatsapp', 'WhatsApp'),
    ]

    ESTADO_CHOICES = [
        ('nuevo', 'Nuevo'),
        ('contactado', 'Contactado'),
        ('cerrado', 'Cerrado'),
    ]

    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    espejo_interes = models.ForeignKey(Espejo, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads', verbose_name="Espejo de Interés")
    mensaje = models.TextField(blank=True)
    canal = models.CharField(max_length=20, choices=CANAL_CHOICES, default='formulario')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='nuevo')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lead / Interesado"
        verbose_name_plural = "Leads / Interesados"
        ordering = ['-creado_en']

    def __str__(self):
        espejo_str = f" - {self.espejo_interes.nombre}" if self.espejo_interes else ""
        return f"{self.nombre} ({self.telefono}){espejo_str}"


class ConfiguracionHero(models.Model):
    POSICION_CHOICES = [
        ('center center', 'Centrado perfecto (Center Center)'),
        ('top center', 'Alineado arriba (Top Center)'),
        ('bottom center', 'Alineado abajo (Bottom Center)'),
        ('center left', 'Alineado izquierda (Center Left)'),
        ('center right', 'Alineado derecha (Center Right)'),
    ]

    titulo_eyebrow = models.CharField(
        max_length=150, 
        default="ILUMINACIÓN ARQUITECTÓNICA & TECNOLOGÍA",
        verbose_name="Texto pequeño superior (Eyebrow)"
    )
    titulo_principal = models.CharField(
        max_length=200, 
        default="La Luz que Enciende tu Espacio",
        verbose_name="Título del Hero"
    )
    subtitulo = models.TextField(
        default="Espejos de diseño superior con iluminación LED perimetral integrada, dial de temperatura Kelvin regulable y cristal con defroster antivaho.",
        verbose_name="Subtítulo descriptivo"
    )
    imagen_hero = models.ImageField(
        upload_to='hero/', 
        blank=True, 
        null=True, 
        verbose_name="Imagen del Espejo Hero",
        help_text="📸 Sube una imagen cuadrada, mínimo 1200x1200px, con el espejo centrado — se recorta automáticamente en círculo con object-fit: cover para mantener la proporción perfecta."
    )
    posicion_imagen = models.CharField(
        max_length=30, 
        choices=POSICION_CHOICES, 
        default='center center',
        verbose_name="Punto Focal (Object-Position)",
        help_text="Ajusta el punto focal si la imagen cargada requiere un descentrado sutil."
    )
    espejo_vinculado = models.ForeignKey(
        Espejo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Espejo Vinculado (Opcional)",
        help_text="Vincular a la ficha técnica de un espejo del catálogo"
    )
    activo = models.BooleanField(default=True, verbose_name="Hero Activo en Portada")

    class Meta:
        verbose_name = "Configuración del Hero Parallax"
        verbose_name_plural = "Configuraciones del Hero Parallax"

    def __str__(self):
        return f"Configuración Hero Parallax: {self.titulo_principal}"

    @property
    def get_imagen_url(self):
        if self.imagen_hero:
            return self.imagen_hero.url
        return '/static/images/default_hero_mirror.jpg'

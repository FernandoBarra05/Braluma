import os
import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.base import ContentFile
from django.utils.text import slugify

from catalogo.models import Categoria, Espejo, ImagenProducto, Lead, ConfiguracionHero

class Command(BaseCommand):
    help = 'Poblar la base de datos de Braluma con imágenes hiperrealistas comerciales'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("[Braluma] Asignando fotografías hiperrealistas comerciales..."))

        # 1. Crear Superusuario
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@braluma.com', 'admin123')

        # 2. Categorías
        cat_bano, _ = Categoria.objects.get_or_create(nombre="Espejos para Bano", slug="espejos-para-bano")
        cat_vestidor, _ = Categoria.objects.get_or_create(nombre="Espejos de Vestidor", slug="espejos-de-vestidor")
        cat_recibidor, _ = Categoria.objects.get_or_create(nombre="Espejos de Recibidor", slug="espejos-de-recibidor")
        cat_vanidad, _ = Categoria.objects.get_or_create(nombre="Espejos Vanidad", slug="espejos-vanidad")

        # 3. Productos con fotos dedicadas
        espejos_data = [
            {
                "nombre": "Braluma Aura LED Circular",
                "categoria": cat_bano,
                "descripcion": "Espejo circular de diseno arquitectonico con resplandor posterior indirecto de 360 deg. Incorpora sensor tactil de encendido, regulacion de intensidad continua y sistema antivaho termico.",
                "precio": 890.00,
                "forma": "redondo",
                "temperatura_min_k": 2700,
                "temperatura_max_k": 6500,
                "regulable": True,
                "antivaho": True,
                "ancho_cm": 80,
                "alto_cm": 80,
                "destacado": True,
                "stock": 15,
                "img_rel": "productos/aura_redondo.png"
            },
            {
                "nombre": "Braluma Eclipse Oval Elegance",
                "categoria": cat_vanidad,
                "descripcion": "Elegante espejo ovalado vertical con marco de luz frontal diffuse y control touch de doble zona. Perfecto para tocadores y banos principales de alta gama.",
                "precio": 1150.00,
                "forma": "ovalado",
                "temperatura_min_k": 3000,
                "temperatura_max_k": 6000,
                "regulable": True,
                "antivaho": True,
                "ancho_cm": 60,
                "alto_cm": 100,
                "destacado": True,
                "stock": 8,
                "img_rel": "productos/eclipse_ovalado.png"
            },
            {
                "nombre": "Braluma Arch Light Medio Punto",
                "categoria": cat_recibidor,
                "descripcion": "Imponente espejo en forma de arco romano con perfil ultra-delgado en acabado grafito y tira LED periferica de alto indice de reproduccion cromatica.",
                "precio": 1350.00,
                "forma": "arco",
                "temperatura_min_k": 2700,
                "temperatura_max_k": 6500,
                "regulable": True,
                "antivaho": True,
                "ancho_cm": 70,
                "alto_cm": 120,
                "destacado": True,
                "stock": 6,
                "img_rel": "productos/arch_arco.png"
            },
            {
                "nombre": "Braluma Prisma Studio Rectangular",
                "categoria": cat_vestidor,
                "descripcion": "Espejo rectangular panoramico con iluminacion dual. Disenado para maxima claridad visual en espacios de vestidor o suites.",
                "precio": 980.00,
                "forma": "rectangular",
                "temperatura_min_k": 3500,
                "temperatura_max_k": 6500,
                "regulable": True,
                "antivaho": False,
                "ancho_cm": 120,
                "alto_cm": 70,
                "destacado": False,
                "stock": 12,
                "img_rel": "productos/prisma_rectangular.png"
            },
            {
                "nombre": "Braluma Halo Minimal 60",
                "categoria": cat_bano,
                "descripcion": "Compacto espejo redondo de 60cm con resplandor calido focalizado. Ideal para medios banos de visitas o ambientes modernos contemporaneos.",
                "precio": 650.00,
                "forma": "redondo",
                "temperatura_min_k": 3000,
                "temperatura_max_k": 5500,
                "regulable": True,
                "antivaho": False,
                "ancho_cm": 60,
                "alto_cm": 60,
                "destacado": False,
                "stock": 20,
                "img_rel": "productos/aura_redondo.png"
            },
            {
                "nombre": "Braluma Solis Oval Compact",
                "categoria": cat_vanidad,
                "descripcion": "Espejo ovalado estilizado con bordes biselados de alta precision y cinta LED integrada de larga duracion.",
                "precio": 820.00,
                "forma": "ovalado",
                "temperatura_min_k": 3000,
                "temperatura_max_k": 6500,
                "regulable": True,
                "antivaho": True,
                "ancho_cm": 50,
                "alto_cm": 90,
                "destacado": False,
                "stock": 10,
                "img_rel": "productos/eclipse_ovalado.png"
            }
        ]

        created_espejos = []
        for data in espejos_data:
            espejo, _ = Espejo.objects.get_or_create(
                nombre=data["nombre"],
                defaults={
                    "categoria": data["categoria"],
                    "descripcion": data["descripcion"],
                    "precio": data["precio"],
                    "forma": data["forma"],
                    "temperatura_min_k": data["temperatura_min_k"],
                    "temperatura_max_k": data["temperatura_max_k"],
                    "regulable": data["regulable"],
                    "antivaho": data["antivaho"],
                    "ancho_cm": data["ancho_cm"],
                    "alto_cm": data["alto_cm"],
                    "destacado": data["destacado"],
                    "stock": data["stock"],
                }
            )
            created_espejos.append(espejo)

            # Asignar fotografía hiperrealista dedicada
            ImagenProducto.objects.filter(espejo=espejo).delete()
            ImagenProducto.objects.create(
                espejo=espejo,
                imagen=data["img_rel"],
                alt_text=f"Fotografia comercial de {espejo.nombre}",
                orden=1
            )
            self.stdout.write(self.style.SUCCESS(f"Fotografia hiperrealista vinculada a {espejo.nombre}"))

        # 4. Configurar Hero con fotografía HD
        hero_conf, _ = ConfiguracionHero.objects.get_or_create(
            activo=True,
            defaults={
                "titulo_eyebrow": "ILUMINACIÓN ARQUITECTÓNICA",
                "titulo_principal": "La Luz que Enciende <em>tu Espacio</em>",
                "subtitulo": "Espejos de alta gama diseñados para proyectar luz continua de 360 grados con graduación Kelvin y tecnología antivaho.",
                "posicion_imagen": "center center",
                "espejo_vinculado": created_espejos[0]
            }
        )
        hero_conf.imagen_hero = "hero/aura_hero.png"
        hero_conf.save()

        # 5. Generar Leads Historicos
        nombres_prueba = ["Maria Fernandez", "Jorge Ugarte", "Lucia Benavides", "Gonzalo Ramirez", "Valeria Rios", "Diego Morales", "Ana Belen Castro", "Fernando Silva"]
        estados = ['nuevo', 'contactado', 'cerrado']
        canales = ['whatsapp', 'formulario']

        now = timezone.now()
        for idx in range(24):
            weeks_ago = random.randint(0, 7)
            created_date = now - timedelta(days=weeks_ago * 7 + random.randint(0, 6), hours=random.randint(1, 12))
            
            espejo_random = random.choice(created_espejos)
            nombre_person = random.choice(nombres_prueba)
            
            lead = Lead.objects.create(
                nombre=nombre_person,
                telefono=f"+51 987{random.randint(100000, 999999)}",
                email=f"{slugify(nombre_person)}@ejemplo.com",
                espejo_interes=espejo_random,
                mensaje=f"Hola, quisiera saber los tiempos de entrega para el modelo {espejo_random.nombre}.",
                canal=random.choice(canales),
                estado=random.choice(estados)
            )
            Lead.objects.filter(id=lead.id).update(creado_en=created_date)

        self.stdout.write(self.style.SUCCESS("[Braluma] ¡Imágenes hiperrealistas configuradas exitosamente!"))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',  # Nombre del servicio del contenedor de Docker
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'ecommerce',
#         'USER': 'postgres',
#         'PASSWORD': 'Player8744',
#     }
# }
import requests
from django.shortcuts import render

# Create your views here.

def get_total_usd(request):
    # obtener datos desde un rest api de terceras partes
    response = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')

    # convertir los datos de repuesta en formato json
    usuarios = response.json()
    return render(request, "core/usuarios.html", {'usuarios': usuarios})

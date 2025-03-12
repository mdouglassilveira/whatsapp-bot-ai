import folium
from geopy.geocoders import Nominatim
from time import sleep

# Lista de cidades (para melhorar a geolocalização, incluí "São Paulo, Brazil" em cada nome)
cities = [
    "Dumont, São Paulo, Brazil",
    "Pontal, São Paulo, Brazil",
    "Sertaozinho, São Paulo, Brazil",
    "Cravinhos, São Paulo, Brazil",
    "Luis Antonio, São Paulo, Brazil",
    "Santa Rita do Passa Quatro, São Paulo, Brazil",
    "Santa Rosa de Viterbo, São Paulo, Brazil",
    "São Simão, São Paulo, Brazil",
    "Americo Brasiliense, São Paulo, Brazil",
    "Araraquara, São Paulo, Brazil",
    "Boa Esperanca do Sul, São Paulo, Brazil",
    "Borborema, São Paulo, Brazil",
    "Candido Rodrigues, São Paulo, Brazil",
    "Dobrada, São Paulo, Brazil",
    "Gaviao Peixoto, São Paulo, Brazil",
    "Ibitinga, São Paulo, Brazil",
    "Itapolis, São Paulo, Brazil",
    "Matao, São Paulo, Brazil",
    "Motuca, São Paulo, Brazil",
    "Nova Europa, São Paulo, Brazil",
    "Rincao, São Paulo, Brazil",
    "Santa Lucia, São Paulo, Brazil",
    "Tabatinga, São Paulo, Brazil",
    "Taquaritinga, São Paulo, Brazil",
    "Trabiju, São Paulo, Brazil",
    "Barretos, São Paulo, Brazil",
    "Bebedouro, São Paulo, Brazil",
    "Cajobi, São Paulo, Brazil",
    "Colina, São Paulo, Brazil",
    "Colombia, São Paulo, Brazil",
    "Guaira, São Paulo, Brazil",
    "Guaraci, São Paulo, Brazil",
    "Jaborandi, São Paulo, Brazil",
    "Monte Azul Paulista, São Paulo, Brazil",
    "Olimpia, São Paulo, Brazil",
    "Severinia, São Paulo, Brazil",
    "Taiacu, São Paulo, Brazil",
    "Taiuva, São Paulo, Brazil",
    "Terra Roxa, São Paulo, Brazil",
    "Viradouro, São Paulo, Brazil",
    "Ariranha, São Paulo, Brazil",
    "Catanduva, São Paulo, Brazil",
    "Catigua, São Paulo, Brazil",
    "Elisiario, São Paulo, Brazil",
    "Embauba, São Paulo, Brazil",
    "Fernando Prestes, São Paulo, Brazil",
    "Itajobi, São Paulo, Brazil",
    "Marapoama, São Paulo, Brazil",
    "Novais, São Paulo, Brazil",
    "Palmares Paulista, São Paulo, Brazil",
    "Paraiso, São Paulo, Brazil",
    "Pindorama, São Paulo, Brazil",
    "Pirangi, São Paulo, Brazil",
    "Santa Adelia, São Paulo, Brazil",
    "Tabapua, São Paulo, Brazil",
    "Vista Alegre do Alto, São Paulo, Brazil"
]

# Cidades a serem destacadas (com cor diferente)
highlight = [
    "Araraquara, São Paulo, Brazil",
    "Sertaozinho, São Paulo, Brazil",
    "Catanduva, São Paulo, Brazil",
    "Barretos, São Paulo, Brazil"
]

# Inicializa o geolocalizador
geolocator = Nominatim(user_agent="mapa_sp")

# Cria o mapa centralizado em coordenadas aproximadas do estado de São Paulo
mapa = folium.Map(location=[-22.0, -49.0], zoom_start=7)

# Loop para geolocalizar cada cidade e adicionar o marcador ao mapa
for city in cities:
    try:
        location = geolocator.geocode(city)
        if location:
            # Se a cidade estiver na lista de destaque, usa marcador vermelho; caso contrário, azul
            color = 'red' if city in highlight else 'blue'
            folium.Marker(
                [location.latitude, location.longitude],
                popup=city,
                icon=folium.Icon(color=color)
            ).add_to(mapa)
            print(f"{city} localizada em ({location.latitude}, {location.longitude})")
        else:
            print(f"Localização não encontrada para: {city}")
        # Pausa para evitar sobrecarga no serviço de geocodificação
        sleep(1)
    except Exception as e:
        print(f"Erro ao buscar {city}: {e}")

# Salva o mapa em um arquivo HTML
mapa.save("mapa_sp.html")
print("Mapa salvo em 'mapa_sp.html'")

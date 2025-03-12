import geopandas as gpd
import matplotlib.pyplot as plt
import unidecode
import geobr

# 1) Ler shapefile dos municípios de SP via geobr
sp = geobr.read_municipality(code_muni='SP')

# 2) Lista de municípios (sem acentos, mas vamos normalizar de qualquer forma)
lista_cidades = [
    "Dumont", "Pontal", "Sertaozinho", "Cravinhos", "Luis Antonio",
    "Santa Rita do Passa Quatro", "Santa Rosa de Viterbo", "Sao Simao",
    "Americo Brasiliense", "Araraquara", "Boa Esperanca do Sul",
    "Borborema", "Candido Rodrigues", "Dobrada", "Gaviao Peixoto",
    "Ibitinga", "Itapolis", "Matao", "Motuca", "Nova Europa", "Rincao",
    "Santa Lucia", "Tabatinga", "Taquaritinga", "Trabiju", "Barretos",
    "Bebedouro", "Cajobi", "Colina", "Colombia", "Guaira", "Guaraci",
    "Jaborandi", "Monte Azul Paulista", "Olimpia", "Severinia", "Taiacu",
    "Taiuva", "Terra Roxa", "Viradouro", "Ariranha", "Catanduva", "Catigua",
    "Elisiario", "Embauba", "Fernando Prestes", "Itajobi", "Marapoama",
    "Novais", "Palmares Paulista", "Paraiso", "Pindorama", "Pirangi",
    "Santa Adelia", "Tabapua", "Vista Alegre do Alto"
]

# 3) Cidades de destaque
cidades_destaque = ["Araraquara", "Sertaozinho", "Catanduva", "Barretos"]

# Função para remover acentos e padronizar minúsculas
def normalizar(texto):
    return unidecode.unidecode(texto).lower().strip()

# Crie conjuntos (set) para comparar rapidamente
lista_normalizada = set(normalizar(c) for c in lista_cidades)
destaque_normalizada = set(normalizar(c) for c in cidades_destaque)

# 4) Normaliza o nome dos municípios no shapefile
sp["nome_normalizado"] = sp["name_muni"].apply(normalizar)

# Defina a cor de cada município
def definir_cor(nome_norm):
    if nome_norm in lista_normalizada:
        if nome_norm in destaque_normalizada:
            return "#FF5050"  # vermelho
        else:
            return "#3C8DFF"  # azul
    else:
        return "#DDDDDD"    # cinza claro (para municípios não listados)

sp["cor"] = sp["nome_normalizado"].apply(definir_cor)

# 5) Plotar todo o estado, mas com cores personalizadas
fig, ax = plt.subplots(figsize=(12, 8))
sp.plot(color=sp["cor"], edgecolor="white", linewidth=0.5, ax=ax)

# 6) Zoom automático para englobar somente a área dos municípios da lista
# Filtra o GeoDataFrame para apenas os municípios da lista
sp_in_list = sp[sp["nome_normalizado"].isin(lista_normalizada)]
# Calcula bounding box (xmin, ymin, xmax, ymax)
minx, miny, maxx, maxy = sp_in_list.total_bounds

# Define uma margem (10% do tamanho da área) para não ficar muito "apertado"
mx = (maxx - minx) * 0.1
my = (maxy - miny) * 0.1

ax.set_xlim(minx - mx, maxx + mx)
ax.set_ylim(miny - my, maxy + my)
ax.set_aspect('equal', 'box')

# 7) Anotar (rotular) apenas as cidades de destaque
for idx, row in sp_in_list.iterrows():
    if row["nome_normalizado"] in destaque_normalizada:
        centroid = row.geometry.centroid
        ax.annotate(
            text=row["name_muni"],        # Nome oficial do shapefile
            xy=(centroid.x, centroid.y),  # Coordenadas do centroide
            ha='center', va='center',
            fontsize=8, color='black',
            weight='bold'
        )

# Remove os eixos para um visual mais limpo
ax.set_axis_off()

# Salva o resultado
plt.savefig("mapa_zoom_destaque.png", dpi=200, bbox_inches="tight")
plt.show()

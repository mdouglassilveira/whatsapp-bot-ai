import geopandas as gpd
import matplotlib.pyplot as plt
import unidecode
import geobr

# 1) Ler shapefile dos municípios de SP via geobr
sp = geobr.read_municipality(code_muni='SP')

# Lista completa de cidades (sem acentos, para facilitar a comparação).
# Observação: os nomes no shapefile podem ter acentos, então faremos a
# desacentuação (usando unidecode) para comparar.
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

# Cidades que precisam ser destacadas
cidades_destaque = ["Araraquara", "Sertaozinho", "Catanduva", "Barretos"]

# 2) Criar função auxiliar para desacentuar strings
def normalizar(texto):
    return unidecode.unidecode(texto).lower() if texto else ""

# 3) Criar coluna "nome_normalizado" no GeoDataFrame para facilitar matching
sp["nome_normalizado"] = sp["name_muni"].apply(lambda x: normalizar(x))

# 4) Criar dicionário {nome_normalizado: cor}
#    - Vermelho para cidades destaque
#    - Azul para as demais da lista
#    - Cinza claro (ou outra cor) para as que não estão na lista
cores = {}
for muni in sp["nome_normalizado"]:
    # Desacentua e coloca em minúsculo para comparar
    nome = normalizar(muni)
    # Verifica se está na lista_cidades
    if any(nome == normalizar(c) for c in lista_cidades):
        # Verifica se está na lista de destaque
        if any(nome == normalizar(d) for d in cidades_destaque):
            cores[muni] = "#FF5050"  # vermelho
        else:
            cores[muni] = "#3C8DFF"  # azul
    else:
        cores[muni] = "#DDDDDD"    # cinza claro

# 5) Adicionar coluna "cor" ao GeoDataFrame
sp["cor"] = sp["nome_normalizado"].apply(lambda x: cores[x])

# 6) Plotar
fig, ax = plt.subplots(figsize=(8,8))  # tamanho do gráfico
sp.plot(color=sp["cor"], edgecolor="#999999", linewidth=0.3, ax=ax)

# Remover eixos e deixar visual mais limpo
ax.set_axis_off()

# Título (opcional)
ax.set_title("Municípios do Estado de São Paulo", fontsize=14, pad=10)

# 7) Salvar figura em PNG ou exibir
plt.savefig("mapa_sp_simplificado.png", dpi=200, bbox_inches='tight')
plt.show()

import matplotlib

matplotlib.use('TkAgg')  # Backend TkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Configurações iniciais da figura
fig, ax = plt.subplots()
fig.patch.set_facecolor("black")  # Fundo preto para a figura
ax.set_facecolor("black")  # Fundo preto para o eixo
ax.axis("off")  # Remove os eixos
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove margens

# Dimensões do sistema solar
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)

# Dados dos planetas e Lua
planetas = {
    "Sol": {"raio_orbita": 0, "cor": "yellow", "tamanho": 40, "velocidade": 0},  # Sol no centro
    "Mercúrio": {"raio_orbita": 0.4, "cor": "gray", "tamanho": 4, "velocidade": 0.04},  # Antes: 0.2
    "Vênus": {"raio_orbita": 0.7, "cor": "gold", "tamanho": 6, "velocidade": 0.03},  # Antes: 0.15
    "Terra": {"raio_orbita": 1.0, "cor": "dodgerblue", "tamanho": 8, "velocidade": 0.02},  # Antes: 0.1
    "Marte": {"raio_orbita": 1.3, "cor": "orangered", "tamanho": 6, "velocidade": 0.016},  # Antes: 0.08
    "Júpiter": {"raio_orbita": 1.8, "cor": "orange", "tamanho": 16, "velocidade": 0.01},  # Antes: 0.05
    "Saturno": {"raio_orbita": 2.1, "cor": "tan", "tamanho": 14, "velocidade": 0.008},  # Antes: 0.04
    "Urano": {"raio_orbita": 2.6, "cor": "lightblue", "tamanho": 12, "velocidade": 0.006},  # Antes: 0.03
    "Netuno": {"raio_orbita": 3.0, "cor": "blue", "tamanho": 12, "velocidade": 0.004},  # Antes: 0.02
    "Lua": {"raio_orbita": 0.15, "cor": "white", "tamanho": 3, "velocidade": 0.1},  # Lua orbitando a Terra. Antes: 0.5
}

# Adicionar rotação aos planetas
# Vamos criar um dicionário para armazenar o ângulo de rotação de cada planeta
rotacao_planetas = {nome: 0 for nome in planetas.keys() if nome != "Sol"}

# Função de atualização da animação (com rotação dos planetas)
def update(frame):
    for nome, dados in objetos.items():
        if nome == "Lua":
            # Lua orbita ao redor da Terra
            angulo_orbita = frame * planetas["Lua"]["velocidade"]
            x = objetos["Terra"]["objeto"].get_data()[0][0] + planetas["Lua"]["raio_orbita"] * np.cos(angulo_orbita)
            y = objetos["Terra"]["objeto"].get_data()[1][0] + planetas["Lua"]["raio_orbita"] * np.sin(angulo_orbita)
        elif nome == "Sol":
            # Sol permanece fixo no centro
            x, y = 0, 0
        else:
            # Atualizar posições dos planetas (translação)
            dados["angulo"] = frame * dados["velocidade"]
            x = dados["raio_orbita"] * np.cos(dados["angulo"])
            y = dados["raio_orbita"] * np.sin(dados["angulo"])

            # Adicionar rotação ao planeta
            rotacao_planetas[nome] += 0.02  # A velocidade de rotação pode ser ajustada
            rotacao_planetas[nome] = rotacao_planetas[nome] % 360  # Garante que o ângulo de rotação se mantenha dentro de 0-360 graus

        # Define a nova posição (x, y) e rotaciona os planetas
        dados["objeto"].set_data([x], [y])
        # Atualiza a rotação do planeta (ou seja, a rotação sobre seu próprio eixo)
        dados["objeto"].set_markerfacecolor(planet_texturas[nome])  # Dependendo do seu código, você pode ter texturas para planetas aqui.

    return [dados["objeto"] for dados in objetos.values()]


# Objetos animados
objetos = {}

# Orbitas e planetas
for nome, info in planetas.items():
    if nome == "Sol":
        # Adiciona o Sol fixo no centro
        sol, = ax.plot(0, 0, 'o', color=info["cor"], markersize=info["tamanho"], label=nome)
        objetos[nome] = {"objeto": sol, "angulo": 0, "raio_orbita": 0, "velocidade": 0}
    elif nome != "Lua":  # Lua será adicionada separadamente
        # Orbitas
        orbita = plt.Circle((0, 0), info["raio_orbita"], color="white", fill=False, linestyle="--", linewidth=0.5)
        ax.add_artist(orbita)
        # Planetas
        planeta, = ax.plot([], [], 'o', color=info["cor"], markersize=info["tamanho"], label=nome)
        objetos[nome] = {"objeto": planeta, "angulo": 0, "raio_orbita": info["raio_orbita"],
                         "velocidade": info["velocidade"]}

# Adicionando órbita da Lua em volta da Terra
orbita_lua = plt.Circle((0, 0), planetas["Lua"]["raio_orbita"], color="white", fill=False, linestyle="--",
                        linewidth=0.3)
ax.add_artist(orbita_lua)
lua, = ax.plot([], [], 'o', color=planetas["Lua"]["cor"], markersize=planetas["Lua"]["tamanho"], label="Lua")
objetos["Lua"] = {"objeto": lua, "angulo": 0, "raio_orbita": planetas["Lua"]["raio_orbita"],
                  "velocidade": planetas["Lua"]["velocidade"]}


# Função de atualização da animação
def update(frame):
    for nome, dados in objetos.items():
        if nome == "Lua":
            # Lua orbita ao redor da Terra
            angulo = frame * planetas["Lua"]["velocidade"]
            x = objetos["Terra"]["objeto"].get_data()[0][0] + planetas["Lua"]["raio_orbita"] * np.cos(angulo)
            y = objetos["Terra"]["objeto"].get_data()[1][0] + planetas["Lua"]["raio_orbita"] * np.sin(angulo)
        elif nome == "Sol":
            # Sol permanece fixo no centro
            x, y = 0, 0
        else:
            # Atualizar posições dos planetas
            dados["angulo"] = frame * dados["velocidade"]
            x = dados["raio_orbita"] * np.cos(dados["angulo"])
            y = dados["raio_orbita"] * np.sin(dados["angulo"])

        # Define a nova posição (x, y)
        dados["objeto"].set_data([x], [y])

    return [dados["objeto"] for dados in objetos.values()]


# Criando a animação
ani = animation.FuncAnimation(fig, update, frames=360, interval=50, blit=False)

# Exibindo o sistema solar animado
plt.legend(loc="upper right", prop={"size": 8})
plt.show()

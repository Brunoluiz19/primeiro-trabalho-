import pygame
import random
import sys
import time
import math
import os

# Inicializa o Pygame
pygame.init()
pygame.mixer.init()

#música
soundtrack = pygame.mixer.Sound("background.mp3")
soundtrack.play(-1)
explosao = pygame.mixer.Sound("explosao.mp3")

#função para recomecar a musica
def restart_soundtrack():
    soundtrack.stop()  # para a musica
    soundtrack.play(-1)  #recomeca 


# Configurações da tela
largura_tela = 1000
altura_tela = 805
tela = pygame.display.set_mode((largura_tela, altura_tela))

# Cores
BRANCO = (0,0,0)
PRETO = (0,0,0)
# Carrega as imagens
imagem_inicio = pygame.image.load('imagem jogo\_ee80465a-bcb5-435d-90fc-9275a5ca9f2a.jpeg').convert_alpha()
imagem_fundo = pygame.image.load('imagem jogo\Fundo.png').convert()
imagem_morte = pygame.image.load('imagem jogo\_4328f170-e6c9-4d9e-b2bd-367e5ab09727.jpeg').convert_alpha()

# Redimensiona as imagens para ajustar à tela
imagem_inicio = pygame.transform.scale(imagem_inicio, (largura_tela, altura_tela))
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura_tela, altura_tela))
imagem_morte = pygame.transform.scale(imagem_morte, (largura_tela, altura_tela))


# Limites laterais
LIMITE_ESQUERDO = 70
LIMITE_DIREITO = largura_tela - 70
# Variáveis do jogo
distancia_percorrida = 0/100
recorde = 0
melhores_recordes = []

# Função para desenhar texto na tela
def desenhar_texto(texto, tamanho, cor, x, y):
    tamanho = 20
    fonte = pygame.font.Font("Crang.ttf", tamanho)
    texto_surface = fonte.render(texto, True, cor) 
    texto_retangulo = texto_surface.get_rect()
    texto_retangulo.center = (x, y)
    tela.blit(texto_surface, texto_retangulo)

# Classe do jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        carro = "imagem jogo/ferrari.png"
        self.image = pygame.image.load(carro)
        self.image = pygame.transform.scale(self.image, (60, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(LIMITE_ESQUERDO, LIMITE_DIREITO - self.rect.width)
        # Define a posição do jogador na parte inferior da tela
        self.rect.y = altura_tela - self.rect.height - 20  # Ajuste a posição conforme necessário
        self.velocidade = 3

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > LIMITE_ESQUERDO:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.right < LIMITE_DIREITO:
            self.rect.x += self.velocidade
        if teclas[pygame.K_a] and self.rect.left > LIMITE_ESQUERDO:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_d] and self.rect.right < LIMITE_DIREITO:
            self.rect.x += self.velocidade

# Classe do inimigo
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        carro1 = 'imagem jogo\carroinimigo1.png'
        carro2 = 'imagem jogo\carroinimigo2.png'
        carro3 = 'imagem jogo\carroinimigo3.png'
        lista_carros = [carro1, carro2, carro3]
        self.image = pygame.image.load(random.choice(lista_carros))
        self.image = pygame.transform.scale(self.image, (60, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(LIMITE_ESQUERDO, LIMITE_DIREITO - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.velocidade = random.uniform(2, 3)  # Mudança para permitir velocidades decimais

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > altura_tela:
            self.rect.x = random.randrange(LIMITE_ESQUERDO, LIMITE_DIREITO - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.velocidade = random.uniform(2, 4)  # Mudança para permitir velocidades decimais

# Grupo de sprites
todos_sprites = pygame.sprite.Group()
jogador = Jogador()
inimigos = pygame.sprite.Group()
todos_sprites.add(jogador)

# Função para iniciar o jogo
def iniciar_jogo():
    global distancia_percorrida
    global recorde
    global velocidade_jogo
    global fase_atual  # Adicione esta linha
    todos_sprites.empty()
    inimigos.empty()
    todos_sprites.add(jogador)
    distancia_percorrida = 0
    velocidade_jogo = 5
    fase_atual = 0  # Adicione esta linha
    for _ in range(5): 
        x = random.randrange(LIMITE_ESQUERDO, LIMITE_DIREITO - 50)
        inimigo = Inimigo()
        inimigo.rect.x = x
        todos_sprites.add(inimigo)
        inimigos.add(inimigo)

# Tela de início
iniciar_jogo()

# Variáveis de fases
NUM_FASES = 10
fase_atual = 0
metas_fases = [50, 100, 150, 200, 250, 500, 800, 1000, 1200, 1500]  # Distância necessária para cada fase
taxas_aumento_fases = [1.5, 2, 2.5, 3.5, 5, 6, 7, 8, 9, 10]  # Taxa de aumento de velocidade para cada fase  

# Função para determinar a fase atual
def determinar_fase(distancia_percorrida):
    for i in range(NUM_FASES):
        if (distancia_percorrida/100) < metas_fases[i]:
            return i
    return NUM_FASES - 1

# Variável para controlar a velocidade do jogo
velocidade_jogo = 5

# Loop do jogo
rodando = True
em_tela_inicial = True
em_tela_morte = False
clock = pygame.time.Clock()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if (em_tela_inicial or em_tela_morte) and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:  # Sai do jogo se pressionar Esc
                rodando = False
            else:
                iniciar_jogo()
                em_tela_inicial = False
                em_tela_morte = False

    if not em_tela_inicial and not em_tela_morte:
        # Atualizações
        todos_sprites.update()

        # Atualiza a fase
        nova_fase = determinar_fase(distancia_percorrida)
        if nova_fase > fase_atual:
         fase_atual = nova_fase
         # Ajusta a velocidade do jogo para a nova fase
         velocidade_jogo = 5 + taxas_aumento_fases[fase_atual]  

        # Ajusta a velocidade do jogador para a velocidade do jogo
        jogador.velocidade = velocidade_jogo

        # Ajusta a velocidade dos inimigos para a velocidade do jogo
        for inimigo in inimigos:
            inimigo.velocidade = random.uniform(velocidade_jogo - 2, velocidade_jogo - 1)

        # Verifica se o jogador colidiu com algum inimigo
        if pygame.sprite.spritecollide(jogador, inimigos, False):
            soundtrack.stop()
            explosao.play()

            pygame.time.delay(2000)

            restart_soundtrack()
            em_tela_morte = True

            # Atualiza o recorde se a distância percorrida for maior que o recorde atual
            if (distancia_percorrida/100) > recorde:
                recorde = (distancia_percorrida/100)
                # Adiciona o recorde à lista de melhores recordes se ele não estiver lá
                if recorde not in melhores_recordes:
                    melhores_recordes.append(recorde)
                    # Mantém apenas os três melhores recordes
                    melhores_recordes.sort(reverse=True)
                    melhores_recordes = melhores_recordes[:3]

        # Calcula a distância percorrida pelo jogador
        distancia_percorrida += jogador.velocidade

        # Verifica e ajusta as velocidades para evitar que os inimigos se sobreponham
        for inimigo1 in inimigos:
            for inimigo2 in inimigos:
                if inimigo1 != inimigo2 and inimigo1.rect.colliderect(inimigo2.rect):
                    # Se houver colisão, ajusta as velocidades para que não se sobreponham
                    if inimigo1.rect.y < inimigo2.rect.y:
                        inimigo1.rect.y -= 5
                        inimigo2.rect.y += 5
                    else:
                        inimigo1.rect.y += 5
                        inimigo2.rect.y -= 5

        # Desenha na tela
        tela.blit(imagem_fundo, (0, 0))  # Desenha a imagem de fundo
        todos_sprites.draw(tela)

        # Desenha a distância percorrida e o recorde na tela
        desenhar_texto(f'Distância Percorrida: {int(distancia_percorrida/100)}', 20, BRANCO, largura_tela // 2, 20)
        desenhar_texto(f'Recorde: {int(recorde/1)}', 20, BRANCO, largura_tela // 2, 50)

        # Atualiza a tela
        pygame.display.flip()

    elif em_tela_inicial:
        tela.blit(imagem_inicio, (0, 0))  # Desenha a imagem de início
        desenhar_texto("Pressione qualquer tecla para começar", 50, BRANCO, largura_tela // 2, altura_tela // 2)
        pygame.display.flip()

    elif em_tela_morte:
        tela.blit(imagem_morte, (0, 0))  # Desenha a imagem de morte
        desenhar_texto("Você Bateu! Pressione qualquer tecla para reiniciar ou Esc para sair", 50, BRANCO, largura_tela // 2, altura_tela // 2)
        pygame.display.flip()

    clock.tick(120)

# Finaliza o Pygame
pygame.quit()
sys.exit()
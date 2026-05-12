import pygame
import sys


# Inicialização do Pygame

pygame.init()

largura_tela = 1344
altura_tela = 768
fps = 60

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Reino em Ruinas")

clock = pygame.time.Clock()

# CORES

BRANCO = (255, 255, 255)
CINZA = (50, 50, 50)
VERMELHO = (255, 49, 49)
VERDE = (71, 128, 114)
BOTAO_FUNDO = (54, 57, 51)
BORDA_BOTAO = (255, 49, 49)
TEXTO_BRANCO = (255, 255, 255)

#FONTES
fonte = pygame.font.SysFont("Arial", 40, bold=True)
fonte_hud = pygame.font.SysFont("Arial", 30, bold=True)


#carregar imagens do jogo

background = pygame.image.load("img/background.jpg")
background = pygame.transform.scale(background, (largura_tela, altura_tela))

menu = pygame.image.load("img/menu.png")
menu = pygame.transform.scale(menu, (largura_tela, altura_tela))

hero_img = pygame.image.load("img/hero.png")
hero_img = pygame.transform.scale(hero_img, (170, 170))

enemy_img = pygame.image.load("img/enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (200, 200))

hero_icon = pygame.image.load("img/hero_icon.png")

enemy_icon = pygame.image.load("img/enemy_icon.png")

chute_hero = pygame.image.load("img/chute_hero.png")
chute_hero = pygame.transform.scale(chute_hero, (250, 200))

menu_pausa = pygame.image.load("img/menu_pausa.png")
menu_pausa = pygame.transform.scale(menu_pausa, (600, 650))

botao_pausa = pygame.image.load("img/botao_pausa.png")
botao_pausa = pygame.transform.scale(botao_pausa, (60, 60))

vitoria = pygame.image.load("img/vitoria.png")
vitoria = pygame.transform.scale(vitoria, (largura_tela, altura_tela))

game_over = pygame.image.load("img/game_over.png")
game_over = pygame.transform.scale(game_over, (largura_tela, altura_tela))


# -----------------------
# BOTÕES
# -----------------------
botao_jogar = pygame.Rect(550, 400, 250, 60)
botao_sair = pygame.Rect(550, 480, 250, 60)
botao_restart = pygame.Rect(450, 500, 500, 60)

pausa_rect = pygame.Rect(600, 60, 60, 60)

botao_voltar = pygame.Rect(470, 250, 400, 100)
botao_reiniciar = pygame.Rect(470, 400, 400, 100)
botao_sair_pausa = pygame.Rect(470, 550, 400, 100)

# -----------------------
# FUNÇÃO BOTÃO
# -----------------------
def desenhar_botao(rect, texto):
    pygame.draw.rect(tela, BOTAO_FUNDO, rect, border_radius=20)
    pygame.draw.rect(tela, BORDA_BOTAO, rect, 3, border_radius=20)

    txt = fonte.render(texto, True, TEXTO_BRANCO)

    tela.blit(txt, (
        rect.x + (rect.width - txt.get_width()) // 2,
        rect.y + (rect.height - txt.get_height()) // 2
    ))

# -----------------------
# FUNÇÃO BARRA DE VIDA
# -----------------------
def desenhar_barra_vida(nome, vida, vida_max, x, y, cor):
    pygame.draw.rect(tela, CINZA, (x, y, 350, 25), border_radius=15)

    largura = int((vida / vida_max) * 350)
    pygame.draw.rect(tela, cor, (x, y, largura, 25), border_radius=15)

    texto_nome = fonte_hud.render(nome, True, BRANCO)
    tela.blit(texto_nome, (x, y - 35))

# -----------------------
# ESTADOS DO JOGO
# -----------------------
MENU = "menu"
JOGO = "jogo"
GAME_OVER = "game_over"
VITORIA = "vitoria"

estado = MENU

# -----------------------
# VARIÁVEIS DO JOGO
# -----------------------
hero_x = 200
hero_y = 470

enemy_x = 900
enemy_y = 450

velocidade = 5

# -----------------------
# VIDA
# -----------------------
hero_vida_max = 100
hero_vida = 100

enemy_vida_max = 150
enemy_vida = 150

# -----------------------
# ATAQUE
# -----------------------
atacando = False
tempo_ataque = 0
duracao_ataque = 200
dano_aplicado = False

# -----------------------
# PAUSA
# -----------------------
pausado = False
# -----------------------
# RESET DO JOGO
# -----------------------
def reset_jogo():
    global hero_x, hero_y, enemy_x, enemy_y
    global hero_vida, enemy_vida
    global atacando, dano_aplicado
    global pausado

    hero_x, hero_y = 200, 470
    enemy_x, enemy_y = 900, 450

    hero_vida = hero_vida_max
    enemy_vida = enemy_vida_max

    atacando = False
    dano_aplicado = False
    pausado = False

# -----------------------
# LOOP PRINCIPAL
# -----------------------
running = True

while running:
    clock.tick(fps)

    # -----------------------
    # EVENTOS
    # -----------------------
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

        # MENU
        if estado == MENU:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):
                    estado = JOGO

                if botao_sair.collidepoint(evento.pos):
                    running = False

        # JOGO
        if estado == JOGO:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if pausa_rect.collidepoint(evento.pos):
                    pausado = not pausado  # Alternar pausa
                elif pausado:
                    if botao_voltar.collidepoint(evento.pos):
                        pausado = False
                    elif botao_reiniciar.collidepoint(evento.pos):
                        reset_jogo()
                        pausado = False
                    elif botao_sair_pausa.collidepoint(evento.pos):
                        running = False

            if not pausado:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        atacando = True
                        tempo_ataque = pygame.time.get_ticks()
                        dano_aplicado = False

            

        # GAME OVER / VITORIA
        if estado == GAME_OVER or estado == VITORIA:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_restart.collidepoint(evento.pos):
                    reset_jogo()
                    estado = MENU


    # ==================================================
    # MENU
    # ==================================================
    if estado == MENU:
        tela.blit(menu, (0, 0))
        desenhar_botao(botao_jogar, "JOGAR")
        desenhar_botao(botao_sair, "SAIR")

    # ==================================================
    # JOGO
    # ==================================================
    elif estado == JOGO:
        if not pausado:
            teclas = pygame.key.get_pressed()

        # movimento
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            hero_x -= velocidade

        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            hero_x += velocidade

        # limites
        if hero_x < 0:
            hero_x = 0

        if hero_x > largura_tela - hero_img.get_width():
            hero_x = largura_tela - hero_img.get_width()

        # desativar ataque após tempo
        if atacando:
            agora = pygame.time.get_ticks()
            if agora - tempo_ataque > duracao_ataque:
                atacando = False

        # dano só 1 vez por ataque
        distancia = abs(hero_x - enemy_x)

        if atacando and not dano_aplicado and distancia < 140:
            enemy_vida -= 10
            dano_aplicado = True

            if enemy_vida < 0:
                enemy_vida = 0

        # verificar vitória e derrota
        if hero_vida <= 0:
            estado = GAME_OVER

        if enemy_vida <= 0:
            estado = VITORIA

        # desenhar
        tela.blit(background, (0, 0))

        # desenhar personagem com sprite de ataque
        if atacando:
            tela.blit(chute_hero, (hero_x, hero_y))
        else:
            tela.blit(hero_img, (hero_x, hero_y))

        tela.blit(enemy_img, (enemy_x, enemy_y))


        # HUD
        desenhar_barra_vida("Guardiã Sombria", hero_vida, hero_vida_max, 100, 100, VERDE)
        desenhar_barra_vida("Rei Dragão", enemy_vida, enemy_vida_max, 800, 100, VERMELHO)

        # botão pausa
        tela.blit(botao_pausa, (pausa_rect.x, pausa_rect.y))

        if pausado:
            overlay = pygame.Surface((largura_tela, altura_tela))
            overlay.set_alpha(140)
            overlay.fill((0, 0, 0))
            tela.blit(overlay, (0, 0))

            tela.blit(menu_pausa, (370, 80))
            desenhar_botao(botao_voltar, "VOLTAR AO JOGO")
            desenhar_botao(botao_reiniciar, "REINICIAR")
            desenhar_botao(botao_sair_pausa, "SAIR")



    # ==================================================
    # GAME OVER
    # ==================================================
    elif estado == GAME_OVER:
        tela.blit(game_over, (0, 0))
        desenhar_botao(botao_restart, "JOGAR NOVAMENTE")

    # ==================================================
    # VITÓRIA
    # ==================================================
    elif estado == VITORIA:
        tela.blit(vitoria, (0, 0))
        desenhar_botao(botao_restart, "JOGAR NOVAMENTE")

    pygame.display.update()

pygame.quit()
sys.exit()
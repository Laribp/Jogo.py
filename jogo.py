import pygame
import sys

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
AMARELO = (255, 220, 50)
LARANJA = (255, 140, 0)

# FONTES
fonte = pygame.font.SysFont("Arial", 40, bold=True)
fonte_hud = pygame.font.SysFont("Arial", 30, bold=True)
fonte_titulo = pygame.font.SysFont("Arial", 58, bold=True)
fonte_desc = pygame.font.SysFont("Arial", 22)

# IMAGENS BASE
background = pygame.image.load("img/background.jpg")
background = pygame.transform.scale(background, (largura_tela, altura_tela))

menu_img = pygame.image.load("img/menu.png")
menu_img = pygame.transform.scale(menu_img, (largura_tela, altura_tela))

_hero_raw = pygame.image.load("img/hero.png")
_hero_raw = pygame.transform.scale(_hero_raw, (170, 170))

_enemy_raw = pygame.image.load("img/enemy.png")
_enemy_raw = pygame.transform.scale(_enemy_raw, (200, 200))

_chute_raw = pygame.image.load("img/chute_hero.png")
_chute_raw = pygame.transform.scale(_chute_raw, (250, 200))

hero_icon = pygame.image.load("img/hero_icon.png")
enemy_icon = pygame.image.load("img/enemy_icon.png")

menu_pausa_img = pygame.image.load("img/menu_pausa.png")
menu_pausa_img = pygame.transform.scale(menu_pausa_img, (600, 650))

botao_pausa_img = pygame.image.load("img/botao_pausa.png")
botao_pausa_img = pygame.transform.scale(botao_pausa_img, (60, 60))

vitoria_img = pygame.image.load("img/vitoria.png")
vitoria_img = pygame.transform.scale(vitoria_img, (largura_tela, altura_tela))

game_over_img = pygame.image.load("img/game_over.png")
game_over_img = pygame.transform.scale(game_over_img, (largura_tela, altura_tela))

# SPRITES DIRECIONAIS HERÓI (1=direita, -1=esquerda)
# hero_img original assume que o boneco olha para a DIREITA
sprites_heroi = {
    "guerreiro": {
         1: _hero_raw,
        -1: pygame.transform.flip(_hero_raw, True, False),
    },
    "arqueiro": {
         1: pygame.transform.flip(_hero_raw, True, False),   # arqueiro visual diferenciado
        -1: _hero_raw,
    },
}
sprites_ataque_heroi = {
    "guerreiro": {
         1: _chute_raw,
        -1: pygame.transform.flip(_chute_raw, True, False),
    },
    "arqueiro": {
         1: pygame.transform.flip(_chute_raw, True, False),
        -1: _chute_raw,
    },
}

# SPRITES DIRECIONAIS INIMIGO
# enemy_img original assume que o boneco olha para a ESQUERDA (em direção ao herói)
sprites_enemy = {
    -1: _enemy_raw,                                           # olhando para esquerda
     1: pygame.transform.flip(_enemy_raw, True, False),      # olhando para direita
}

# BOTÕES MENU
botao_jogar = pygame.Rect(550, 400, 250, 60)
botao_sair = pygame.Rect(550, 480, 250, 60)
botao_restart = pygame.Rect(450, 500, 500, 60)

pausa_rect = pygame.Rect(600, 60, 60, 60)
botao_voltar = pygame.Rect(470, 250, 400, 100)
botao_reiniciar = pygame.Rect(470, 400, 400, 100)
botao_sair_pausa = pygame.Rect(470, 550, 400, 100)

# BOTÕES SELEÇÃO DE CLASSE
botao_guerreiro = pygame.Rect(180, 230, 400, 320)
botao_arqueiro = pygame.Rect(770, 230, 400, 320)

# ESTADOS
MENU = "menu"
SELECAO_CLASSE = "selecao_classe"
JOGO = "jogo"
GAME_OVER = "game_over"
VITORIA = "vitoria"

estado = MENU
classe_heroi = None

# POSIÇÕES
hero_x = 200
hero_y = 470
enemy_x = 950
enemy_y = 450
velocidade_heroi = 5

# DIREÇÕES (1=direita, -1=esquerda)
heroi_direcao = 1    # herói começa olhando para a direita (em direção ao inimigo)
enemy_direcao = -1   # inimigo começa olhando para a esquerda (em direção ao herói)

# VIDA
hero_vida_max = 100
hero_vida = 100
enemy_vida_max = 150
enemy_vida = 150

# ATAQUE HERÓI
atacando = False
tempo_ataque = 0
duracao_ataque = 200
dano_aplicado = False
cooldown_ataque = 0
COOLDOWN_GUERREIRO = 600
COOLDOWN_ARQUEIRO = 700

# PROJÉTEIS
projeteis = []

# INIMIGO
enemy_velocidade = 2
enemy_atacando = False
tempo_ultimo_ataque_enemy = 0
COOLDOWN_ENEMY = 1400
RANGE_ATAQUE_ENEMY = 170

# PAUSA
pausado = False


def desenhar_botao(rect, texto):
    pygame.draw.rect(tela, BOTAO_FUNDO, rect, border_radius=20)
    pygame.draw.rect(tela, BORDA_BOTAO, rect, 3, border_radius=20)
    txt = fonte.render(texto, True, TEXTO_BRANCO)
    tela.blit(txt, (
        rect.x + (rect.width - txt.get_width()) // 2,
        rect.y + (rect.height - txt.get_height()) // 2
    ))


def desenhar_barra_vida(nome, vida, vida_max, x, y, cor):
    pygame.draw.rect(tela, CINZA, (x, y, 350, 25), border_radius=15)
    largura = int((vida / vida_max) * 350)
    pygame.draw.rect(tela, cor, (x, y, largura, 25), border_radius=15)
    texto_nome = fonte_hud.render(nome, True, BRANCO)
    tela.blit(texto_nome, (x, y - 35))


def desenhar_selecao_classe():
    tela.blit(background, (0, 0))
    overlay = pygame.Surface((largura_tela, altura_tela))
    overlay.set_alpha(170)
    overlay.fill((0, 0, 0))
    tela.blit(overlay, (0, 0))

    titulo = fonte_titulo.render("ESCOLHA SUA CLASSE", True, AMARELO)
    tela.blit(titulo, (largura_tela // 2 - titulo.get_width() // 2, 70))

    subtitulo = fonte_desc.render("Clique em uma classe para começar", True, BRANCO)
    tela.blit(subtitulo, (largura_tela // 2 - subtitulo.get_width() // 2, 145))

    mouse_pos = pygame.mouse.get_pos()

    for btn, nome_cls, img_cls, titulo_cls, descs, cor_fundo in [
        (
            botao_guerreiro,
            "guerreiro",
            pygame.transform.scale(sprites_heroi["guerreiro"][1], (130, 130)),
            "GUERREIRO",
            ["Ataque corpo a corpo", "Dano: 15 por golpe", "Alcance: curto", "Tecla: ESPAÇO"],
            (50, 30, 20),
        ),
        (
            botao_arqueiro,
            "arqueiro",
            pygame.transform.scale(sprites_heroi["arqueiro"][1], (130, 130)),
            "ARQUEIRO",
            ["Ataque à distância", "Dano: 12 por flecha", "Alcance: longo", "Tecla: ESPAÇO"],
            (20, 30, 50),
        ),
    ]:
        hover = btn.collidepoint(mouse_pos)
        cor_borda = AMARELO if hover else VERMELHO
        escala = 1.04 if hover else 1.0
        btn_draw = pygame.Rect(
            btn.x - int(btn.width * (escala - 1) / 2),
            btn.y - int(btn.height * (escala - 1) / 2),
            int(btn.width * escala),
            int(btn.height * escala),
        )
        pygame.draw.rect(tela, cor_fundo, btn_draw, border_radius=18)
        pygame.draw.rect(tela, cor_borda, btn_draw, 3, border_radius=18)

        tela.blit(img_cls, (btn.x + (btn.width - 130) // 2, btn.y + 15))

        t_nome = fonte.render(titulo_cls, True, AMARELO)
        tela.blit(t_nome, (btn.x + (btn.width - t_nome.get_width()) // 2, btn.y + 160))

        for i, d in enumerate(descs):
            cor_texto = LARANJA if i == 3 else BRANCO
            t = fonte_desc.render(d, True, cor_texto)
            tela.blit(t, (btn.x + (btn.width - t.get_width()) // 2, btn.y + 215 + i * 26))


def reset_jogo():
    global hero_x, hero_y, enemy_x, enemy_y
    global hero_vida, enemy_vida
    global atacando, dano_aplicado, cooldown_ataque
    global pausado, projeteis
    global enemy_atacando, tempo_ultimo_ataque_enemy
    global heroi_direcao, enemy_direcao

    hero_x, hero_y = 200, 470
    enemy_x, enemy_y = 950, 450
    hero_vida = hero_vida_max
    enemy_vida = enemy_vida_max
    atacando = False
    dano_aplicado = False
    cooldown_ataque = 0
    pausado = False
    projeteis = []
    enemy_atacando = False
    tempo_ultimo_ataque_enemy = 0
    heroi_direcao = 1
    enemy_direcao = -1


running = True

while running:
    clock.tick(fps)
    agora = pygame.time.get_ticks()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

        if estado == MENU:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):
                    estado = SELECAO_CLASSE
                if botao_sair.collidepoint(evento.pos):
                    running = False

        elif estado == SELECAO_CLASSE:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_guerreiro.collidepoint(evento.pos):
                    classe_heroi = "guerreiro"
                    reset_jogo()
                    estado = JOGO
                if botao_arqueiro.collidepoint(evento.pos):
                    classe_heroi = "arqueiro"
                    reset_jogo()
                    estado = JOGO

        elif estado == JOGO:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if pausa_rect.collidepoint(evento.pos):
                    pausado = not pausado
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
                    if evento.key == pygame.K_SPACE and agora >= cooldown_ataque:
                        if classe_heroi == "guerreiro":
                            atacando = True
                            tempo_ataque = agora
                            dano_aplicado = False
                            cooldown_ataque = agora + COOLDOWN_GUERREIRO
                        elif classe_heroi == "arqueiro":
                            # flecha sai no lado oposto ao movimento (arqueiro atira para trás)
                            direcao_flecha = -heroi_direcao
                            if direcao_flecha == 1:
                                flecha_x = hero_x + 160
                            else:
                                flecha_x = hero_x - 22
                            projeteis.append({
                                "x": flecha_x,
                                "y": hero_y + 75,
                                "direcao": direcao_flecha,
                            })
                            atacando = True
                            tempo_ataque = agora
                            cooldown_ataque = agora + COOLDOWN_ARQUEIRO

        elif estado in (GAME_OVER, VITORIA):
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_restart.collidepoint(evento.pos):
                    reset_jogo()
                    estado = SELECAO_CLASSE

    # ==================================================
    # MENU
    # ==================================================
    if estado == MENU:
        tela.blit(menu_img, (0, 0))
        desenhar_botao(botao_jogar, "JOGAR")
        desenhar_botao(botao_sair, "SAIR")

    # ==================================================
    # SELEÇÃO DE CLASSE
    # ==================================================
    elif estado == SELECAO_CLASSE:
        desenhar_selecao_classe()

    # ==================================================
    # JOGO
    # ==================================================
    elif estado == JOGO:
        if not pausado:
            teclas = pygame.key.get_pressed()

            # Movimento herói + atualiza direção
            movendo = False
            if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
                hero_x -= velocidade_heroi
                heroi_direcao = -1
                movendo = True
            if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
                hero_x += velocidade_heroi
                heroi_direcao = 1
                movendo = True
            hero_x = max(0, min(hero_x, largura_tela - 170))

            # Desativar animação de ataque após duração
            if atacando and agora - tempo_ataque > duracao_ataque:
                atacando = False

            # Dano corpo a corpo (guerreiro)
            if classe_heroi == "guerreiro":
                distancia = abs(hero_x - enemy_x)
                if atacando and not dano_aplicado and distancia < 160:
                    enemy_vida = max(0, enemy_vida - 15)
                    dano_aplicado = True

            # Mover projéteis e verificar colisão (arqueiro)
            projeteis_ativos = []
            for p in projeteis:
                p["x"] += 11 * p["direcao"]
                enemy_rect = pygame.Rect(enemy_x + 20, enemy_y + 10, 160, 180)
                projetil_rect = pygame.Rect(p["x"], p["y"], 22, 8)
                if projetil_rect.colliderect(enemy_rect):
                    enemy_vida = max(0, enemy_vida - 12)
                elif 0 <= p["x"] <= largura_tela:
                    projeteis_ativos.append(p)
            projeteis = projeteis_ativos

            # Movimento do inimigo em direção ao herói + atualiza direção
            diff = enemy_x - hero_x
            if diff > RANGE_ATAQUE_ENEMY:
                enemy_x -= enemy_velocidade
                enemy_direcao = -1   # movendo para a esquerda (em direção ao herói)
            elif diff < -RANGE_ATAQUE_ENEMY:
                enemy_x += enemy_velocidade
                enemy_direcao = 1    # movendo para a direita (herói passou para a direita)
            else:
                # Parado: vira para encarar o herói
                enemy_direcao = -1 if hero_x < enemy_x else 1
            enemy_x = max(0, min(enemy_x, largura_tela - 200))

            # Ataque do inimigo
            if abs(hero_x - enemy_x) < RANGE_ATAQUE_ENEMY:
                if agora - tempo_ultimo_ataque_enemy > COOLDOWN_ENEMY:
                    hero_vida = max(0, hero_vida - 10)
                    tempo_ultimo_ataque_enemy = agora
                    enemy_atacando = True
            if enemy_atacando and agora - tempo_ultimo_ataque_enemy > 300:
                enemy_atacando = False

            # Verificar fim de jogo
            if hero_vida <= 0:
                estado = GAME_OVER
            if enemy_vida <= 0:
                estado = VITORIA

        # DESENHO
        tela.blit(background, (0, 0))

        # Herói — sprite baseado em classe + direção + animação de ataque
        if atacando:
            sprite_heroi = sprites_ataque_heroi[classe_heroi][heroi_direcao]
            # offset horizontal para o sprite de ataque (mais largo que o normal)
            offset_atk = -80 if heroi_direcao == -1 else 0
            tela.blit(sprite_heroi, (hero_x + offset_atk, hero_y))
        else:
            tela.blit(sprites_heroi[classe_heroi][heroi_direcao], (hero_x, hero_y))

        # Inimigo — sprite baseado na direção atual
        sprite_inimigo = sprites_enemy[enemy_direcao]
        tela.blit(sprite_inimigo, (enemy_x, enemy_y))

        # Projéteis
        for p in projeteis:
            pygame.draw.rect(tela, AMARELO, (p["x"], p["y"], 22, 8), border_radius=4)
            # ponta da flecha no lado da direção de movimento
            ponta_x = p["x"] + (22 if p["direcao"] == 1 else -6)
            pygame.draw.polygon(tela, LARANJA, [
                (ponta_x, p["y"] + 4),
                (ponta_x - 8 * p["direcao"], p["y"]),
                (ponta_x - 8 * p["direcao"], p["y"] + 8),
            ])

        # HUD
        sufixo = "[Guerreiro]" if classe_heroi == "guerreiro" else "[Arqueiro]"
        desenhar_barra_vida(f"Guardiã Sombria {sufixo}", hero_vida, hero_vida_max, 100, 100, VERDE)
        desenhar_barra_vida("Rei Dragão", enemy_vida, enemy_vida_max, 800, 100, VERMELHO)

        # Barra de cooldown do ataque
        restante = max(0, cooldown_ataque - agora)
        cd_max = COOLDOWN_GUERREIRO if classe_heroi == "guerreiro" else COOLDOWN_ARQUEIRO
        t_cd = fonte_desc.render("ATAQUE", True, BRANCO)
        tela.blit(t_cd, (100, 130))
        pygame.draw.rect(tela, CINZA, (100, 148, 180, 10), border_radius=5)
        if restante > 0:
            pct = 1.0 - restante / cd_max
            pygame.draw.rect(tela, AMARELO, (100, 148, int(180 * pct), 10), border_radius=5)
        else:
            pygame.draw.rect(tela, AMARELO, (100, 148, 180, 10), border_radius=5)

        tela.blit(botao_pausa_img, (pausa_rect.x, pausa_rect.y))

        if pausado:
            overlay = pygame.Surface((largura_tela, altura_tela))
            overlay.set_alpha(140)
            overlay.fill((0, 0, 0))
            tela.blit(overlay, (0, 0))
            tela.blit(menu_pausa_img, (370, 80))
            desenhar_botao(botao_voltar, "VOLTAR AO JOGO")
            desenhar_botao(botao_reiniciar, "REINICIAR")
            desenhar_botao(botao_sair_pausa, "SAIR")

    # ==================================================
    # GAME OVER
    # ==================================================
    elif estado == GAME_OVER:
        tela.blit(game_over_img, (0, 0))
        desenhar_botao(botao_restart, "JOGAR NOVAMENTE")

    # ==================================================
    # VITÓRIA
    # ==================================================
    elif estado == VITORIA:
        tela.blit(vitoria_img, (0, 0))
        desenhar_botao(botao_restart, "JOGAR NOVAMENTE")

    pygame.display.update()

pygame.quit()
sys.exit()

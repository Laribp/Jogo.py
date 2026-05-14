# Reino em Ruinas

Jogo de luta 2D desenvolvido em Python com Pygame.

## Sobre o Jogo

Enfrente o **Rei Dragão** escolhendo entre duas classes de personagem: o **Guerreiro**, que luta corpo a corpo, ou o **Arqueiro**, que ataca à distância. O inimigo se move e contra-ataca automaticamente.

## Funcionalidades

- Tela de seleção de classe (Guerreiro ou Arqueiro)
- Guerreiro: ataque corpo a corpo com animação de chute
- Arqueiro: disparo de flechas direcionais (atira no sentido oposto ao movimento)
- Inimigo com movimentação e IA de ataque
- Sprites direcionais — personagens viram conforme o movimento
- Barras de vida no HUD
- Barra de cooldown do ataque
- Menu de pausa com opções de retomar, reiniciar ou sair
- Telas de vitória e game over

## Controles

| Tecla | Ação |
|-------|------|
| `A` / `←` | Mover para a esquerda |
| `D` / `→` | Mover para a direita |
| `ESPAÇO` | Atacar / Atirar flecha |
| Botão `II` | Pausar / Retomar |

## Requisitos

- Python 3.10 ou superior
- pygame-ce

## Instalação

```bash
pip install pygame-ce
```

## Como Jogar

```bash
python jogo.py
```

## Estrutura do Projeto

```
Jogo.py/
├── jogo.py        # Código principal do jogo
├── img/           # Assets de imagem
│   ├── background.jpg
│   ├── menu.png
│   ├── hero.png
│   ├── enemy.png
│   ├── chute_hero.png
│   ├── hero_icon.png
│   ├── enemy_icon.png
│   ├── botao_pausa.png
│   ├── menu_pausa.png
│   ├── vitoria.png
│   └── game_over.png
└── README.md
```

## Tecnologias

- Python 3
- [pygame-ce](https://pypi.org/project/pygame-ce/) (Community Edition)

# Changelog — Reino em Ruinas

## [1.2.0] - 2026-05-14

### Alterado
- **Arqueiro:** direção das flechas invertida em relação ao movimento
  - `D` / `→` → arqueiro move para direita, flecha vai para a **esquerda**
  - `A` / `←` → arqueiro move para esquerda, flecha vai para a **direita**

---

## [1.1.0] - 2026-05-14

### Adicionado
- **Sprites direcionais para o herói:** boneco vira para o lado correto ao pressionar A/D
- **Sprites direcionais para o inimigo:** inimigo vira o sprite conforme se move ou encara o herói
- **Sprites de ataque direcionais:** animação de ataque também espelha conforme a direção
- **Flechas direcionais:** flecha sai da ponta correta do boneco e viaja na direção que ele está olhando
- Ponta triangular na flecha indica visualmente a direção de movimento

### Corrigido
- Posição de origem da flecha ajustada para cada direção (saía sempre pelo mesmo lado)

---

## [1.0.0] - 2026-05-14

### Adicionado
- **Tela de seleção de classe** entre Menu e Jogo
  - **Guerreiro:** ataque corpo a corpo, dano 15, alcance ~160px, cooldown 600ms
  - **Arqueiro:** disparo de flechas, dano 12, alcance total da tela, cooldown 700ms
- **Movimento do inimigo:** inimigo caminha em direção ao herói automaticamente
- **IA de ataque do inimigo:** ataca o herói a cada 1400ms causando 10 de dano quando próximo (~170px)
- **Barra de cooldown** do ataque exibida no HUD
- **Projéteis do arqueiro** representados com corpo amarelo e ponta laranja
- **Reiniciar** agora retorna à tela de seleção de classe em vez do menu principal

### Alterado
- Dano do guerreiro aumentado de 10 para 15 por golpe
- Nomes das variáveis de imagem renomeados para evitar conflito (`menu` → `menu_img`, etc.)
- Todo o estado do jogo (direção, projéteis, cooldowns) resetado corretamente no `reset_jogo()`

---

## [0.1.0] - versão original

### Funcionalidades base
- Menu principal com botões Jogar e Sair
- Herói móvel (A/D ou setas) com ataque por ESPAÇO (dano 10, alcance 140px)
- Inimigo estático
- Barras de vida para herói e inimigo
- Menu de pausa (voltar, reiniciar, sair)
- Telas de vitória e game over

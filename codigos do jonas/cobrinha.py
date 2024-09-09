import pygame
import random
import sys

pygame.init()
largura = 600
altura = 400
tela = pygame.display.set_mode((largura, altura))

pygame.display.set_caption("Jogo da Cobrinha")
verde = (0, 255, 0)
vermelho = (255, 0, 0)
preto = (0, 0, 0)

tamanho_celula = 20
velocidade = 15
relogio = pygame.time.Clock()

def gerar_comida():
    x_comida = random.randrange(0, largura, tamanho_celula)
    y_comida = random.randrange(0, altura, tamanho_celula)
    return x_comida, y_comida

def desenhar_cobrinha(cobra):
    for parte in cobra:
        pygame.draw.rect(tela, verde, (parte[0], parte[1], tamanho_celula, tamanho_celula))

def jogo():
    x = largura // 2
    y = altura // 2
    x_velocidade = 0
    y_velocidade = 0
    cobra = [(x, y)]
    comprimento_cobra = 1

    x_comida, y_comida = gerar_comida()

    while True:
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and x_velocidade == 0:
                    x_velocidade = -tamanho_celula
                    y_velocidade = 0
                elif evento.key == pygame.K_RIGHT and x_velocidade == 0:
                    x_velocidade = tamanho_celula
                    y_velocidade = 0
                elif evento.key == pygame.K_UP and y_velocidade == 0:
                    x_velocidade = 0
                    y_velocidade = -tamanho_celula
                elif evento.key == pygame.K_DOWN and y_velocidade == 0:
                    x_velocidade = 0
                    y_velocidade = tamanho_celula

        x += x_velocidade
        y += y_velocidade
        cobra.append((x, y))

        if len(cobra) > comprimento_cobra:
            del cobra[0]

        if x < 0 or x >= largura or y < 0 or y >= altura or (x, y) in cobra[:-1]:
            break

        if x == x_comida and y == y_comida:
            comprimento_cobra += 1
            x_comida, y_comida = gerar_comida()

        tela.fill(preto)
        desenhar_cobrinha(cobra)
        pygame.draw.rect(tela, vermelho, (x_comida, y_comida, tamanho_celula, tamanho_celula))
        pygame.display.flip()

        relogio.tick(velocidade)

jogo()
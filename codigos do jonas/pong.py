import pygame
import sys

pygame.init()

largura = 800
altura = 400
tela = pygame.display.set_mode((largura, altura))

pygame.display.set_caption("Pong")

branco = (255, 255, 255)
preto = (0, 0, 0)
azul = (0, 128, 255)
verde = (0, 255, 0)
amarelo = (255, 255, 0)

raquete_largura = 10
raquete_altura = 100
raquete_esquerda_y = altura // 2 - raquete_altura // 2
raquete_direita_y = altura // 2 - raquete_altura // 2

bola_x, bola_y = largura // 2, altura // 2
bola_dx, bola_dy = 5, 5

velocidade_raquete = 5

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_w]:
        raquete_esquerda_y -= velocidade_raquete
    if teclas[pygame.K_s]:
        raquete_esquerda_y += velocidade_raquete
    if teclas[pygame.K_UP]:
        raquete_direita_y -= velocidade_raquete
    if teclas[pygame.K_DOWN]:
        raquete_direita_y += velocidade_raquete

    if bola_y < 0 or bola_y > altura - 10:
        bola_dy = -bola_dy

    bola_x += bola_dx
    bola_y += bola_dy

    if bola_x < 20 and raquete_esquerda_y < bola_y < raquete_esquerda_y + raquete_altura:
        bola_dx = -bola_dx

    if bola_x > largura - 30 and raquete_direita_y < bola_y < raquete_direita_y + raquete_altura:
        bola_dx = -bola_dx


    if bola_x < 0 or bola_x > largura:
        bola_x, bola_y = largura // 2, altura // 2
        bola_dx, bola_dy = -bola_dx, bola_dy 
    tela.fill(preto)

    pygame.draw.rect(tela, azul, (10, raquete_esquerda_y, raquete_largura, raquete_altura)) 
    pygame.draw.rect(tela, verde, (largura - 20, raquete_direita_y, raquete_largura, raquete_altura))  
    pygame.draw.ellipse(tela, amarelo, (bola_x, bola_y, 10, 10))  # Bola

    pygame.display.flip()
    pygame.time.Clock().tick(60)
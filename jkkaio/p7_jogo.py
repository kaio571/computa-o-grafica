import pygame, random
# Carregando as imagens.
imagemNave = pygame.image.load("nave.png")
imagemAsteroide = pygame.image.load("asteroide.png")
imagemRaio = pygame.image.load("raio.png")
imagemFundo = pygame.image.load("espaço.png")
LARGURAJANELA = 600
ALTURAJANELA = 600
CORTEXTO = (255, 255, 255)
QPS = 40
TAMMINIMO = 10
TAMMAXIMO = 40
VELMINIMA = 1
VELMAXIMA = 8
ITERACOES = 6
VELJOGADOR = 5
VELRAIO = (0,-15)
# largura da janela
# altura da janela
# cor do texto (branca)
# quadros por segundo
# tamanho mínimo do asteroide
# tamanho máximo do asteroide
# velocidade mínima do asteroide
# velocidade máxima do asteroide
# número de iterações antes de criar um novo asteroide
# velocidade da nave
# velocidade do raio
LARGURANAVE = imagemNave.get_width()
ALTURANAVE = imagemNave.get_height()
LARGURARAIO = imagemRaio.get_width()
ALTURARAIO = imagemRaio.get_height()

def moverJogador(jogador, teclas, dim_janela):
    borda_esquerda = 0
    borda_superior = 0
    borda_direita = dim_janela[0]
    borda_inferior = dim_janela[1]
    if teclas["esquerda"] and jogador["objRect"].left > borda_esquerda:
        jogador["objRect"].x -= jogador["vel"]
    if teclas["direita"] and jogador["objRect"].right < borda_direita:
        jogador["objRect"].x += jogador["vel"]
    if teclas["cima"] and jogador["objRect"].top > borda_superior:
        jogador["objRect"].y -= jogador["vel"]
    if teclas["baixo"] and jogador["objRect"].bottom < borda_inferior:
        jogador["objRect"].y += jogador["vel"]

def moverElemento(elemento):
    elemento["objRect"].x += elemento["vel"][0]
    elemento["objRect"].y += elemento["vel"][1]

def terminar():
    # Termina o programa.
    pygame.quit()
    exit()

def aguardarEntrada():
    # Aguarda entrada por teclado ou clique do mouse no "x" da janela.
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: 
                    terminar()
                return

def colocarTexto(texto, fonte, janela, x, y):
    # Coloca na posição (x,y) da janela o texto com a fonte passados por argumento.
    objTexto = fonte.render(texto, True, CORTEXTO)
    rectTexto = objTexto.get_rect()
    rectTexto.topleft = (x, y)
    janela.blit(objTexto, rectTexto)

# Configurando pygame, relogio, janela.
pygame.init()
relogio = pygame.time.Clock()
janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
pygame.display.set_caption("Asteroides Troianos")
# Ocultando o cursor e redimensionando a imagem de fundo.
pygame.mouse.set_visible(False)   
imagemFundoRedim = pygame.transform.scale(imagemFundo,(LARGURAJANELA, ALTURAJANELA))
# Configurando a fonte.
fonte = pygame.font.Font(None, 48)
# Configurando o som.
somFinal = pygame.mixer.Sound("final_fx.wav")
somRecorde = pygame.mixer.Sound("record.wav")
somTiro = pygame.mixer.Sound("laser.wav")
pygame.mixer.music.load("trilha_nave.wav")
# Tela de inicio.
colocarTexto("Asteroides Troianos", fonte, janela, LARGURAJANELA / 5, ALTURAJANELA / 3)
colocarTexto("Pressione uma tecla para começar.", fonte, janela, LARGURAJANELA / 20 , ALTURAJANELA / 2)
pygame.display.update()
aguardarEntrada()
recorde = 0
while True:
    # Configurando o começo do jogo.
    asteroides = []     
    raios = []                                                      
    pontuacao = 0     
    deve_continuar = True                            
    # lista com os asteroides
    # lista com os raios
    # pontuação
    # indica se o loop do jogo deve continuar
    # direções de movimentação
    teclas = {}
    teclas["esquerda"] = teclas["direita"] = teclas["cima"] = teclas["baixo"] = False  
    contador = 0                             
    # contador de iterações
    pygame.mixer.music.play(-1, 0.0)    
    # colocando a música de fundo
    # Criando jogador.
    posX = LARGURAJANELA / 2
    posY = ALTURAJANELA - 50
    jogador = {"objRect": pygame.Rect(posX, posY, LARGURANAVE, ALTURANAVE), "imagem": imagemNave, "vel": VELJOGADOR}
    while deve_continuar:               
        pontuacao += 1 
        if pontuacao == recorde:
            somRecorde.play()
        # Checando os eventos ocorridos.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    terminar()
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    teclas["esquerda"] = True
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    teclas["direita"] = True
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    teclas["cima"] = True
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    teclas["baixo"] = True
                if evento.key == pygame.K_SPACE:
                    raio = {"objRect": pygame.Rect(jogador["objRect"].centerx, jogador["objRect"].top, LARGURARAIO, ALTURARAIO), "imagem": imagemRaio, "vel": VELRAIO}
                    raios.append(raio)
                    somTiro.play()
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    teclas["esquerda"] = False
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    teclas["direita"] = False
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    teclas["cima"] = False
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    teclas["baixo"] = False
            if evento.type == pygame.MOUSEMOTION:
                # Se o mouse se move, movimenta jogador para onde o cursor está.
                centroX_jogador = jogador["objRect"].centerx
                centroY_jogador = jogador["objRect"].centery
                jogador["objRect"].move_ip(evento.pos[0] - centroX_jogador, evento.pos[1] - centroY_jogador)
            if evento.type == pygame.MOUSEBUTTONDOWN:
                raio = {"objRect": pygame.Rect(jogador["objRect"].centerx, jogador["objRect"].top, LARGURARAIO, ALTURARAIO), "imagem": imagemRaio, "vel": VELRAIO}
                raios.append(raio)
                somTiro.play()
        # Preenchendo o fundo da janela com a imagem correspondente.
        janela.blit(imagemFundoRedim, (0,0))        
        # Colocando as pontuações.
        colocarTexto("Pontuação: " + str(pontuacao), fonte, janela, 10, 0)
        colocarTexto("Recorde: " + str(recorde), fonte, janela, 10, 40)
        # Adicionando asteroides quando indicado.
        contador += 1
        if contador >= ITERACOES:
            contador = 0
            tamAsteroide = random.randint(TAMMINIMO, TAMMAXIMO)
            posX = random.randint(0, LARGURAJANELA - tamAsteroide)
            posY = - tamAsteroide
            vel_x = random.randint(-1,1)
            vel_y = random.randint(VELMINIMA, VELMAXIMA)
            asteroide = {"objRect": pygame.Rect(posX, posY, tamAsteroide, tamAsteroide),  
                         "imagem": pygame.transform.scale(imagemAsteroide, (tamAsteroide, tamAsteroide)), 
                         "vel": (vel_x, vel_y)} 
            asteroides.append(asteroide)
                # Movimentando e desenhando os asteroides.
        for asteroide in asteroides:
            moverElemento(asteroide)
            janela.blit(asteroide["imagem"], asteroide["objRect"])

        # Eliminando os asteroides que passam pela base da janela.
        for asteroide in asteroides[:]:
            topo_asteroide = asteroide["objRect"].top
            if topo_asteroide > ALTURAJANELA:
                asteroides.remove(asteroide)

        # Movimentando e desenhando os raios.
        for raio in raios:
            moverElemento(raio)
            janela.blit(raio["imagem"], raio["objRect"])

        # Eliminando os raios que passam pelo topo da janela.
        for raio in raios[:]:
            base_raio = raio["objRect"].bottom
            if base_raio < 0:
                raios.remove(raio)

        # Movimentando e desenhando jogador (nave).
        moverJogador(jogador, teclas, (LARGURAJANELA, ALTURAJANELA))
        janela.blit(jogador["imagem"], jogador["objRect"])

        # Checando se jogador ou algum raio colidiu com algum asteroide.
        for asteroide in asteroides[:]:
            jogadorColidiu = jogador["objRect"].colliderect(asteroide["objRect"])
            if jogadorColidiu:
                if pontuacao > recorde:
                    recorde = pontuacao
                deve_continuar = False

        for raio in raios[:]:
            raioColidiu = raio["objRect"].colliderect(asteroide["objRect"])
            if raioColidiu:
                raios.remove(raio)
                asteroides.remove(asteroide)

        pygame.display.update()
        relogio.tick(QPS)

    # Parando o jogo e mostrando a tela final.
    pygame.mixer.music.stop()
    somFinal.play()
    colocarTexto("GAME OVER", fonte, janela, (LARGURAJANELA / 3), (ALTURAJANELA / 3))
    colocarTexto("Pressione uma tecla para jogar.", fonte, janela, (LARGURAJANELA / 10), (ALTURAJANELA / 2))
    pygame.display.update()

    # Aguardando entrada por teclado para reiniciar o jogo ou sair.
    aguardarEntrada()
    somFinal.stop()       
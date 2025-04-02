from itertools import chain

import pygame
import os
import random

pygame.init()

TELA_LARGURA = 500
TELA_ALTURA = 700

IMAGE_CANO = [
pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png'))),
pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe1.png'))),
pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe2.png'))),
pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe3.png'))),
pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe4.png'))),
]
IMAGE_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGE_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGE_PASSARO = [
pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial',50)
FONTE_INICIO = pygame.font.SysFont('arial', 40)

def tela_inicio(tela):
    tela.blit(IMAGE_BACKGROUND, (0, 0))

    fonte_nome = pygame.font.SysFont('arial', 50, bold=True)
    nome_jogo = fonte_nome.render("Flappy OCTOCAT", True, (255, 223, 0))
    pos_nome = (TELA_LARGURA // 2 - nome_jogo.get_width() // 2, 80)

    botao_rect = pygame.Rect((TELA_LARGURA // 2 - 100, TELA_ALTURA // 2 - 30, 200, 60))
    cor_botao = (0, 150, 255)
    cor_texto = (255, 255, 255)

    esperando = True
    while esperando:
        tela.blit(IMAGE_BACKGROUND, (0, 0))
        tela.blit(nome_jogo, pos_nome)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        cor_atual = (0, 100, 200) if botao_rect.collidepoint(mouse_x, mouse_y) else cor_botao
        pygame.draw.rect(tela, cor_atual, botao_rect, border_radius=15)
        texto = FONTE_INICIO.render("Start", True, cor_texto)
        tela.blit(texto, (botao_rect.x + 50, botao_rect.y + 10))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN and botao_rect.collidepoint(mouse_x, mouse_y):
                esperando = False



class Passaro :
    IMGS = IMAGE_PASSARO
    #ANIMAÇÕES DA ROTAÇÃO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -7
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        #calcular o deslocamento
        self.tempo += 1
        deslocamento = 1 * (self.tempo**2) + self.velocidade * self.tempo
        #restringir o deslocamento
        if deslocamento > 16 :
            deslocamento = 16
        elif deslocamento < 0 :
             deslocamento -= 2
        self.y += deslocamento
        if self.y < 50:  # Antes era 0, agora limitamos a 50 para dar mais espaço
            self.y = 50
        #o angulo do passaro

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
       # definir qual imagem do passaro vai usar
       self.contagem_imagem += 1
       if self.contagem_imagem < self.TEMPO_ANIMACAO :
           self.imagem = self.IMGS[0]
       elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
           self.imagem = self.IMGS[1]
       elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
           self.imagem = self.IMGS[2]
       elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
           self.imagem = self.IMGS[1]
       elif self.contagem_imagem < self.TEMPO_ANIMACAO* 4 + 1:
           self.imagem = self.IMGS[0]
           self.contagem_imagem = 0
       # se o passaro estiver caindo eu não vou bater asa
       if self.angulo <= -80:
           self.imagem = self.IMGS[1]
           self.contagem_imagem = self.TEMPO_ANIMACAO * 2
       # desenhar a imagem
       imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
       pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
       retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
       tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano :
    DISTANCIA = 300
    VELOCIDADE = 5
    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.imagem = random.choice(IMAGE_CANO)
        self.CANO_TOPO = pygame.transform.flip(self.imagem, False, True)
        self.CANO_BASE = self.imagem
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask =passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)
        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao :
    VELOCIDADE = 5
    LARGURA = IMAGE_CHAO.get_width()
    IMAGEM = IMAGE_CHAO

    def __init__(self, y):
       self.y = y
       self.x1 = 0
       self.x2 = self.LARGURA

    def mover(self):
       self.x1 -= self.VELOCIDADE
       self.x2 -= self.VELOCIDADE

       if self.x1 + self.LARGURA < 0 :
           self.x1 = self.x2 + self.LARGURA
       if self.x2 + self.LARGURA < 0 :
           self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGE_BACKGROUND,(0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)
    chao.desenhar(tela)
    texto = FONTE_PONTOS.render(f"Pontuação : {pontos}", 1, (255, 255, 255))
    tela.blit(texto,(TELA_LARGURA - 10 - texto.get_width() , 10))
    pygame.display.update()



def main():
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    tela_inicio(tela)
    passaros = [Passaro(200, 250)]
    chao = Chao(550)
    canos = [Cano(500)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)
        #interação com o usuário

        for evento in pygame.event.get():
             if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
             if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                     for passaro in passaros:
                         passaro.pular()
        for passaro in passaros:
            passaro.mover()
        chao.mover()
        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros[:]):
                if cano.colidir(passaro):
                    passaros.pop(i)
                elif not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)
        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros[:]):
            if(passaro.y + passaro.imagem.get_height() > chao.y) or passaro.y < 0:
                passaros.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)

        if len(passaros) == 0:
            tela_inicio(tela)  # Reinicia o jogo ao perder
            main()
            return



if __name__ == '__main__':
    main()













import pyxel

class Jogo:
    def __init__(self):
        pyxel.init(160, 220, title="Eiffel Up", fps=10)
        pyxel.load("eiffel_up.pyxres")

        #váriavel q controla qual tela o jogador ta
        self.estado = "fase1"
        #garante q a troca de fase só aconteça uma vez
        self.mudou_fase = False

        #sistema de vida e dano após colisão dos inimigos
        #o jogador começa com 3.0 vidas
        #float pq o jogo retira meia vida
        self.vidas_max = 3.0
        #armazena quantidade de vida que o jogador tem no momento
        self.vidas_atuais = self.vidas_max
        #qnd o balão encosta em um inimigo, muda p True
        self.invulneravel = False
        #é 0 enquanto o jogador nao sofreu dano
        self.tempo_invulneravel = 0
        #define em fps por segundos o tempo de piscada
        self.DURACAO_INVULNERAVEL = 25

        #variavél do placar de pontos de cada fase
        self.pontos = 0

        #posição do balão na tela
        self.x = 64
        self.y = 185

        #armazena a altura do desenho do balão em pixels 
        # (qnd o balão inteiro sumiu no topo da tela pd mudar de fase)
        self.altura_balao = 35
        self.velocidade = 1 #balão sobe a cada 1 pixel

        #dimensoes do aviao fase 2
        self.aviao_x = 0
        self.aviao_y = 40
        self.aviao_w = 24 
        self.aviao_vel = 2 #se move mais rápido a cada 2 pixels

        #dimensoes dos dois pombos fase 2
        self.pombo_x = 40
        self.pombo_y_inicial = 50 #altura original do pombo
        self.pombo_y = 50 #variável para mudar a posição do pombo 
        self.pombo_w = 14
        self.pombo_h = 22
        
        self.pombo2_x = 110
        self.pombo2_y_inicial = 70
        self.pombo2_y = 70
        self.pombo2_w = 14
        self.pombo2_h = 22

        #sistema de flutuação dos pombos
        #serve p deixar o movimento mais devagar 
        self.contador_flutuacao = 0
        #1 para baixo / -1 para cima
        self.direcao_pombo = 1


        #lista de dicionários, cada um é uma moeda na fase 2
        #quando o balão colide c uma moeda,
        # visivel muda para False e faz a moeda sumir
        self.moedas = [
            {"x": 20, "y": 30, "visivel": True},
            {"x": 80, "y": 45, "visivel": True},
            {"x": 130, "y": 85, "visivel": True}
        ]

        pyxel.run(self.update, self.draw) 

    def update(self): 
        if pyxel.btnp(pyxel.KEY_Q): 
            pyxel.quit() 


        #se as vidas acabarem, interrompe o codigo e parte p Game over
        if self.vidas_atuais <= 0:
            return

        #cconfere se o jogador ta piscando (q daí ele fica um tempo invunelneravel)
        if self.invulneravel:
            #reduz 1 no tempo a cada frame 
            self.tempo_invulneravel -= 1
            #qnd o tempo chega em 0, self.invulneravel volta a ser false e a piscada acaba
            if self.tempo_invulneravel <= 0:
                self.invulneravel = False

        # colisão no balão, usando o x e y e 3 pixels para dentro, 
        #para a colisao nao pegar de tão longe
        balao_col_x = self.x + 3
        balao_col_y = self.y + 3
        balao_col_w = 20
        balao_col_h = 29


        if self.estado == "fase1":
            #movimento das teclas
            if pyxel.btn(pyxel.KEY_LEFT): 
                self.x -= 1 
            if pyxel.btn(pyxel.KEY_RIGHT): 
                self.x += 1

            #o balão não ultrapassa as laterais (0, 128)
            if self.x < 0:
                self.x = 0
            if self.x > 128:
                self.x = 128

            #subida do balão na vertical
            self.y -= self.velocidade

            #balão some no topo da tela  e o jogo muda para fase 2 
            if self.y <= -self.altura_balao and not self.mudou_fase:
                self.estado = "fase2"
                self.mudou_fase = True
                self.y = 120

        elif self.estado == "fase2":
            if pyxel.btn(pyxel.KEY_LEFT): 
                self.x -= 1 
            if pyxel.btn(pyxel.KEY_RIGHT): 
                self.x += 1

            if self.x < 0:
                self.x = 0
            if self.x > 128:
                self.x = 128

            self.y -= self.velocidade

            self.aviao_x += self.aviao_vel

            #faz o aviao andar na horizontal
            if self.aviao_x > 160:
                self.aviao_x = -self.aviao_w

            # delimita a area da moeda em que o balão precisa encostar
            moeda_w, moeda_h = 12, 12

            #loop q passa por cada moeda da lista
            for moeda in self.moedas:
                if moeda["visivel"]:
                    #borda esquerda do balão precisa estar a
                    # esquerda da borda direita da moeda
                    #borda direita do balão precisa estar 
                    #  direita da borda esquerda da moeda
                    #borda superior do balão precisa estar 
                    # acima da borda inferior da moeda
                    #borda inferior do balão precisa estar
                    #  abaixo da borda superior da moeda
                    if (balao_col_x < moeda["x"] + moeda_w and
                        balao_col_x + balao_col_w > moeda["x"] and
                        balao_col_y < moeda["y"] + moeda_h and
                        balao_col_y + balao_col_h > moeda["y"]):
                        moeda["visivel"] = False
                        self.pontos += 10

            self.contador_flutuacao += 1

            #quando o contador chega a 2 ou mais:
            if self.contador_flutuacao >= 2:
                self.contador_flutuacao = 0

                #um pombo some e o outro subtrai, fazendo com q eles façam movimento
                #invertido
                self.pombo_y += self.direcao_pombo
                self.pombo2_y -= self.direcao_pombo

                # se o pombo subir 2 pixels da onde começou, a self direção vira 1
                if self.pombo_y <= self.pombo_y_inicial - 2:
                    self.direcao_pombo = 1
                # e se descer 2 pixels, vira -1
                elif self.pombo_y >= self.pombo_y_inicial + 2:
                    self.direcao_pombo = -1

            # Inimigos
            #mesmo sistema de colisão da moeda com o balão
            if not self.invulneravel:
                if (balao_col_x < self.pombo_x + self.pombo_w - 2 and
                    balao_col_x + balao_col_w > self.pombo_x + 2 and
                    balao_col_y < self.pombo_y + self.pombo_h - 2 and
                    balao_col_y + balao_col_h > self.pombo_y + 2):
                    self.vidas_atuais -= 0.5 #aplica o dano pela metade
                    self.invulneravel = True #enquanto true, ele ignora se o balão colidir dnv com outro inimigo
                    #atribui o valor total de fps por segundos e enqt for maior q zero, reduz -1
                    self.tempo_invulneravel = self.DURACAO_INVULNERAVEL
                
                elif (balao_col_x < self.pombo2_x + self.pombo2_w - 2 and
                      balao_col_x + balao_col_w > self.pombo2_x + 2 and
                      balao_col_y < self.pombo2_y + self.pombo2_h - 2 and
                      balao_col_y + balao_col_h > self.pombo2_y + 2):
                    self.vidas_atuais -= 0.5 
                    self.invulneravel = True
                    self.tempo_invulneravel = self.DURACAO_INVULNERAVEL

                elif (balao_col_x < self.aviao_x + self.aviao_w - 2 and
                      balao_col_x + balao_col_w > self.aviao_x + 2 and
                      balao_col_y < self.aviao_y + 14 and
                      balao_col_y + balao_col_h > self.aviao_y + 2):
                    self.vidas_atuais -= 0.5 
                    self.invulneravel = True
                    self.tempo_invulneravel = self.DURACAO_INVULNERAVEL
            
    def draw(self): 
        #game over
        if self.vidas_atuais <= 0:
            pyxel.cls(0)
            pyxel.text(60, 55, "game over", 8)
            return

        #fase 1
        if self.estado == "fase1":
            pyxel.cls(5) 
            #fundo da tela
            pyxel.blt(0, 0, 1, 0, 24, 160, 120, None)
            pyxel.blt(0, 120, 0, 0, 214, 320, 320, None) 

            #essa função faz com que o balão pique alternadamente se
            #o jogador estiver invulneravel, se for par ele aparece e reaparece a cada frame
            if not self.invulneravel or self.tempo_invulneravel % 2 == 0:
                # balão
                pyxel.blt(self.x, self.y, 0, 67, 0, 26, 35, 6) 

        elif self.estado == "fase2":
            pyxel.cls(12)

            #mesma lógica da fase 1
            if not self.invulneravel or self.tempo_invulneravel % 2 == 0:
                # Balão 
                pyxel.blt(self.x, self.y, 0, 67, 0, 26, 35, 6)

            #cenário do fundo
            pyxel.blt(-1, 15, 1, 90, 144, 320, 320, None)
            pyxel.blt(83, 0, 1, 74, 144, 15, 15, 6)

            #aviao
            pyxel.blt(self.aviao_x, self.aviao_y, 1, 203, 39, 320, 320, 0)

            #pombos
            pyxel.blt(self.pombo_x, self.pombo_y, 0, 17, 0, 14, 22, 0)
            pyxel.blt(self.pombo2_x, self.pombo2_y, 0, 17, 0, 14, 22, 0)

            #percorre a lista e se for true desenha a moeda na tela
            for moeda in self.moedas:
                 if moeda["visivel"]:
                     pyxel.blt(moeda["x"], moeda["y"], 0, 0, 0, 16, 16, 0, scale=0.8)

            #redesenha a moeda para ficar na frente de todos os desenhos
            if not self.invulneravel or self.tempo_invulneravel % 2 == 0:
                 # balão
                 pyxel.blt(self.x, self.y, 0, 67, 0, 26, 35, 6)

        #dimensões do coração
        larg_c = 12 
        alt_c = 12 

        cheio_u, cheio_v   = 94, 0 
        metade_u, metade_v = 106, 0 
        vazio_u, vazio_v   = 118, 0 

        #desenha o placar de pontuação
        pyxel.blt(4, 2, 0, 32, 0, 22, 16, 7)

        #roda 3 vezes
        for i in range(int(self.vidas_max)):
            x_pos = 110 + (i * (larg_c + 4)) #posiciona os corações na horizontal
            y_pos = 2 #altura no topo

            #coração cheio
            if self.vidas_atuais >= i + 1:
                pyxel.blt(x_pos, y_pos, 0, cheio_u, cheio_v, larg_c, alt_c, 0)
            #coração metade
            elif self.vidas_atuais == i + 0.5:
                pyxel.blt(x_pos, y_pos, 0, metade_u, metade_v, larg_c, alt_c, 0)
            #coração vazio
            else:
                pyxel.blt(x_pos, y_pos, 0, vazio_u, vazio_v, larg_c, alt_c, 0)

        #posicionamento do placar de pontuação no desenho
        texto_pontos = f"{self.pontos}"
        x_texto = 16 - (len(texto_pontos) * 2)
        pyxel.text(x_texto, 5, texto_pontos, 0)

Jogo()



        


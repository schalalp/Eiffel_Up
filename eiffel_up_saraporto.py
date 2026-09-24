import pyxel

class Jogo:
    def __init__(self):
        pyxel.init(160, 220, title="Eiffel Up", fps=30)
        pyxel.load("eiffel_up.pyxres")

        #váriavel q controla qual tela o jogador ta
        self.estado = "fase1"
        #garante q a troca de fase só aconteça uma vez
        self.mudou_fase = False

        #sistema de vida e dano após colisão dos inimigos
        self.vidas_max = 3.0
        self.vidas_atuais = self.vidas_max
        self.invulneravel = False
        self.tempo_invulneravel = 0
        self.DURACAO_INVULNERAVEL = 25

        #variavél do placar de pontos de cada fase
        self.pontos = 0

        #posição do balão na tela
        self.x = 64
        self.y = 185

        self.altura_balao = 35
        self.velocidade = 1 

        #dimensoes do aviao fase 2
        self.aviao_x = 0
        self.aviao_y = 40
        self.aviao_w = 24 
        self.aviao_vel = 2 

        #dimensoes dos pombos fase 2
        self.pombo_x = 40
        self.pombo_y_inicial = 70 
        self.pombo_y = 70
        self.pombo_w = 14
        self.pombo_h = 22
        
        self.pombo2_x = 110
        self.pombo2_y_inicial = 20
        self.pombo2_y = 20
        self.pombo2_w = 14
        self.pombo2_h = 22

        self.pombo3_x = 120
        self.pombo3_y_inicial = 160
        self.pombo3_y = 160
        self.pombo3_w = 14
        self.pombo3_h = 22

        #sistema de flutuação dos pombos
        self.contador_flutuacao = 0
        self.direcao_pombo = 1

        # moedas fase 1
        self.moedas_fase1 = [
            {"x": 30, "y": 100, "visivel": True},
            {"x": 100, "y": 30, "visivel": True},
            {"x": 115, "y": 160, "visivel": True},
        ]

        # moedas fase 2
        self.moedas_fase2 = [
            {"x": 20, "y": 15, "visivel": True},
            {"x": 120, "y": 70, "visivel": True},
            {"x": 30, "y": 180, "visivel": True}
        ]

        pyxel.run(self.update, self.draw) 

    def update(self): 
        if pyxel.btnp(pyxel.KEY_Q): 
            pyxel.quit() 

        if self.vidas_atuais <= 0:
            return

        if self.invulneravel:
            self.tempo_invulneravel -= 1
            if self.tempo_invulneravel <= 0:
                self.invulneravel = False

        balao_col_x = self.x + 3
        balao_col_y = self.y + 3
        balao_col_w = 20
        balao_col_h = 29

        if self.estado == "fase1":
            if pyxel.btn(pyxel.KEY_LEFT): 
                self.x -= 1 
            if pyxel.btn(pyxel.KEY_RIGHT): 
                self.x += 1

            if self.x < 0:
                self.x = 0
            if self.x > 128:
                self.x = 128

            self.y -= self.velocidade

            # Colisão moedas 
            for moeda in self.moedas_fase1:
                if moeda["visivel"]:
                    if (balao_col_x < moeda["x"] + 16 and
                        balao_col_x + balao_col_w > moeda["x"] - 1 and
                        balao_col_y < moeda["y"] + 16 and
                        balao_col_y + balao_col_h > moeda["y"] - 1):
                        moeda["visivel"] = False
                        self.pontos += 10

            # colisao nuvens 
            if not self.invulneravel:
                nuv_esq_x, nuv_esq_y, nuv_esq_w, nuv_esq_h = 22, 18, 30, 12
                nuv_dir_x, nuv_dir_y, nuv_dir_w, nuv_dir_h = 102, 18, 30, 15

                if ((balao_col_x < nuv_esq_x + nuv_esq_w and balao_col_x + balao_col_w > nuv_esq_x and
                     balao_col_y < nuv_esq_y + nuv_esq_h and balao_col_y + balao_col_h > nuv_esq_y) or
                    (balao_col_x < nuv_dir_x + nuv_dir_w and balao_col_x + balao_col_w > nuv_dir_x and
                     balao_col_y < nuv_dir_y + nuv_dir_h and balao_col_y + balao_col_h > nuv_dir_y)):
                    
                    self.vidas_atuais -= 0.5 
                    self.invulneravel = True 
                    self.tempo_invulneravel = self.DURACAO_INVULNERAVEL

            if self.y <= -self.altura_balao and not self.mudou_fase:
                self.estado = "fase2"
                self.mudou_fase = True
                self.y = 185

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

            if self.aviao_x > 160:
                self.aviao_x = -self.aviao_w

            # Colisão moedas 
            for moeda in self.moedas_fase2:
                if moeda["visivel"]:
                    if (balao_col_x < moeda["x"] + 16 and
                        balao_col_x + balao_col_w > moeda["x"] - 1 and
                        balao_col_y < moeda["y"] + 16 and
                        balao_col_y + balao_col_h > moeda["y"] - 1):
                        moeda["visivel"] = False
                        self.pontos += 10

            self.contador_flutuacao += 1

            if self.contador_flutuacao >= 2:
                self.contador_flutuacao = 0
                self.pombo_y += self.direcao_pombo
                self.pombo2_y -= self.direcao_pombo
                self.pombo3_y -= self.direcao_pombo 

                if self.pombo_y <= self.pombo_y_inicial - 2:
                    self.direcao_pombo = 1
                elif self.pombo_y >= self.pombo_y_inicial + 2:
                    self.direcao_pombo = -1

            if not self.invulneravel:
                if (balao_col_x < self.pombo_x + self.pombo_w - 2 and
                    balao_col_x + balao_col_w > self.pombo_x + 2 and
                    balao_col_y < self.pombo_y + self.pombo_h - 2 and
                    balao_col_y + balao_col_h > self.pombo_y + 2):
                    self.vidas_atuais -= 0.5 
                    self.invulneravel = True 
                    self.tempo_invulneravel = self.DURACAO_INVULNERAVEL
                
                elif (balao_col_x < self.pombo2_x + self.pombo2_w - 2 and
                      balao_col_x + balao_col_w > self.pombo2_x + 2 and
                      balao_col_y < self.pombo2_y + self.pombo2_h - 2 and
                      balao_col_y + balao_col_h > self.pombo2_y + 2):
                    self.vidas_atuais -= 0.5 
                    self.invulneravel = True
                    self.tempo_invulneravel = self.DURACAO_INVULNERAVEL

                elif (balao_col_x < self.pombo3_x + self.pombo3_w - 2 and
                      balao_col_x + balao_col_w > self.pombo3_x + 2 and
                      balao_col_y < self.pombo3_y + self.pombo3_h - 2 and
                      balao_col_y + balao_col_h > self.pombo3_y + 2):
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
        if self.vidas_atuais <= 0:
            pyxel.cls(0)
            pyxel.text(60, 55, "game over", 8)
            return

        if self.estado == "fase1":
            pyxel.cls(5) 
            pyxel.blt(0, 0, 1, 0, 24, 160, 120, None) 
            pyxel.blt(0, 120, 0, 0, 214, 320, 320, None) 
            pyxel.blt(0,160,0,0,154,320,320,None)

            # desenha as moedas da Fase 1
            for moeda in self.moedas_fase1:
                if moeda["visivel"]:
                    pyxel.blt(moeda["x"], moeda["y"], 0, 0, 0, 15, 16, 15)

            if not self.invulneravel or self.tempo_invulneravel % 2 == 0:
                pyxel.blt(self.x, self.y, 0, 67, 0, 26, 35, 6) 

        elif self.estado == "fase2":
            pyxel.cls(12)

            pyxel.blt(-1, 108, 1, 90, 144, 320, 320, None)
            pyxel.blt(83, 0, 1, 74, 144, 15, 100, 6)
            pyxel.blt(83, 98, 1, 74, 144, 15, 15, 6)

            pyxel.blt(self.aviao_x, self.aviao_y, 1, 203, 39, 320, 70, 0)

            pyxel.blt(self.pombo_x, self.pombo_y, 0, 17, 0, 14, 22, 0)
            pyxel.blt(self.pombo2_x, self.pombo2_y, 0, 17, 0, 14, 22, 0)
            pyxel.blt(self.pombo3_x, self.pombo3_y, 0, 17, 0, 14, 22, 0)

            # desenha as moedas da Fase 2
            for moeda in self.moedas_fase2:
                if moeda["visivel"]:
                    pyxel.blt(moeda["x"], moeda["y"], 0, 0, 0, 15, 16, 15)

            if not self.invulneravel or self.tempo_invulneravel % 2 == 0:
                pyxel.blt(self.x, self.y, 0, 67, 0, 26, 35, 6)

        # dimensões do coração
        larg_c = 12 
        alt_c = 12 

        cheio_u, cheio_v   = 94, 0 
        metade_u, metade_v = 106, 0 
        vazio_u, vazio_v   = 118, 0 

        pyxel.blt(4, 2, 0, 32, 0, 22, 16, 7)

        for i in range(int(self.vidas_max)):
            x_pos = 110 + (i * (larg_c + 4)) 
            y_pos = 2 

            if self.vidas_atuais >= i + 1:
                pyxel.blt(x_pos, y_pos, 0, cheio_u, cheio_v, larg_c, alt_c, 0)
            elif self.vidas_atuais == i + 0.5:
                pyxel.blt(x_pos, y_pos, 0, metade_u, metade_v, larg_c, alt_c, 0)
            else:
                pyxel.blt(x_pos, y_pos, 0, vazio_u, vazio_v, larg_c, alt_c, 0)

        texto_pontos = f"{self.pontos}"
        x_texto = 16 - (len(texto_pontos) * 2)
        pyxel.text(x_texto, 5, texto_pontos, 0)

Jogo()

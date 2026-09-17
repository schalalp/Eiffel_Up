import pyxel

class Jogo:
    def __init__(self):
        pyxel.init(160, 120, title="Eiffel Up", fps=10)
        pyxel.load("eiffel_up.pyxres")

        self.estado = "fase1"
        self.mudou_fase = False

        self.vidas_max = 3.0
        self.vidas_atuais = self.vidas_max
        self.invulneravel = False
        self.tempo_invulneravel = 0
        self.DURACAO_INVULNERAVEL = 25

        self.pontos = 0

        self.x = 64
        self.y = 70

        self.altura_balao = 35
        self.velocidade = 1

        self.aviao_x = 0
        self.aviao_y = 40
        self.aviao_w = 24
        self.aviao_vel = 2

        self.pombo_x = 40
        self.pombo_y_inicial = 50
        self.pombo_y = 50
        self.pombo_w = 14
        self.pombo_h = 22
        
        self.pombo2_x = 110
        self.pombo2_y_inicial = 70
        self.pombo2_y = 70
        self.pombo2_w = 14
        self.pombo2_h = 22

        self.contador_flutuacao = 0
        self.direcao_pombo = 1

        self.moedas = [
            {"x": 20, "y": 30, "visivel": True},
            {"x": 80, "y": 45, "visivel": True},
            {"x": 130, "y": 85, "visivel": True}
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

        # Definindo hitbox real e enxuta do balão (com margem de tolerância)
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

            if self.aviao_x > 160:
                self.aviao_x = -self.aviao_w

            # Colisão com Moedas (Hitbox menor e mais justa)
            moeda_w, moeda_h = 12, 12

            for moeda in self.moedas:
                if moeda["visivel"]:
                    if (balao_col_x < moeda["x"] + moeda_w and
                        balao_col_x + balao_col_w > moeda["x"] and
                        balao_col_y < moeda["y"] + moeda_h and
                        balao_col_y + balao_col_h > moeda["y"]):
                        moeda["visivel"] = False
                        self.pontos += 10

            self.contador_flutuacao += 1
            
            if self.contador_flutuacao >= 2:
                self.contador_flutuacao = 0
                self.pombo_y += self.direcao_pombo
                self.pombo2_y -= self.direcao_pombo
                
                if self.pombo_y <= self.pombo_y_inicial - 2:
                    self.direcao_pombo = 1
                elif self.pombo_y >= self.pombo_y_inicial + 2:
                    self.direcao_pombo = -1

            # Colisão com Inimigos
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

            if not self.invulneravel or self.tempo_invulneravel % 2 == 0:
                # Balão com transparência 6
                pyxel.blt(self.x, self.y, 0, 67, 0, 26, 35, 6) 

        elif self.estado == "fase2":
            pyxel.cls(12)

            if not self.invulneravel or self.tempo_invulneravel % 2 == 0:
                # Balão com transparência 6
                pyxel.blt(self.x, self.y, 0, 67, 0, 26, 35, 6)

            pyxel.blt(-1, 15, 1, 90, 144, 320, 320, None)
            pyxel.blt(83, 0, 1, 74, 144, 15, 15, 6)

            pyxel.blt(self.aviao_x, self.aviao_y, 1, 203, 39, 320, 320, 0)

            pyxel.blt(self.pombo_x, self.pombo_y, 0, 17, 0, 14, 22, 0)
            pyxel.blt(self.pombo2_x, self.pombo2_y, 0, 17, 0, 14, 22, 0)

            for moeda in self.moedas:
                 if moeda["visivel"]:
                     pyxel.blt(moeda["x"], moeda["y"], 0, 0, 0, 16, 16, 0, scale=0.8)

            if not self.invulneravel or self.tempo_invulneravel % 2 == 0:
                 # Balão com transparência 6
                 pyxel.blt(self.x, self.y, 0, 67, 0, 26, 35, 6)

        LARG_C = 12 
        ALT_C = 12 

        CHEIO_U, CHEIO_V   = 94, 0 
        METADE_U, METADE_V = 106, 0 
        VAZIO_U, VAZIO_V   = 118, 0 

        pyxel.blt(4, 2, 0, 32, 0, 22, 16, 7)

        for i in range(int(self.vidas_max)):
            x_pos = 110 + (i * (LARG_C + 4))
            y_pos = 2 
            
            if self.vidas_atuais >= i + 1:
                pyxel.blt(x_pos, y_pos, 0, CHEIO_U, CHEIO_V, LARG_C, ALT_C, 0)
                    
            elif self.vidas_atuais == i + 0.5:
                pyxel.blt(x_pos, y_pos, 0, METADE_U, METADE_V, LARG_C, ALT_C, 0)
                
            else:
                pyxel.blt(x_pos, y_pos, 0, VAZIO_U, VAZIO_V, LARG_C, ALT_C, 0)

        texto_pontos = f"{self.pontos}"
        x_texto = 16 - (len(texto_pontos) * 2)
        pyxel.text(x_texto, 5, texto_pontos, 0)

Jogo()

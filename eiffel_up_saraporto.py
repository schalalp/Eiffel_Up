import pyxel

class Jogo:
    def __init__(self):
        pyxel.init(160, 120, title="Eiffel Up", fps=10)
        pyxel.load("eiffel_up.pyxres")

        #guarda a parte em que estamos no jogo
        self.estado = "fase1"
        #p trocar de fase uma vez só 
        self.mudou_fase = False

        # sistema de matade da vida 

        self.vidas_max = 3.0
        self.vidas_atuais = self.vidas_max
        self.invulneravel = False
        self.tempo_invulneravel = 0
        self.DURACAO_INVULNERAVEL = 25 #2.5 segundos

        #balão 
        self.x = 64
        self.y = 70

        #p calcular qnd ele subir na tela ate o topo
        self.altura_balao = 35
        self.velocidade = 1

        self.moedas = [
            {"x":10, "y":20, "visivel": True},
            {"x": 50, "y": 40, "visivel": True},
            {"x": 125, "y": 52, "visivel": True}
         ]

        pyxel.run(self.update, self.draw) 

    def update(self): 
        if pyxel.btnp(pyxel.KEY_Q): 
            pyxel.quit() 

        # game
        if self.vidas_atuais <= 0:
            return

        #piscada de dano do balão
        if self.invulneravel:
            self.tempo_invulneravel -= 1
            if self.tempo_invulneravel <= 0:
                self.invulneravel = False

         # tudo q ta dentro desse if só roda se self.estado for == "fase"
        if self.estado == "fase1":

           # define largura e altura do balao e da moeda p facilitar no cálculo da colisao
            balao_w, balao_h = 29, 35
            moeda_w, moeda_h = 4, 9

            # define largura e altura da abelha p facilitar no cálculo da colisao
            abe_x, abe_y, abe_w, abe_h = 23, 23, 23, 23

            if not self.invulneravel:
                if (self.x < abe_x + abe_w and
                    self.x + balao_w > abe_x and
                    self.y < abe_y + abe_h and
                    self.y + balao_h > abe_y):
                                
                    self.vidas_atuais -= 0.5  # tira metade de um coração
                    self.invulneravel = True
                    self.tempo_invulneravel = self.DURACAO_INVULNERAVEL

            #esse for passa por cada  moeda da lista, verifica se o retangulo da moeda ta sobrepondo o retangulo do balão
            #se ta sobrepondo, ela some do jogo (deixa de ser desenhada)
            for moeda in self.moedas:
                if moeda["visivel"]:
                    if (self.x < moeda["x"] + moeda_w and
                        self.x + balao_w > moeda["x"] and
                        self.y < moeda["y"] + moeda_h and
                        self.y + balao_h > moeda["y"]):
                        moeda["visivel"] = False

            if pyxel.btn(pyxel.KEY_LEFT): 
                self.x -= 1 
            if pyxel.btn(pyxel.KEY_RIGHT): 
                self.x += 1

            if self.x < 0:
                self.x = 0
            if self.x > 128:
                self.x = 128

            self.y -= self.velocidade

            #aq acontece a troca de fase, ou seja, só muda a fase qnd o balao ja saiu da tela por cima
            #e o not self.mudou_fase vai fazer com q só rode uma vez a fase 
            if self.y <= -self.altura_balao and not self.mudou_fase:
                self.estado = "fase2"
                self.mudou_fase = True
                self.y = 120

        #repete a mesma logica de movimento da fase 1
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

    def draw(self): 
        # tela de game over 
        if self.vidas_atuais <= 0:
            pyxel.cls(0)
            pyxel.text(60, 55, "game over", 8)
            return

        if self.estado == "fase1":
            pyxel.cls(5) 

            #desenha torre eiffel
            pyxel.blt(0, 0, 1, 0, 24, 160, 120, None)  # background fase 1

            #desenha moeda
            #for moeda in self.moedas:
             #   if moeda["visivel"]:
              #      pyxel.blt(moeda["x"], moeda["y"], 0, 0, 0, 16, 16, 0, scale=0.8)

            #desenha abelha
            #pyxel.blt(15, 60, 0, 31, 2, 32, 32, 0)

            #pyxel.blt(110, 10, 0, 31, 2, 32, 32, 0)
            

            # desenha a piscada no balão
            if not self.invulneravel or self.tempo_invulneravel % 2 == 0:
                #desenha o balão
                pyxel.blt(self.x, self.y, 0, 67, 0, 26, 35, 0) 

        elif self.estado == "fase2":
            pyxel.cls(12)

            # desenha a piscada no balão
            if not self.invulneravel or self.tempo_invulneravel % 2 == 0:
                #desenha o balão
                pyxel.blt(self.x, self.y, 0, 67, 0, 26, 35, 0)

            #desenha torre eiffel
            pyxel.blt(60, 0, 1, 160 ,24, 350, 320, 0)

            #desenha pombo
            pyxel.blt(30, 30, 0, 17, 0, 14, 22, 0)

        # sistema dos corações
        LARG_C = 12          # X
        ALT_C = 12           # Y

        #  coordenadas
        CHEIO_U, CHEIO_V   = 94, 0    # Coração cheio (94, 0)
        METADE_U, METADE_V = 106, 0    # Coração na metade (106,0)
        VAZIO_U, VAZIO_V   = 118, 0    # Coração vazio (118, 0)

        for i in range(int(self.vidas_max)):
            x_pos = 110 + (i * (LARG_C+ 4))
            y_pos = 2 
            
            if self.vidas_atuais >= i + 1:
                #desenha os corações
                pyxel.blt(x_pos, y_pos, 0, CHEIO_U, CHEIO_V, LARG_C, ALT_C, 0)
                    
            elif self.vidas_atuais == i + 0.5:
                pyxel.blt(x_pos, y_pos, 0, METADE_U, METADE_V, LARG_C, ALT_C, 0)
                
            else:
                pyxel.blt(x_pos, y_pos, 0, VAZIO_U, VAZIO_V, LARG_C, ALT_C, 0)

Jogo()
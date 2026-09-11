import pyxel

class Jogo: 
    def __init__(self): 
        pyxel.init(160, 120, title="Eiffel Up", fps=10) 
        pyxel.load("eiffel_up.pyxres") 

        # guarda a parte em que estamos no jogo
        self.estado = "fase1"
        # p fazer a troca de fase uma vez só
        self.mudou_fase = False

        #balão
        self.x = 64 
        self.y = 70 
        # p calcular qnd ele subir na tela ate o topo
        self.altura_balao = 35
        self.velocidade = 1 

        self.moedas = [
            {"x": 20, "y": 20, "visivel": True},
            {"x": 50, "y": 40, "visivel": True},
            {"x": 80, "y": 52, "visivel": True}
        ]

        pyxel.run(self.update, self.draw) 

    def update(self): 
        if pyxel.btnp(pyxel.KEY_Q): 
            pyxel.quit() 

        # tudo q ta dentro desse if só roda se self.estado for == "fase"
        if self.estado == "fase1":
            #define largura e altura do balao e da moeda p facilitar no cálculo da colisao
            balao_w, balao_h = 29, 35
            moeda_w, moeda_h = 13, 13

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
        if self.estado == "fase1":
            pyxel.cls(12) 

            pyxel.blt(90, 136, 1, 1, 255, 16, 16, 0)
            
            for moeda in self.moedas:
                if moeda["visivel"]:
                    pyxel.blt(moeda["x"], moeda["y"], 0, 0, 0, 16, 16, 0, scale=0.8)

            pyxel.blt(self.x, self.y, 0, 67, 0, 29, 35, 0) 

            pyxel.blt(90, 136, 1, 0, 232, 128, 128, 0, scale=2.0)

        elif self.estado == "fase2":
            pyxel.cls(12)
            pyxel.blt(self.x, self.y, 0, 67, 0, 29, 35, 0)

Jogo()
        

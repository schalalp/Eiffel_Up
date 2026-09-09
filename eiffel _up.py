import pyxel

class Jogo: 
    def __init__(self): 
        pyxel.init(160, 120, title="Eiffel Up", fps=10) 
        pyxel.load("eiffel_up.pyxres") 
        #tentativa png
        ##pyxel.images[1].load(65,71, "gabriel2.png")

        # Balão
        self.x = 64 
        self.y = 70 
        self.velocidade = 1 

        self.moedas = [[20, 12, True], [50, 25, True], [120, 10, True]]

        pyxel.run(self.update, self.draw) 

    def update(self): 
        if pyxel.btnp(pyxel.KEY_Q): 
            pyxel.quit() 

        # Controles do balão
        if pyxel.btn(pyxel.KEY_LEFT): 
            self.x -= 2 
        if pyxel.btn(pyxel.KEY_RIGHT): 
            self.x += 2 

        # Limites das laterais
        if self.x < 0:
            self.x = 0
        if self.x > 128:
            self.x = 128

        # Balão sobe
        if self.y > -32: 
            self.y -= self.velocidade

        #Colisão das moedas
        for i range(len(self.moedas)):


    def draw(self): 
        # Fundo azul 
        pyxel.cls(12) 

        # 3 moedas fixas na tela (banco 0, u=0, v=0, tamanho 16x16)
        pyxel.blt(20, 12, 0, 0, 0, 16, 16, 0)
        pyxel.blt(50, 25, 0, 0, 0, 16, 16, 0)
        pyxel.blt(120, 10, 0, 0, 0, 16, 16, 0)


        ##pyxel.blt(self.x, self.y, 1, 50, 50, 64, 64, 0)

        #Desenha o balão
        if self.y > -32:
            pyxel.blt(self.x, self.y, 0, 67, 0, 29, 35, 0) 

Jogo()

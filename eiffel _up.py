import pyxel

class Jogo: 
    def __init__(self): 
        pyxel.init(160, 120, title="Eiffel Up", fps=10) 
        pyxel.load("eiffel_up.pyxres") 

        #balão
        self.x = 64 
        self.y = 70 
        self.velocidade = 1 

        
        self.moedas = [
            {"x": 20, "y": 12, "visivel": True},
            {"x": 50, "y": 25, "visivel": True},
            {"x": 120, "y": 10, "visivel": True}
        ]

        pyxel.run(self.update, self.draw) 

    def update(self): 
        if pyxel.btnp(pyxel.KEY_Q): 
            pyxel.quit() 

        # cxontroles do balão
        if pyxel.btn(pyxel.KEY_LEFT): 
            self.x -= 2 
        if pyxel.btn(pyxel.KEY_RIGHT): 
            self.x += 2 

        # limites das laterais
        if self.x < 0:
            self.x = 0
        if self.x > 128:
            self.x = 128

        # balão sobe
        if self.y > -32: 
            self.y -= self.velocidade

    
        # se o balão encostou na moeda
        for moeda in self.moedas:
            if moeda["visivel"]:
                
                if abs(self.x - moeda["x"]) < 16 and abs(self.y - moeda["y"]) < 16:
                    moeda["visivel"] = False 

    def draw(self): 
        pyxel.cls(12) 

        #  desenhar as moedas que ainda estão visiveis
        for moeda in self.moedas:
            if moeda["visivel"]:
                pyxel.blt(moeda["x"], moeda["y"], 0, 0, 0, 16, 16, 0)

        # desenha o balão
        if self.y > -32:
            pyxel.blt(self.x, self.y, 0, 67, 0, 29, 35, 0) 

Jogo()

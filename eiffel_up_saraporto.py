import pyxel
import math 
import random

class Jogo:
    def __init__(self):
        pyxel.init(160, 220, title="Eiffel Up", fps=30)
        pyxel.load("eiffel_up.pyxres")


        pyxel.image(2).load(0, 0, "fundo_fase_3_4.jpg")
        pyxel.image(2).load(160, 0, "planeta.png")

        #Váriavel que controla qual tela o jogador esta
        self.estado = "inicio"

        self.opcao_menu = 0
        self.personagem = "gabriel"

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
        self.aviao_w = 43
        self.aviao_h = 22
        self.aviao_vel = 0.5

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

        #dimensões dos meteoros fase 3

        self.meteoro_x = 0
        self.meteoro_y = 40
        self.meteoro_w = 45
        self.meteoro_h = 40
        self.meteoro_vel = 1

        self.meteoro2_x = 160
        self.meteoro2_y = 120
        self.meteoro2_w = 40
        self.meteoro2_h = 40
        self.meteoro2_vel = 1

        #dimensões do satélite fase 4
        self.satelite_x= 125
        self.satelite_y= 40
        self.satelite_w= 44
        self.satelite_h= 44
        self.satelite_vel= 1 

    
        # Estrela inimiga da fase 4
        self.estrela_x = 20.0
        self.estrela_y = 20.0
        self.estrela_w = 18
        self.estrela_h = 24

        # Velocidade vetorial da estrela
        self.estrela_vx = 0.0
        self.estrela_vy = 0.0

        # Parâmetros da perseguição
        self.estrela_aceleracao = 0.08
        self.estrela_vel_max = 1.5

        # Tempo para reposicionar a estrela
        self.estrela_timer = 240  

        #Dimensões Ovni
        self.ovni_x = 2
        self.ovni_y = 0        
        self.ovni_w = 40
        self.ovni_h = 32
        self.ovni_vel = 1
        self.ovni_dir = 1      

        #Tiros
        self.tiro = None         # n existe tiro na tela
        self.tiro_w = 6  
        self.tiro_h = 3
        self.tiro_vel = 4
        self.tiro_intervalo = 25  # frames de espera até o próximo tiro (30 fps = 0,5 s)
        self.tiro_seguinte = self.tiro_intervalo

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

        # moedas fase 3 ( rosa)
        self.moedas_fase3 = [
            {"x": 20, "y": 15, "visivel": True},
            {"x": 120, "y": 70, "visivel": True},
            {"x": 30, "y": 180, "visivel": True}
                ]

        # moedas fase 4 (rosa)
        self.moedas_fase4 = [
            {"x": 20, "y": 60, "visivel": True},
            {"x": 100, "y": 100, "visivel": True}
        ]

        #moedas Fase 5 (verde)
        self.moedas_fase5 = [
            {"x": 115, "y": 24, "visivel": True},
            {"x": 44, "y": 120, "visivel": True}
        ]

        #moedas Fase 6 (verde)
        self.moedas_fase6 = [
            {"x": 32, "y": 66, "visivel": True},
            {"x": 86, "y": 165, "visivel": True}
        ]

        pyxel.run(self.update, self.draw) 

    # função colisao

    def colide(self, a, b):
        # a e b são retângulos no formato (x, y, largura, altura)
        return (a[0] < b[0] + b[2] and a[0] + a[2] > b[0] and
                a[1] < b[1] + b[3] and a[1] + a[3] > b[1])

    def tomar_dano(self):
        self.vidas_atuais -= 0.5
        self.invulneravel = True
        self.tempo_invulneravel = self.DURACAO_INVULNERAVEL

    def pegar_moedas(self, moedas, balao, valor=10):
        for m in moedas:
            if m["visivel"] and self.colide(balao, (m["x"] - 1, m["y"] - 1, 17, 17)):
                m["visivel"] = False
                self.pontos += valor

   # MOVIMENTO VETORIAL DA ESTRELA  

    def mover_estrela(self):
        # Centro aproximado do balão
        alvo_x = self.x + 13
        alvo_y = self.y + 17

        # Vetor da estrela até o balão
        dx = alvo_x - self.estrela_x
        dy = alvo_y - self.estrela_y

        # Distância entre estrela e balão
        distancia = math.sqrt(dx**2 + dy**2)

        # Aceleração gradual na direção do balão
        if distancia > 0:
            self.estrela_vx += (
                dx / distancia
            ) * self.estrela_aceleracao

            self.estrela_vy += (
                dy / distancia
            ) * self.estrela_aceleracao

        # Velocidade total
        velocidade = math.sqrt(
            self.estrela_vx**2
            + self.estrela_vy**2
        )

        # Limita a velocidade máxima
        if velocidade > self.estrela_vel_max:
            fator = self.estrela_vel_max / velocidade

            self.estrela_vx *= fator
            self.estrela_vy *= fator

        # Movimento com inércia
        self.estrela_x += self.estrela_vx
        self.estrela_y += self.estrela_vy

        # Limites da tela
        self.estrela_x = max(
            0, min(144, self.estrela_x)
        )

        self.estrela_y = max(
            0, min(204, self.estrela_y)
        )

    # REPOSICIONAMENTO DA ESTRELA

    def reposicionar_estrela(self):
        # Escolhe um dos lados da tela
        lado = random.choice([0, 1])

        if lado == 0:
            self.estrela_x = 0.0
        else:
            self.estrela_x = 144.0

        # Aparece próximo à trajetória do balão
        self.estrela_y = float(
            max(
                0,
                min(
                    204,
                    self.y + random.randint(-50, 50)
                )
            )
        )

        # Reinicia a velocidade
        self.estrela_vx = 0.0
        self.estrela_vy = 0.0

        # Reinicia o temporizador
        self.estrela_timer = 240

    def atirar(self):
        # nasce no meio do lado direito do ovni
        self.tiro = {
            "x": self.ovni_x + self.ovni_w,
            "y": self.ovni_y + self.ovni_h / 2 - self.tiro_h / 2,
        }

    def atualizar_ovni(self, balao):
        # sobe e desce sem sair da tela
        self.ovni_y += self.ovni_vel * self.ovni_dir

        if self.ovni_y <= 0:
            self.ovni_y = 0
            self.ovni_dir = 1
        elif self.ovni_y >= 220 - self.ovni_h:
            self.ovni_y = 220 - self.ovni_h
            self.ovni_dir = -1

        # se não há tiro, conta a espera e atira
        if self.tiro is None:
            self.tiro_seguinte -= 1
            if self.tiro_seguinte <= 0:
                self.atirar()
                self.tiro_seguinte = self.tiro_intervalo
        else:
            # tiro vai para a direita
            self.tiro["x"] += self.tiro_vel

            hitbox_tiro = (self.tiro["x"], self.tiro["y"],
                           self.tiro_w, self.tiro_h)

            if self.colide(balao, hitbox_tiro):
                if not self.invulneravel:
                    self.tomar_dano()
                self.tiro = None
            elif self.tiro["x"] > 160:
                self.tiro = None
    
    def update(self): 
        if pyxel.btnp(pyxel.KEY_Q): 
            pyxel.quit() 

        if self.vidas_atuais <= 0:
            return

        if self.estado == "inicio":
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
                self.estado = "menu"
            return

        if self.estado == "menu":
            if pyxel.btnp(pyxel.KEY_LEFT):
                self.opcao_menu = 0
            if pyxel.btnp(pyxel.KEY_RIGHT):
                self.opcao_menu = 1

            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
                if self.opcao_menu == 0:
                    self.personagem = "gabriel"
                else:
                    self.personagem = "sara"
                self.estado = "fase1"
            return

        if self.invulneravel:
            self.tempo_invulneravel -= 1
            if self.tempo_invulneravel <= 0:
                self.invulneravel = False

        # hitbox do balão (x, y, largura, altura)
        balao = (self.x + 3, self.y + 3, 20, 29)

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

            self.pegar_moedas(self.moedas_fase1, balao)

            if not self.invulneravel:
                nuvens = [(22, 18, 30, 12), (102, 18, 30, 15)]
                if any(self.colide(balao, n) for n in nuvens):
                    self.tomar_dano()

            if self.y <= -self.altura_balao:
                self.estado = "fase2"
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

            self.pegar_moedas(self.moedas_fase2, balao)

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
                inimigos = [
                    (self.pombo_x + 4,  self.pombo_y + 2,  self.pombo_w - 8,  self.pombo_h - 4),
                    (self.pombo2_x + 4, self.pombo2_y + 2, self.pombo2_w - 8, self.pombo2_h - 4),
                    (self.pombo3_x + 4, self.pombo3_y + 2, self.pombo3_w - 8, self.pombo3_h - 4),
                    (self.aviao_x + 3,  self.aviao_y + 3,  self.aviao_w - 6,  self.aviao_h - 6),
                ]
                if any(self.colide(balao, i) for i in inimigos):
                    self.tomar_dano()

            if self.y <= -self.altura_balao:
                self.estado = "fase3"
                self.y = 185

        elif self.estado == "fase3":
            if pyxel.btn(pyxel.KEY_LEFT): 
                self.x -= 1 
            if pyxel.btn(pyxel.KEY_RIGHT): 
                self.x += 1

            if self.x < 0:
                self.x = 0
            if self.x > 128:
                self.x = 128

            self.y -= self.velocidade

            self.meteoro_x += self.meteoro_vel
            self.meteoro2_x -= self.meteoro2_vel
            
            if self.meteoro_x > 160:
                self.meteoro_x = -self.meteoro_w

            if self.meteoro2_x < -self.meteoro2_w:
                self.meteoro2_x = 160

            self.pegar_moedas(self.moedas_fase3, balao,50)

            if not self.invulneravel:
                meteoros = [
                    (self.meteoro_x + 7, self.meteoro_y + 4, self.meteoro_w - 14, self.meteoro_h - 8 ),
                    (self.meteoro2_x + 7, self.meteoro2_y + 4, self.meteoro2_w - 14, self.meteoro2_h - 8 )
                ]

                if any(self.colide(balao, m) for m in meteoros):
                    self.tomar_dano()


          # Passagem para a fase 4
            if self.y <= -self.altura_balao:
                self.estado = "fase4"
                self.y = 185

                # Posição inicial da estrela: (20, 20)
                self.estrela_x = 20.0
                self.estrela_y = 20.0

                self.estrela_vx = 0.0
                self.estrela_vy = 0.0
                self.estrela_timer = 240

        elif self.estado == "fase4":

            # Movimento do balão
            if pyxel.btn(pyxel.KEY_LEFT):
                self.x -= 1

            if pyxel.btn(pyxel.KEY_RIGHT):
                self.x += 1

            self.x = max(0, min(128, self.x))

            self.y -= self.velocidade

            

            #Movimento do satélite
            self.satelite_x -= 1
            self.satelite_y += 1

            if self.satelite_x < -44 or self.satelite_y > 220:
                self.satelite_x= 160
                self.satelite_y= 40

            # Coleta das moedas rosas da fase 4
            self.pegar_moedas(self.moedas_fase4, balao, 50)

            # Colisão com o satélite
            satelite = (
                self.satelite_x + 4,
                self.satelite_y + 4,
                self.satelite_w - 8,
                self.satelite_h - 8
            )

            if not self.invulneravel:
                if self.colide(balao, satelite):
                    self.tomar_dano()    

            # Movimento vetorial da estrela
            self.mover_estrela()

            # Reaparecimento periódico
            self.estrela_timer -= 1

            if self.estrela_timer <= 0:
                self.reposicionar_estrela()

            # Hitbox da estrela
            estrela = (
                int(self.estrela_x) + 2, int(self.estrela_y) + 2, self.estrela_w - 4, self.estrela_h - 4)

            # Colisão com o balão
            if not self.invulneravel:
                if self.colide(balao, estrela):
                    self.tomar_dano()

            if self.y <= -self.altura_balao:
                self.estado = "fase5"
                self.y = 185

        elif self.estado == "fase5":
            if pyxel.btn(pyxel.KEY_LEFT): 
                self.x -= 1 
            if pyxel.btn(pyxel.KEY_RIGHT): 
                self.x += 1
        
            if self.x < 0:
                 self.x = 0
            if self.x > 128:
                self.x = 128
        
            self.y -= self.velocidade
        
            # Coleta das moedas verdes da Fase 5
            self.pegar_moedas(self.moedas_fase5, balao, 100)

            # Passagem para a fase 6
            if self.y <= -self.altura_balao:
                self.estado = "fase6"
                self.y = 185
            

        elif self.estado == "fase6":
            if pyxel.btn(pyxel.KEY_LEFT): 
                self.x -= 1 
            if pyxel.btn(pyxel.KEY_RIGHT): 
                self.x += 1

            if self.x < 0:
                self.x = 0
            if self.x > 128:
                self.x = 128

            self.y -= self.velocidade

            self.atualizar_ovni(balao)

            # Coleta das moedas verdes da Fase 6
            self.pegar_moedas(self.moedas_fase6, balao, 100)

            # Colisão do balão com o corpo do ovni
            ovni = (
                self.ovni_x + 3,
                self.ovni_y + 3,
                self.ovni_w - 6,
                self.ovni_h - 6
            )

            if not self.invulneravel:
                if self.colide(balao, ovni):
                    self.tomar_dano()

           

        

    def draw(self): 
        if self.vidas_atuais <= 0:
            pyxel.cls(0)
            pyxel.text(60, 55, "game over", 8)
            return

        if self.estado == "inicio":
            pyxel.cls(5)

            # título centralizado (cada letra do pyxel.text tem 4 px de largura)
            titulo = "EIFFEL UP"
            pyxel.text(80 - len(titulo) * 2, 70, titulo, 7)

            # balão enfeitando a tela
            pyxel.blt(67, 100, 0, 67, 0, 26, 35, 6)

            # texto piscando
            if pyxel.frame_count % 30 < 20:
                aviso = "START"
                pyxel.text(80 - len(aviso) * 2, 160, aviso, 7)

            return

        if self.estado == "menu":
            pyxel.cls(5)

            titulo = "ESCOLHA SEU PERSONAGEM"
            pyxel.text(80 - len(titulo) * 2, 40, titulo, 7)

            pyxel.blt(34, 90, 0, 67, 0, 26, 35, 6)
            pyxel.blt(100, 90, 0, 91, 48, 26, 35, 6)

            pyxel.text(47 - len("GABRIEL") * 2, 135, "GABRIEL", 7)
            pyxel.text(113 - len("SARA") * 2, 135, "SARA", 7)

            if self.opcao_menu == 0:
                pyxel.rectb(28, 84, 38, 47, 7)
            else:
                pyxel.rectb(94, 84, 38, 47, 7)

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

            pyxel.blt(int(self.aviao_x), self.aviao_y, 1, 203, 39, 320, 70, 0)

            pyxel.blt(self.pombo_x, self.pombo_y, 0, 17, 0, 14, 22, 0)
            pyxel.blt(self.pombo2_x, self.pombo2_y, 0, 17, 0, 14, 22, 0)
            pyxel.blt(self.pombo3_x, self.pombo3_y, 0, 17, 0, 14, 22, 0)

            # desenha as moedas da Fase 2
            for moeda in self.moedas_fase2:
                if moeda["visivel"]:
                    pyxel.blt(moeda["x"], moeda["y"], 0, 0, 0, 15, 16, 15)

            if not self.invulneravel or self.tempo_invulneravel % 2 == 0:
                pyxel.blt(self.x, self.y, 0, 67, 0, 26, 35, 6)

        elif self.estado == "fase3":
            pyxel.cls(0)

            pyxel.blt(0, 0, 2, 0, 0, 160, 220)
            
            pyxel.blt(105, 153, 0, 205, 190, 600,600,0)
            pyxel.blt(self.meteoro_x, self.meteoro_y, 0, 204, 97, 45, 40, 0)
            pyxel.blt(self.meteoro2_x, self.meteoro2_y, 0, 210, 43, 40, 40, 0)
            
            if not self.invulneravel or self.tempo_invulneravel % 2 == 0:
                pyxel.blt(self.x, self.y, 0, 67, 0, 26, 35, 6)

            for moeda in self.moedas_fase3:
                if moeda["visivel"]:
                    pyxel.blt(moeda["x"], moeda["y"], 0, 0, 24, 15, 16, 15)


        #fase 4
        elif self.estado == "fase4":

            pyxel.cls(0)

            # Fundo
            pyxel.blt(
                0, 0, 2,
                0, 0,
                160, 220
            ) 

            pyxel.blt(self.satelite_x, self.satelite_y, 0, 33, 80, 44, 44, 0)

            pyxel.blt(
                        int(self.estrela_x),
                        int(self.estrela_y),
                        0,       
                        32, 38,  
                        18, 20,  
                        7   
                    )

            
            # Balão
            if (
                not self.invulneravel
                or self.tempo_invulneravel % 2 == 0
            ):
                pyxel.blt(
                    self.x, self.y,
                    0, 67, 0,
                    26, 35, 6
                )

            # Desenha as moedas rosas da fase 4
            for moeda in self.moedas_fase4:
                if moeda["visivel"]:
                    pyxel.blt(
                        moeda["x"], moeda["y"],
                        0, 0, 24,
                        15, 16, 15
                    )    

        elif self.estado == "fase5":

            pyxel.cls(0)

             # Fundo
            pyxel.blt(0, 0, 2, 0, 0, 160, 220) 

            # Balão
            if not self.invulneravel or self.tempo_invulneravel % 2 == 0:
                pyxel.blt(self.x, self.y, 0, 67, 0, 26, 35, 6)
                        
            # Desenha as moedas verdes da Fase 5
            for moeda in self.moedas_fase5:
                if moeda["visivel"]:
                    pyxel.blt(moeda["x"], moeda["y"], 0, 7, 69, 15, 16, 15)
                        

        elif self.estado == "fase6":

            pyxel.cls(0)
            
            # Fundo
            pyxel.blt(0, 0, 2, 0, 0, 160, 220) 
            
            # Fundo
            pyxel.blt(95, 40, 2, 160, 0, 50, 50, 0) 
            
            # ovni (banco 0, posição 86,120 no editor)
            pyxel.blt(int(self.ovni_x), int(self.ovni_y), 0, 86, 120,
                    self.ovni_w, self.ovni_h, 0)
            
            # tiro vermelho
            if self.tiro is not None:
                pyxel.rect(int(self.tiro["x"]), int(self.tiro["y"]),
                        self.tiro_w, self.tiro_h, 8)
            
            # Balão
            if not self.invulneravel or self.tempo_invulneravel % 2 == 0:
                pyxel.blt(self.x, self.y, 0, 67, 0, 26, 35, 6)
            
            # Desenha as moedas verdes da Fase 6
            for moeda in self.moedas_fase6:
                if moeda["visivel"]:
                    pyxel.blt(moeda["x"], moeda["y"], 0, 7, 69, 15, 16, 15)
            

            
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

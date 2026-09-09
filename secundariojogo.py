for moeda in self.moedas:
            if moeda["visivel"]:
                
                if abs(self.x - moeda["x"]) < 16 and abs(self.y - moeda["y"]) < 16:
                    moeda["visivel"] = False

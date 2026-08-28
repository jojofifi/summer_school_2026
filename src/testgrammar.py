from enum import Enum, auto
import random

class Firework(Enum):
    Firework = auto()
# Partie du Firework
class Symbol(Enum):
    MONTEE = auto()
    EXPLOSION = auto()
# Different type de symbol
class Terminal(Enum):
    LINEAIRE = auto()
    COURBER = auto()
    ETOILE = auto()
    PARTICULE = auto()
    METEORITE = auto()
    
# Ce que renvoie le generator c'est a dire toute les infos du firework
class Tree:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []
    def print_tree(self):
        if not self.children :
            print(f" Terminal = {self.value}")
        else :
            result = "Tree" + str(self.value) + "\n"
            for i in range(len(self.children)):
                result += "\n"+ self.children[i].print_tree()
        return result



class Rules:
    def __init__(self):
        self.rules = {}
    # Ajoute dans rules une regle contenant un symbole et une liste avec contenue dedans et ajoute a la liste si meme symbole
    def add_rule(self, symbol, contenue):
        self.rules.setdefault(symbol, []).append(contenue)
    # Renvoie toute les regles d'un symbol
    def get_replacements(self, symbol):
        return self.rules[symbol]
    


class Generator:
    def __init__(self, rules):
        self.rules = rules

    def generate(self, symbol):
        # Prend la liste de tout les remplacement possible
        replacements = self.rules.get_replacements(symbol)
        # En choisit un random
        replacement = random.choice(replacements)
        # L'ajoute au Tree en fonction de ce que c'est
        return Tree(symbol, self._unwrap(replacement))

    def _unwrap(self, contenue):
        # Si c'est une liste prend tout les element et les unwrap
        if isinstance(contenue, list):
            result = []
            for c in contenue:
                result.extend(self._unwrap(c))
            return result
        # Si c'est un terminal ajoute au Tree
        elif isinstance(contenue, Terminal):
            return [Tree(contenue)]
        # Si c'est un symbol remplace par un terminal de la liste
        elif isinstance(contenue, Symbol):
            return [self.generate(contenue)]



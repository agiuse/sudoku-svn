# -*- coding: utf-8 -*-
'''
Created on 6 aout 2011

@author: eagius

L'objectif de la classe Compteur est de gérer les 9 mini-compteurs, 1 par chiffre.
Cette classe permet de mettre à jour ces compteurs et gérer la liste de référence de cases.
La classe permet d'incrémenter ou de décrémenter le compteur en fonction de l'ajout ou la suppression
d'un chiffre dans une case.
'''
from sudoku_case import Case

class Counter(object):
    """
    """

    def __init__(self):
        self.counter = [None,[],[],[],[],[],[],[],[],[]]
    
    def _len(self,digit):
        """
        Renvoie le nombre de cases associés au compteur
        """
        return(len(self.counter[digit]))

    # ----- incrémente / décremente le compteur
    # principe : ajouter/supprimer une case
    def inc(self,ref_case):
        """
        Cette méthode incrémente tous les compteurs dont le chiffre appartient à la liste de la case
        La méthode renvoie True si l'opération s'est bien déroulé sinon False
        """
        if isinstance(ref_case,Case):
            for _digit in ref_case.list():
                try:
                    self.counter[_digit].index(ref_case)
                except ValueError:                    
                    self.counter[_digit].append(ref_case)
            return(True)  
        return(False)
    
    def list(self):
        """
        Renvoie le compteur sous forme de liste
        """
        return([self._len(_i_counter) for _i_counter in range(1,10)])
                
    def __eq__(self,ref_counter):
        if isinstance(ref_counter,Counter):
            # comparaison entre objet deux compteurs     
            return(self.list() == ref_counter.list())
        
        if isinstance(ref_counter,list):
            # comparaison entre un objet et une liste
            return(self.list() == ref_counter)
        
        return(None)
    
    def __ne__(self,ref_counter):
        return(not self.__eq__(ref_counter))

    
    def __str__(self):
        _string="counter("
        for _i_counter in range(1,9):
            _string = _string + str(self._len(_i_counter)) + ","
        return(_string + str(self._len(9)) + ")")
 

if __name__ == '__main__':
    # ---- test de la création
    print("Test 1 - création d'un compteur")
    compteur = Counter()
    print("compteur =", compteur)    
    print("  -----------------------------------------")    
        
    # ---- test de l'ajout de Case avec toutes les chiffres
    print("Test 2 - ajout d'une case avec la liste de valeur par défaut")
    compteur = Counter()
    case1 = Case(3,4)
    case2 = Case(2,5)
    compteur.inc(case1)
    compteur.inc(case2)
    resultat_compteur=[2,2,2,2,2,2,2,2,2]
    print("compteur =", compteur)
    if compteur != resultat_compteur:
        print("Test 2.1 compteur Ko", compteur, "vs", resultat_compteur)
    print("  -----------------------------------------")    
        
    # ---- Test de l'ajout de Case avec des listes de valeurs reduite
    print("Test 3 - ajout d'une case avec des listes de valeurs différentes")
    compteur = Counter()
    case1 = Case(3,4)
    case1.sub(2)
    case1.sub(9)
    case2 = Case(2,5)
    case2.update(4)
    case3 = Case(4,5)
    resultat_compteur = [2,1,2,3,2,2,2,2,1]
    compteur.inc(case1)
    compteur.inc(case2)
    compteur.inc(case3)
    print("compteur =", compteur)
    if compteur != resultat_compteur:
        print("Test 3.1 compteur Ko", compteur, "vs", resultat_compteur)
    print("  -----------------------------------------")

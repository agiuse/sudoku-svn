# -*- coding: utf-8 -*-
'''
Created on 29 juil. 2011

@author: eagius
'''

# ----------------------------------------------------------------------------------------------
from sudoku_coordinate import Coordinate

class Case(object):
    """
    La Classe Case contient comme donnée une liste de chiffres et des métadonnées :
    - statut : permet de dire si sa liste est constituée d'un chiffre, d'un couple de chiffre ou de n chiffres
    - resolved_statut : booléen pour exprimer si le chiffre est trouvé ou en cours de résolution
    - new_pair : boolean pour exprimer si la case contient un couple qui n'a pas été traité
    """
    __SINGLE_DIGIT__ = 0
    __MULTI_DIGIT__ = 1
    __PAIR_DIGIT__ = 2
    __EMPTY_DIGIT__= 3
    
    __COLUMN__ = 0
    __ROW__ = 1
    __SQUARE__ = 2

    
    
    def __init__(self, coordinate_column, coordinate_row):
        self._array_statut = [ Case.__EMPTY_DIGIT__, Case.__SINGLE_DIGIT__, 
                              Case.__PAIR_DIGIT__, Case.__MULTI_DIGIT__, 
                              Case.__MULTI_DIGIT__, Case.__MULTI_DIGIT__,
                              Case.__MULTI_DIGIT__, Case.__MULTI_DIGIT__,
                              Case.__MULTI_DIGIT__, Case.__MULTI_DIGIT__]
        
        self._values = [1,2,3,4,5,6,7,8,9]
        self._resolved_statut = False
        self._new_pair = False
        self._coordinate = Coordinate(coordinate_column,coordinate_row)
        self.__method_near_cases__ = (self._coordinate.getListColumn,self._coordinate.getListRow,self._coordinate.getListSquare)

    # --- méthode de consultation
    def getCoordinate(self):
        return (self._coordinate)

    def getNearCases(self,type):   
        """
        Retourne une liste d'objet Coordinate sans la coordonnée de la case courante
        """
        return([ coord for coord in self.__method_near_cases__[type]() if coord != self.getCoordinate()]) 

    # --- comparaison entre la case
    def __eq__(self, case): 
        """
        Compare la case courante avec la case en paramètre.
        L'objectif de la comparaison est de dire si la case comparée est la même ou non.
        Le critère d'acceptance est la correspondance entre la coordonnée quelle que soit la liste des chiffres.  
        """
        # --- Comparaison entre deux coordonnées
        if isinstance(case,Case):
            # Compare entre deux objets Case
            # Appel de la méthode Coordinate.__eq__
            return(self.getCoordinate() == case.getCoordinate())
       
        if isinstance(case,Coordinate) or isinstance(case,tuple):
            # Compare entre un objet Coordinate de Case et un objet Coordinate ou un tuple
            # Appel de la méthode Coordinate.__eq__
            return(self.getCoordinate() == case)
        
        # --- Comparaison entre deux listes de valeurs
        if isinstance(case,list):
            # Compare la liste des valeurs de la Case et celle en paramètre
            
            return(self.list() == case)
        
        return(None)

    def __ne__(self, case): 
        """
        Compare la case courante avec la case en paramètre.
        L'objectif de la comparaison est de dire si la case comparée est la même ou non.
        Le critère d'acceptance est la correspondance entre la coordonnée quelle que soit la liste des chiffres.  
        """
        return(not self.__eq__(case))
         
    # --- Gestion des changements d'état --- 
    def is_single_digit(self):
        """
        méthode qui renvoie vrai si le statut de la case est single digit et case non resolue
        """
        return(self.getStatut() == Case.__SINGLE_DIGIT__ and self.is_not_resolved())
    
    def is_not_resolved(self):
        """
        Renvoie True si la case est en état "not resolved"
        """
        return (not self._resolved_statut)

    def getStatut(self):
        """
        Renvoie True si la case possède une seule valeur
        """
        return( self._array_statut[self.len()] )

    def is_new_pair(self):
        """
        Renvoie True si la case à deux digits et elle n'est pas encore traitée
        """
        return(self._new_pair)

    def setPairTraited(self):
        """
        Passe la case � l'état "doublon trait�e"
        """
        if self.getStatut() == Case.__PAIR_DIGIT__:
            if self.is_new_pair():
                self._new_pair = False
                
    def setResolved(self):
        """
        Passe la case � l'état "resolved"
        """
        if self.is_not_resolved() and self.getStatut() == Case.__SINGLE_DIGIT__:
            self._resolved_statut = True
            
    # --- GESTION DE LA LISTE DE CHIFFRE ---
    def add(self, digit):
        """
        ajout un digit dans la liste
        """
        if self.is_not_resolved():
            try:
                self._values.index(digit)
                return(False)
            except ValueError:
                self._values.append(digit)
                if self.getStatut() == Case.__PAIR_DIGIT__:
                    self._new_pair = True                        
                
                return(True)
        
        return(False)
    

    def sub(self, digit):
        """
        Supprime un digit de la liste
        """       
        if self.is_not_resolved():
            try:
                self._values.remove(digit)
                if self.getStatut() == Case.__PAIR_DIGIT__:
                    self._new_pair = True                        
                return(True)
            except ValueError:
                return(False)

        return(False)
    
    def update(self, digit):
        """
        Met la liste au chiffre en param�tre
        """
        if self.is_not_resolved():
            self._values = []
            self._new_pair = False
            self.add(digit)
            return(True)
        
        return(False)

    def isDigit(self, digit):
        """
        Retourne True si le chiffre appartient à la liste de valeur
        """
        try:
            self._values.index(digit)
            return(True)
        except ValueError:
            return(False)

    def list(self):
        """
        Renvoie la liste de valeur
        """
        self._values.sort()
        return(self._values)
 
    def len(self):
        """
        Renvoie la longueur de la liste de chiffre
        """
        return(len(self.list()))


    def __str__(self):
        """
        Affichage dans la commande print
        """
#        __len = self.len()
#        if __len == 1:
#            return("v = ({[0]})".format(self._values))
#        elif __len == 2:
#            return("v = ({},{})".format(self._values))        
#        elif __len > 2:
        if self.is_not_resolved():
            return("v = ({})".format(self._values))
        else:
            return("v = <{}>".format(self._values))
            

if __name__ == '__main__':

    # --- TEST GESTION DE LA LISTE ---
    c = Case(2,3)
    
    print("Test 0 - méthode __str__",c)
    
    # --- affiche la liste par défaut
    print("Test 1 - méthode list() et __eq__()")
    r = [1,2,3,4,5,6,7,8,9]
    if c != r:
        print(r,c,'KO')

    # --- supprime un chiffre existant
    print("Test 2.1 - méthode sub() avec un élément existant en début de liste",c)
    r = [2,3,4,5,6,7,8,9]
    c.sub(1)
    if c != r:
        print(r,c,'KO')
        
    print("Test 2.2 - méthode sub() avec un élément existant en fin de liste",c)
    r = [2,3,4,5,6,7,8]
    c.sub(9)
    if c != r:
        print(r,c,'KO')

    print("Test 2.3 - méthode sub() avec un élément existant en milieu de liste",c)
    r = [2,3,4,6,7,8]
    c.sub(5)
    if c != r:
        print(r,c,'KO')
  
    # --- supprime un chiffre non existant
    print("Test 3.1 - méthode sub() avec un élément inexistant en début de liste",c)
    r = [2,3,4,6,7,8]
    c.sub(1)
    l = c.list()
    if l != r:
        print(r,l,'KO')

    print("Test 3.2 - méthode sub() avec un élément inexistant en fin de liste",c)
    r = [2,3,4,6,7,8]
    c.sub(9)
    if c != r:
        print(r,c,'KO')

    print("Test 3.3 - méthode sub() avec un élément inexistant en milieu de liste", c)
    r = [2,3,4,6,7,8]
    c.sub(5)
    if c != r:
        print(r,c,'KO')
    
    # --- ajoute un chiffre existant
    print("Test 4.1 - méthode add() avec un élément existant en début de liste", c)
    r = [2,3,4,6,7,8]
    c.add(2)
    if c != r:
        print(r,c,'KO')

    print("Test 4.2 - méthode add() avec un élément existant en milieu de liste",c)
    r = [2,3,4,6,7,8]
    c.add(6)
    if c != r:
        print(r,c,'KO')

    print("Test 4.3 - méthode add() avec un élément existant en fin de liste",c)
    r = [2,3,4,6,7,8]
    c.add(8)
    if c != r:
        print(r,c,'KO')

    # --- ajoute un chiffre inexistant
    print("Test 5.1 - méthode add() avec un élément inexistant en début de liste",c)
    r = [1,2,3,4,6,7,8]
    c.add(1)
    if c != r:
        print(r,c,'KO')

    print("Test 5.2 - méthode add() avec un élément inexistant en milieu de liste",c)
    r = [1,2,3,4,5,6,7,8]
    c.add(5)
    if c != r:
        print(r,c,'KO')

    print("Test 5.3 - méthode add() avec un élément inexistant en fin de liste",c)
    r = [1,2,3,4,5,6,7,8,9]
    c.add(9)
    if c != r:
        print(r,c,'KO')

    # --- test la methode update()
    print("Test 6 - test la méthode update()",c)
    c = Case(6,2)
    r = [4]
    c.update(4)
    if c != r:
        print(r,c,'KO')
    
    # --- TEST GESTION DU STATUS ---
    c = Case(6,2)
    
    # --- test le statut par défaut
    print("Test 7 - test la méthode getStatut(), is_not_resolved() et is_new_pair()")
    r_statut = (True,                   # --- not resolved
                False,                  # --- not resolved et __SINGLE_DIGIT
                Case.__MULTI_DIGIT__,   # --- le nombre de chiffre
                False                   # --- si c'est une paire non traité
                )
    statut = (c.is_not_resolved(),c.is_single_digit(), c.getStatut(), c.is_new_pair())
    if r_statut != statut:
        print(r_statut, statut,"KO")
    
    print("Test 8 - test le changement de statut de multi à pair traitée impossible")
    r_statut = (True,                   # --- not resolved
                False,                  # --- not resolved et __SINGLE_DIGIT
                Case.__MULTI_DIGIT__,   # --- le nombre de chiffre
                False                  # --- si c'est une paire non traité
                )
    c.setPairTraited()
    statut = (c.is_not_resolved(),c.is_single_digit(), c.getStatut(), c.is_new_pair())
    if r_statut != statut:
        print(r_statut, statut,"KO")
        
    print("Test 9 - test le changement de statut à l'état résolu impossible")
    r_statut = (True,                   # --- not resolved
                False,                  # --- not resolved et __SINGLE_DIGIT
                Case.__MULTI_DIGIT__,   # --- le nombre de chiffre
                False                  # --- si c'est une paire non traité
                )
    c.setResolved()
    statut = (c.is_not_resolved(),c.is_single_digit(), c.getStatut(), c.is_new_pair())
    if r_statut != statut:
        print(r_statut, statut,"KO")

    print("Test 10 - test le changement de statut de multi à pair")
    r_statut = (True,                   # --- not resolved
                False,                  # --- not resolved et __SINGLE_DIGIT
                Case.__PAIR_DIGIT__,   # --- le nombre de chiffre
                True                  # --- si c'est une paire non traité
                )
    c.sub(1)
    c.sub(2)
    c.sub(3)
    c.sub(5)
    c.sub(6)
    c.sub(7)
    c.sub(9)
    
    statut = (c.is_not_resolved(),c.is_single_digit(), c.getStatut(), c.is_new_pair())
    if r_statut != statut:
        print(r_statut, statut,"KO")

    print("Test 11 - test le changement de statut de pair non traitée à traitée")
    r_statut = (True,                   # --- not resolved
                False,                  # --- not resolved et __SINGLE_DIGIT
                Case.__PAIR_DIGIT__,   # --- le nombre de chiffre
                False                  # --- si c'est une paire non traité
                )
    c.setPairTraited()
    statut = (c.is_not_resolved(),c.is_single_digit(), c.getStatut(), c.is_new_pair())
    if r_statut != statut:
        print(r_statut, statut,"KO")

    print("Test 12 - test le changement de statut à l'état résolu impossible")
    r_statut = (True,                   # --- not resolved
                False,                  # --- not resolved et __SINGLE_DIGIT
                Case.__PAIR_DIGIT__,   # --- le nombre de chiffre
                False                  # --- si c'est une paire non traité
                )
    c.setResolved()
    statut = (c.is_not_resolved(),c.is_single_digit(), c.getStatut(), c.is_new_pair())
    if r_statut != statut:
        print(r_statut, statut,"KO")
 
    print("Test 13 - test le changement de statut de pair à mono")
    r_statut = (True,                   # --- not resolved
                True,                  # --- not resolved et __SINGLE_DIGIT
                Case.__SINGLE_DIGIT__,   # --- le nombre de chiffre
                False                  # --- si c'est une paire non traité
                )
    c.sub(8)
    statut = (c.is_not_resolved(),c.is_single_digit(), c.getStatut(), c.is_new_pair())
    if r_statut != statut:
        print(r_statut, statut,"KO")
        
    print("Test 14 - test que le changement en mode resolved est possible")
    r_statut = (False,                   # --- not resolved
                False,                  # --- not resolved et __SINGLE_DIGIT
                Case.__SINGLE_DIGIT__,   # --- le nombre de chiffre
                False                  # --- si c'est une paire non traité
                )
    c.setResolved()
    statut = (c.is_not_resolved(),c.is_single_digit(), c.getStatut(), c.is_new_pair())
    if r_statut != statut:
        print(r_statut, statut,"KO")

    # --- Test les méthodes de calculs des cases voisines
    # test la methode getNearCases(type)
    cases = (Case(2,3),Case(6,2),Case(7,1),Case(1,4),Case(5,5),Case(9,6),Case(3,8),Case(4,9),Case(8,7))

    print("Test 15 - test la methode getNearCases(Case.__COLUMN__)")
    coords_result=(
            ((1,3,1),(3,3,1),(4,3,2),(5,3,2),(6,3,2),(7,3,3),(8,3,3),(9,3,3)),
            ((1,2,1),(2,2,1),(3,2,1),(4,2,2),(5,2,2),(7,2,3),(8,2,3),(9,2,3)),
            ((1,1,1),(2,1,1),(3,1,1),(4,1,2),(5,1,2),(6,1,2),(8,1,3),(9,1,3)),
            ((2,4,4),(3,4,4),(4,4,5),(5,4,5),(6,4,5),(7,4,6),(8,4,6),(9,4,6)),
            ((1,5,4),(2,5,4),(3,5,4),(4,5,5),(6,5,5),(7,5,6),(8,5,6),(9,5,6)),
            ((1,6,4),(2,6,4),(3,6,4),(4,6,5),(5,6,5),(6,6,5),(7,6,6),(8,6,6)),
            ((1,8,7),(2,8,7),(4,8,8),(5,8,8),(6,8,8),(7,8,9),(8,8,9),(9,8,9)),
            ((1,9,7),(2,9,7),(3,9,7),(5,9,8),(6,9,8),(7,9,9),(8,9,9),(9,9,9)),
            ((1,7,7),(2,7,7),(3,7,7),(4,7,8),(5,7,8),(6,7,8),(7,7,9),(9,7,9))
            )
    
    for _i_test in range(0,9):
        c = cases[_i_test]
        print("Case - Test 15.",_i_test + 1, " -" ,c.getCoordinate()," :")
        result = coords_result[_i_test]
        cases_voisines = c.getNearCases(Case.__COLUMN__)
        for (ref_coord, _i_coord) in zip(cases_voisines, range(0,len(cases_voisines))):
            print(ref_coord, result[_i_coord], ref_coord == result[_i_coord])

    print("Test 16 - test la methode getNearCases(Case.__ROW__)")
    coords_result=(
            ((2,1,1),(2,2,1),(2,4,4),(2,5,4),(2,6,4),(2,7,7),(2,8,7),(2,9,7)),
            ((6,1,2),(6,3,2),(6,4,5),(6,5,5),(6,6,5),(6,7,8),(6,8,8),(6,9,8)),
            ((7,2,3),(7,3,3),(7,4,6),(7,5,6),(7,6,6),(7,7,9),(7,8,9),(7,9,9)),
            ((1,1,1),(1,2,1),(1,3,1),(1,5,4),(1,6,4),(1,7,7),(1,8,7),(1,9,7)),
            ((5,1,2),(5,2,2),(5,3,2),(5,4,5),(5,6,5),(5,7,8),(5,8,8),(5,9,8)),
            ((9,1,3),(9,2,3),(9,3,3),(9,4,6),(9,5,6),(9,7,9),(9,8,9),(9,9,9)),
            ((3,1,1),(3,2,1),(3,3,1),(3,4,4),(3,5,4),(3,6,4),(3,7,7),(3,9,7)),
            ((4,1,2),(4,2,2),(4,3,2),(4,4,5),(4,5,5),(4,6,5),(4,7,8),(4,8,8)),
            ((8,1,3),(8,2,3),(8,3,3),(8,4,6),(8,5,6),(8,6,6),(8,8,9),(8,9,9))
            )

    for _i_test in range(0,9):
        c = cases[_i_test]
        print("Case - Test 16.",_i_test + 1, " -" ,c.getCoordinate()," :")
        result = coords_result[_i_test]
        cases_voisines = c.getNearCases(Case.__ROW__)
        for (ref_coord,_i_coord) in zip(cases_voisines, range(0,8)):
            print(ref_coord, result[_i_coord], ref_coord == result[_i_coord])
 
    print("Test 17 - test la methode getNearCases(Case.__SQUARE__)")
    coords_result=(
            ((1,1,1),(1,2,1),(1,3,1),(2,1,1),(2,2,1),(3,1,1),(3,2,1),(3,3,1)),
            ((4,1,2),(4,2,2),(4,3,2),(5,1,2),(5,2,2),(5,3,2),(6,1,2),(6,3,2)),
            ((7,2,3),(7,3,3),(8,1,3),(8,2,3),(8,3,3),(9,1,3),(9,2,3),(9,3,3)),
            ((1,5,4),(1,6,4),(2,4,4),(2,5,4),(2,6,4),(3,4,4),(3,5,4),(3,6,4)),
            ((4,4,5),(4,5,5),(4,6,5),(5,4,5),(5,6,5),(6,4,5),(6,5,5),(6,6,5)),
            ((7,4,6),(7,5,6),(7,6,6),(8,4,6),(8,5,6),(8,6,6),(9,4,6),(9,5,6)),
            ((1,7,7),(1,8,7),(1,9,7),(2,7,7),(2,8,7),(2,9,7),(3,7,7),(3,9,7)),
            ((4,7,8),(4,8,8),(5,7,8),(5,8,8),(5,9,8),(6,7,8),(6,8,8),(6,9,8)),
            ((7,7,9),(7,8,9),(7,9,9),(8,8,9),(8,9,9),(9,7,9),(9,8,9),(9,9,9))
            )
    for _i_test in range(0,9):
        c = cases[_i_test]
        print("Case - Test 17.",_i_test + 1, " -" ,c.getCoordinate()," :")
        result = coords_result[_i_test]
        cases_voisines = c.getNearCases(Case.__SQUARE__)
        for (_i_coord, ref_coord) in zip(range(0,8),cases_voisines):
            print(ref_coord, result[_i_coord], ref_coord == result[_i_coord])

    # --- Test la méthode isDigit(self,digit)
    print("Test 18 - test la méthode isDigit(self,digit) avec présence du chiffre")
    # -- test l'existence
    result=(True,True,True,True,True,True,True,True,True)
    case = Case(3,5)
    for digit in range(0,9):
        if case.isDigit(digit+1) != result[digit]:
            print("Test 18 - Ko pour le chiffre", digit + 1, "(",result[digit],")")
    
    # -- test l'absence
    print("Test 19 - test la méthode isDigit(self,digit) avec non présence du chiffre")
    result=(False,False,True,False,False,False,False,False,False)
    case.update(3)
    for digit in range(0,9):
        if case.isDigit(digit+1) != result[digit]:
            print("Test 19 - Ko pour le chiffre", digit + 1, "(",result[digit],")")
        
    # -- Test l'affichage
    case = Case(3,6)
    print("Test 20.1 - test en multi-valeur",case)
    case.update(4)
    print("Test 20.2 - test en single valeur", case)
    case.add(2)
    print("Test 20.3 - test en pair value", case)
    case.sub(4)
    case.setResolved()
    print("Test 20.4 - test en single value et à l'état resolved",case)

# -*- coding: utf-8 -*-
'''
Created on 25 juil. 2011

@author: eagius
'''
# ----------------------------------------------------------------------------------------------
from sudoku_coordinate import Coordinate
from sudoku_case import Case

class Grid(object):
    """
    La classe Grid va gérer une grille 9x9
    """
    __INIT_STEP__ = 0
    __READY_STEP__ = 1
       
    def __init__(self):
        self._row_max=9
        self._column_max=9
        self.__array_cases = []
        self._step = Grid.__INIT_STEP__
        self.create()
        
    def create(self):
        # --- créer la grille 9x9 avec 81 cases
        def _column_created(_i_row):
            return( [Case(_i_column, _i_row) 
                     for _i_column in range(1,self._column_max + 1)]
                   )
        
        self.__array_cases = [ _column_created(_i_row) for _i_row in range(1,self._row_max+1)]
        
    # --- gestion du statut de la grille
    def getStatut(self):
        """
        Donne le statut courant de la grille
        """
        return(self._step)
    
    def setStatut(self,new_statut):
        """
        Change de statut 
        """
        self._step = new_statut
    
    def isStatut(self, statut):
        return(self._step == statut)

    # --- Gestion des cases
    def getCase(self,column, row=0):
        """
        Méthode qui renvoie la référence de la case à partir de ses coordonnées.
        """
        if isinstance(column,Coordinate):
            _coord = column
        else:
            _coord = Coordinate(column, row)
            
        return (self.__array_cases[_coord.row() - 1][_coord.column() - 1])
    
    def setValues(self,cases_list):
        """
        Initie la grille avec des cases de départs.
        En entrée, une liste de tuple (c,r,digit)
        """
        if self.isStatut(Grid.__INIT_STEP__):
            if isinstance(cases_list,tuple):
                _nb_cases = 0
                for (_column, _row, _digit) in cases_list:
                    _c = self.getCase(_column,_row)
                    self.update(_c,_digit)
                    _nb_cases = _nb_cases + 1

                self.setStatut(Grid.__READY_STEP__)
                return(_nb_cases)
            
        return(None)
            
    def getValues(self,column,row):
        """
        Méthode donnant la liste des valeurs d'une case
        """
        # Coordonnées vérifiées par la méthode getCase
        return(self.getCase(column, row).list())      
         
    def sub(self,ref_case,digit):
        """
        Cette méthode permet de retirer un chiffre et  de mettre en place les compteurs
        """
        return(ref_case.sub(digit))
        
    def update(self,ref_case,digit):
        """
        Cette méthode permet de mettre un chiffre et de mettre en place les compteurs
        """
        ref_case.update(digit)

    # --- gestion de la liste ou d'un sous-liste de cases
    def getCases(self, ref_case, type = Case.__COLUMN__ ):    
        """
        Renvoie les cases voisines de la case courante en fonction de type Column, Row ou Square
        Remarque : La case courante n'est pas mise dans la liste.        
        """
        if isinstance(ref_case,Case):
            return([ self.getCase(coordonne) for coordonne in ref_case.getNearCases(type) ])
        
        return(None)

    def checkCase(self,ref_case):
        """
        Cette méthode vérifie que la case possède bien une valeur unique et qu'une case voisine ne 
        contient pas cette valeur unique.
        Elle génère l'exception ValueError si le nombre de cases est supérieur.
        """
        if isinstance(ref_case,Case):
            if ref_case.getStatut() == Case.__SINGLE_DIGIT__:
                # -- calcule toutes les cases voisines en __SINGLE_DIGIT__
                nb = len([ case for case in self.getCases(ref_case, Case.__COLUMN__) + 
                         self.getCases(ref_case, Case.__ROW__) + 
                         self.getCases(ref_case, Case.__SQUARE__)
                         if case == ref_case ])
                if nb > 1:
                    raise(ValueError)

   
    def list(self):
        """
        Méthode qui renvoie l'ensemble des références des cases sous forme d'une liste
        Objectif : traiter en boucle les cases.
        METHODE NON TESTEE
        """
        
        return( [ self.getCase(_nb_case) for _nb_case in range(1,82)])

    def array(self):
        """
        Méthode qui renvoie la grille sous forme de tableau contenant la liste des valeurs
        """
        def _row_traited(_i_row):
            return([self.getValues(_i_column + 1, _i_row + 1)
                    for _i_column in range(0,self._column_max)]
                   )
        return([_row_traited(_i_row) for _i_row in range(0,self._row_max)])
        
    # --- comparaison entre deux grille
    def __eq__(self, grille): 
        """
        Compare la grille courante avec la grille en paramètre.
        La grille peut être un objet Grid ou bien un tableau de tableau (objet list)
        L'objectif de la comparaison est de dire si la case comparée est la même ou non.
        Le critère d'acceptance est la correspondance entre la coordonnée quelle que soit la liste des chiffres.  
        """

        if isinstance(grille,Grid):
            # Compare entre deux objets Case
            return(self.array() == grille.array())
        
        if isinstance(grille,list):
            # compare entre un objet Grid et la grille sous forme de liste
            return(self.array() == grille)
            
        return(None)

    def __str__(self):
        """
        Affiche la grille avec la commande print
        """
        def _row_traited(_i_row):
            _string=""
            for _i_column in range(1,self._column_max+1):
                _string = _string + "{:33}".format(self.getCase(_i_column,_i_row))
                if _i_column == 3 or _i_column == 6:
                    _string = _string + "|"
                else:
                    _string = _string + ":"
            return(_string)
                    
        _string=""
        for _i_row in range(1,self._row_max+1):
            if _i_row == 4 or _i_row == 7:
                _string = _string + "--------------------------------------------------------------------------------------------------------------------\n"
            _string = _string + "row = " + str(_i_row) +"|" + _row_traited(_i_row) + "\n"
        return(_string)

    # ---- METHODES DE RESOLUTION
    def _lookup_methodA(self):
        """
        fonction qui permet de générer la liste des cases avec un seul chiffre 
        et dont la case n'est pas "résolue" en parcourant toute la grille
        """
        _nb_case_resolved=0
        for ref_case in self.list():
            if ref_case.is_single_digit():
                _digit = ref_case.list()[0]
                _list = [ _case for _case in self.getCases(ref_case,Case.__COLUMN__) + self.getCases(ref_case,Case.__ROW__) + self.getCases(ref_case,Case.__SQUARE__)
                         if _case.is_not_resolved() and not _case.is_single_digit() ]
                for _case in _list:
                    if _case.is_not_resolved() and _case.isDigit(_digit):
                        self.sub(_case,_digit)
                        _nb_case_resolved = _nb_case_resolved + 1

                ref_case.setResolved()

        return(_nb_case_resolved)

    def _lookup_methodB(self):
        """
        Cette méthode privée permet de résoudre les cases ayant un chiffre unique;
        """
        def traitment(ref_case, type):
            # vérifique que les cases voisines n'ont pas le chiffre
            for _digit in ref_case.list():
                compteur = 0
                for _case in self.getCases(ref_case,type):
                    if _case.isDigit(_digit):
                        compteur = compteur + 1
                if compteur == 0:
                    self.update(ref_case, _digit)
                    return(1)       # -- il ne peut avoir deux chiffres uniques dans la même case
            return(0)               
                     
        _nb_case_resolved=0
        # --- lister les 9 cases par zone
        for ref_case in self.list():
            if ref_case.is_not_resolved():
                if not ref_case.is_single_digit():
                    for _type in (Case.__COLUMN__,Case.__ROW__,Case.__SQUARE__):
                        _nb_case_resolved = _nb_case_resolved + traitment(ref_case,_type)

        return(_nb_case_resolved)

    def _lookup_methodC(self):
        """
        Cette méthode privée permet de résoudre les cases étant un coupe de cases pair;
        """
        def traitment(ref_case,type):
            _nb_case_resolved = 0
            # --- recherche une case avec le même couple de chiffres dans la zone de la case
            _cases_list=self.getCases(ref_case,type)
            _pair_case=None
            _digits_list=ref_case.list()
            for _case in _cases_list: # -- pas de test sur la cohérence (normalement 1 seule case)
                if _digits_list == _case.list(): _pair_case=_case
                    # --- elimine les valeurs
            
            if isinstance(_pair_case,Case):
                for _case in _cases_list:
                    if _case != _pair_case:
                        if _case.is_not_resolved() and (self.sub(_case, _digits_list[0]) | self.sub(_case, _digits_list[1])):
                            _nb_case_resolved = _nb_case_resolved + 1
                            
            return(_nb_case_resolved)
        
        _nb_case_resolved=0
        
        for ref_case in self.list():
            if ref_case.is_not_resolved():
                if ref_case.is_new_pair():
                    for _type in (Case.__COLUMN__,Case.__ROW__,Case.__SQUARE__):
                        _nb_case_resolved = _nb_case_resolved + traitment(ref_case,_type)
                        ref_case.setPairTraited()   
                
        return(_nb_case_resolved)
    
    def lookup(self):            
        """
        Cette méthode contient l'algorithme de résolution d'une grille
        """
        if self.isStatut(Grid.__READY_STEP__):
            _progress = True
            while _progress:
                while self._lookup_methodA() != 0:
                    pass
            
                if self._lookup_methodB() == 0:
                    if self._lookup_methodC() == 0:
                        _progress = False
            
            return(True)
        
        return(None)
    
# -----------------------------------------------------------------------------------
if __name__ == '__main__':

 
    # ---- Test les méthodes de comparaison et array()
    print("Test 1.1 - test la methode create() et __init__")
    grille = Grid()
    grille_resultat_init = [
        [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
    ]
    print("Test 1.2 - la grille initiale (méthode __eq__() et array()", grille == grille_resultat_init)

    print("Test 1.3 - test la méthode __str__()")
    print(grille)
    
    # ---- Test l'ajout de valeur à l'étape __INIT_STEP__
    print("Test 2 - étape __INIT_STEP__")
    grille = Grid()
    grille_resultat_easy = [
        [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[8],[1,2,3,4,5,6,7,8,9],[1],[1,2,3,4,5,6,7,8,9]],
        [[3],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[5],[1,2,3,4,5,6,7,8,9],[9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[7]],
        [[1,2,3,4,5,6,7,8,9],[4],[1,2,3,4,5,6,7,8,9],[6],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[9],[8],[5]],
        [[5],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[3],[1,2,3,4,5,6,7,8,9],[6],[1,2,3,4,5,6,7,8,9],[2],[4]],
        [[4],[1],[1,2,3,4,5,6,7,8,9],[8],[2],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [[1,2,3,4,5,6,7,8,9],[3],[1,2,3,4,5,6,7,8,9],[4],[5],[1],[1,2,3,4,5,6,7,8,9],[7],[6]],
        [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[5],[1],[7],[1,2,3,4,5,6,7,8,9],[3],[6],[8]],
        [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[8],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[5],[1,2,3,4,5,6,7,8,9]],
        [[1,2,3,4,5,6,7,8,9],[7],[3],[2],[1,2,3,4,5,6,7,8,9],[5],[4],[1,2,3,4,5,6,7,8,9],[1]]
    ]
    if not grille.isStatut(Grid.__INIT_STEP__):
        print("Test 2.1 : la grille n'est pas à l'état __READY_STEP__")
    
    list_cases = ((1,2,3),(1,4,5),(1,5,4),(2,3,4),(2,5,1),(2,6,3),(2,9,7),
                 (3,7,5),(3,9,3),(4,2,5),(4,3,6),(4,4,3),(4,5,8),
                (4,6,4),(4,7,1),(4,9,2),(5,5,2),(5,6,5),(5,7,7),
                (5,8,8),(6,1,8),(6,2,9),(6,4,6),(6,6,1),(6,9,5),
                (7,3,9),(7,7,3),(7,9,4),(8,1,1),(8,3,8),(8,4,2),
                (8,6,7),(8,7,6),(8,8,5),(9,2,7),(9,3,5),(9,4,4),
                (9,6,6),(9,7,8),(9,9,1))
    
    r = grille.setValues(list_cases)
    
    if r == None :
        print("Test 2.2 : Verifie que la methode setValues() a mis à jour la grille - Ko")
    
    if r != 40:
        print("Test 2.3 : le nombre de cases mises à jour n'est pas celui prévu : 40 <>", r)
        
    if not grille.isStatut(Grid.__READY_STEP__):
        print("Test 2.4 : la grille n'est pas à l'état __READY_STEP__")
    
    print("Test 2.5 - verifie le contenu de la grille (test la méthode __eq__() et array()", grille == grille_resultat_easy)
    
    if ( grille.setValues(((1,3,3))) != None):
        print("Test 2.5.1 - verifie que la grille n'est plus modifiable par cette méthode setValues()- Ko")
    
    print("Test 2.6 - test la méthode __str__()")
    print(grille)

    # --- Vérification de la cohérence de la grille en __INIT_STEP__
    print("Test 3 - vérifie la cohérence d'une grille en erreur")
    grille = Grid()
    grille_resultat_easy = [
        [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[8],[1,2,3,4,5,6,7,8,9],[1],[1,2,3,4,5,6,7,8,9]],
        [[3],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[5],[1,2,3,4,5,6,7,8,9],[9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[7]],
        [[1,2,3,4,5,6,7,8,9],[4],[1,2,3,4,5,6,7,8,9],[6],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[9],[8],[5]],
        [[5],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[3],[1,2,3,4,5,6,7,8,9],[6],[1,2,3,4,5,6,7,8,9],[2],[4]],
        [[4],[1],[1,2,3,4,5,6,7,8,9],[8],[2],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [[1,2,3,4,5,6,7,8,9],[3],[1,2,3,4,5,6,7,8,9],[4],[5],[1],[1,2,3,4,5,6,7,8,9],[7],[6]],
        [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[5],[1],[7],[1,2,3,4,5,6,7,8,9],[3],[6],[8]],
        [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[8],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[5],[1,2,3,4,5,6,7,8,9]],
        [[1,2,3,4,5,6,7,8,9],[7],[3],[2],[1,2,3,4,5,6,7,8,9],[5],[4],[1,2,3,4,5,6,7,8,9],[1]]
    ]
    if not grille.isStatut(Grid.__INIT_STEP__):
        print("Test 3.1 : la grille n'est pas à l'état __READY_STEP__")
    
    list_cases = ((1,2,3),(1,4,5),(1,5,5),(2,3,4),(2,5,1),(2,6,1),(2,9,7),
                 (3,7,5),(3,9,3),(4,2,5),(4,3,6),(4,4,3),(4,5,8),
                (4,6,4),(4,7,1),(4,9,2),(5,5,2),(5,6,5),(5,7,7),
                (5,8,8),(6,1,8),(6,2,9),(6,4,6),(6,6,1),(6,9,5),
                (7,3,9),(7,7,3),(7,9,4),(8,1,1),(8,3,8),(8,4,2),
                (8,6,7),(8,7,6),(8,8,5),(9,2,7),(9,3,5),(9,4,4),
                (9,6,6),(9,7,8),(9,9,1))

    try:
        r = grille.setValues(list_cases)
    except ValueError:
        print("Test 3.2 - test de cohérence ok")
        
    # ---- test la méthode getCase(x,y)
    print("Test 4 - test la méthode getCase(x,y)")
    cases = ((2,3),(6,2),(7,1),(1,4),(5,5),(9,6),(3,8),(4,9),(8,7))
    coord_result=((2,3,1),(6,2,2),(7,1,3),(1,4,4),(5,5,5),(9,6,6),(3,8,7),(4,9,8),(8,7,9))

    for ((column,row),coord_result) in zip(cases,coord_result):
        c = grille.getCase(column, row)
        if c != coord_result:
            print("getCase(",(column,row),") Ko", c.getCoordinate(),coord_result)

    # ---- test la méthode getCase(x,y)
    print("Test 5 - test la méthode getCase(Cordinate(x,y))")
    cases = ((2,3),(6,2),(7,1),(1,4),(5,5),(9,6),(3,8),(4,9),(8,7))
    coord_result=((2,3,1),(6,2,2),(7,1,3),(1,4,4),(5,5,5),(9,6,6),(3,8,7),(4,9,8),(8,7,9))

    for ((column,row),coord_result) in zip(cases,coord_result):
        coord = Coordinate(column, row)
        c = grille.getCase(coord)
        if c != coord_result:
            print("getCase(",coord,") Ko", c.getCoordinate(),coord_result)

    # ---- test la méthode getCase(x,y)
    print("Test 6 - test la méthode getCase(nb_case)")
    cases = (20,15,7,28,41,54,66,76,62)
    coord_result=((2,3,1),(6,2,2),(7,1,3),(1,4,4),(5,5,5),(9,6,6),(3,8,7),(4,9,8),(8,7,9))

    for (nb_case,coord_result) in zip(cases,coord_result):
        c = grille.getCase(nb_case)
        if c != coord_result:
            print("getCase(",nb_case,") Ko", c.getCoordinate(),coord_result)

    # --- Test de la méthode getNearCases()
    print("Test 7 - test la méthode getNearCases(ref_case)")
    cases = (20,15,7,28,41,54,66,76,62)
    coords_result=(((1,3,1),(3,3,1),(4,3,2),(5,3,2),(6,3,2),(7,3,3),(8,3,3),(9,3,3),
            (2,1,1),(2,2,1),(2,4,4),(2,5,4),(2,6,4),(2,7,7),(2,8,7),(2,9,7),
            (1,1,1),(1,2,1),(1,3,1),(2,1,1),(2,2,1),(3,1,1),(3,2,1),(3,3,1)),
            ((1,2,1),(2,2,1),(3,2,1),(4,2,2),(5,2,2),(7,2,3),(8,2,3),(9,2,3),
            (6,1,2),(6,3,2),(6,4,5),(6,5,5),(6,6,5),(6,7,8),(6,8,8),(6,9,8),
            (4,1,2),(4,2,2),(4,3,2),(5,1,2),(5,2,2),(5,3,2),(6,1,2),(6,3,2)),
            ((1,1,1),(2,1,1),(3,1,1),(4,1,2),(5,1,2),(6,1,2),(8,1,3),(9,1,3),
            (7,2,3),(7,3,3),(7,4,6),(7,5,6),(7,6,6),(7,7,9),(7,8,9),(7,9,9),
            (7,2,3),(7,3,3),(8,1,3),(8,2,3),(8,3,3),(9,1,3),(9,2,3),(9,3,3)),
            ((2,4,4),(3,4,4),(4,4,5),(5,4,5),(6,4,5),(7,4,6),(8,4,6),(9,4,6),
            (1,1,1),(1,2,1),(1,3,1),(1,5,4),(1,6,4),(1,7,7),(1,8,7),(1,9,7),
            (1,5,4),(1,6,4),(2,4,4),(2,5,4),(2,6,4),(3,4,4),(3,5,4),(3,6,4)),
            ((1,5,4),(2,5,4),(3,5,4),(4,5,5),(6,5,5),(7,5,6),(8,5,6),(9,5,6),
            (5,1,2),(5,2,2),(5,3,2),(5,4,5),(5,6,5),(5,7,8),(5,8,8),(5,9,8),
            (4,4,5),(4,5,5),(4,6,5),(5,4,5),(5,6,5),(6,4,5),(6,5,5),(6,6,5)),
            ((1,6,4),(2,6,4),(3,6,4),(4,6,5),(5,6,5),(6,6,5),(7,6,6),(8,6,6),
            (9,1,3),(9,2,3),(9,3,3),(9,4,6),(9,5,6),(9,7,9),(9,8,9),(9,9,9),
            (7,4,6),(7,5,6),(7,6,6),(8,4,6),(8,5,6),(8,6,6),(9,4,6),(9,5,6)),
            ((1,8,7),(2,8,7),(4,8,8),(5,8,8),(6,8,8),(7,8,9),(8,8,9),(9,8,9),
            (3,1,1),(3,2,1),(3,3,1),(3,4,4),(3,5,4),(3,6,4),(3,7,7),(3,9,7),
            (1,7,7),(1,8,7),(1,9,7),(2,7,7),(2,8,7),(2,9,7),(3,7,7),(3,9,7)),
            ((1,9,7),(2,9,7),(3,9,7),(5,9,8),(6,9,8),(7,9,9),(8,9,9),(9,9,9),
            (4,1,2),(4,2,2),(4,3,2),(4,4,5),(4,5,5),(4,6,5),(4,7,8),(4,8,8),
            (4,7,8),(4,8,8),(5,7,8),(5,8,8),(5,9,8),(6,7,8),(6,8,8),(6,9,8)),
            ((1,7,7),(2,7,7),(3,7,7),(4,7,8),(5,7,8),(6,7,8),(7,7,9),(9,7,9),
            (8,1,3),(8,2,3),(8,3,3),(8,4,6),(8,5,6),(8,6,6),(8,8,9),(8,9,9),
            (7,7,9),(7,8,9),(7,9,9),(8,8,9),(8,9,9),(9,7,9),(9,8,9),(9,9,9)))
    
    for _i_test in range(0,9):
        c = grille.getCase(cases[_i_test])
        print("Case - Test 7.",_i_test + 1, " - " ,c.getCoordinate()," :")
        result = coords_result[_i_test]
        for (j,case) in zip(range(0,24),grille.getCases(c,Case.__COLUMN__) + grille.getCases(c,Case.__ROW__) + grille.getCases(c,Case.__SQUARE__)):
            r = case.getCoordinate()
            print(r, result[j],r == result[j])

    # --- Test de la méthode lookup()
    print("test 8 : Vérification de la méthode lookup()")
    # --- vérifier la recherche des cases à un chiffre et non résolue
    print("Test 8.1 : vérification de la recherche des cases à un chiffre et non résolue")
    # --- grille par défaut en mode "__INIT_STEP__"
    # --- la méthode s'arrête tout de suite
    grille1 = Grid()
    if grille1.lookup() != None:
        print("Test 8.1 - Ko")

    print(" ---------------------------")    
    # --- alimente la grille 'cohérente' et passe le mode en mode __READY_STEP__
    print("Test 9 : vérification de la recherche des cases à une chiffre et non résolue")
    grille_easy_resultat = [
        [[6],[5],[9],[7],[4],[8],[2],[1],[3]],
        [[3],[2],[8],[5],[1],[9],[6],[4],[7]],
        [[7],[4],[1],[6],[3],[2],[9],[8],[5]],
        [[5],[8],[7],[3],[9],[6],[1],[2],[4]],
        [[4],[1],[6],[8],[2],[7],[5],[3],[9]],
        [[9],[3],[2],[4],[5],[1],[8],[7],[6]],
        [[2],[9],[5],[1],[7],[4],[3],[6],[8]],
        [[1],[6],[4],[9],[8],[3],[7],[5],[2]],
        [[8],[7],[3],[2],[6],[5],[4],[9],[1]]]
    list_cases_easy = ((1,2,3),(1,4,5),(1,5,4),(2,3,4),(2,5,1),(2,6,3),(2,9,7),
                 (3,7,5),(3,9,3),(4,2,5),(4,3,6),(4,4,3),(4,5,8),
                (4,6,4),(4,7,1),(4,9,2),(5,5,2),(5,6,5),(5,7,7),
                (5,8,8),(6,1,8),(6,2,9),(6,4,6),(6,6,1),(6,9,5),
                (7,3,9),(7,7,3),(7,9,4),(8,1,1),(8,3,8),(8,4,2),
                (8,6,7),(8,7,6),(8,8,5),(9,2,7),(9,3,5),(9,4,4),
                (9,6,6),(9,7,8),(9,9,1))

    if grille1.setValues(list_cases_easy) != 40:
            print("Test 9.1 - Ko grille non mise à jour!")
            exit(1)

    grille_resultat_methodA = [
        [[6],[5],[9],[7],[4],[8],[2],[1],[3]],
        [[3],[2],[8],[5],[1],[9],[6],[4],[7]],
        [[7],[4],[1],[6],[3],[2],[9],[8],[5]],
        [[5],[8],[7],[3],[9],[6],[1],[2],[4]],
        [[4],[1],[6],[8],[2],[7],[5],[3],[9]],
        [[9],[3],[2],[4],[5],[1],[8],[7],[6]],
        [[2],[9],[5],[1],[7],[4],[3],[6],[8]],
        [[1],[6],[4],[9],[8],[3],[7],[5],[2]],
        [[8],[7],[3],[2],[6],[5],[4],[9],[1]]]
    
    print(grille1)
    print("Test 9.2 - exécution de la méthode A")
    while grille1._lookup_methodA() != 0:
        pass
    print("Test 9.2 - test si la grille est le résultat attendu", grille1 == grille_resultat_methodA)
    print(grille1)
    print(" ---------------------------")
    
    # --- Test la méthode B
    print("Test 10 - Test de la méthode de résolution B")
    grille1 = Grid()
    grille_moyenne_resultat = [
        [[6],[8],[1],[4],[5],[7],[2],[3],[9]],
        [[7],[9],[5],[2],[1],[3],[4],[6],[8]],
        [[3],[2],[4],[6],[9],[8],[7],[5],[1]],
        [[5],[6],[8],[9],[7],[1],[3],[4],[2]],
        [[2],[1],[7],[3],[4],[6],[9],[8],[5]],
        [[9],[4],[3],[5],[8],[2],[6],[1],[7]],
        [[8],[3],[6],[1],[2],[9],[5],[7],[4]],
        [[1],[5],[2],[7],[3],[4],[8],[9],[6]],
        [[4],[7],[9],[8],[6],[5],[1],[2],[3]]]

    list_cases_moyenne = ((1,2,7),(1,4,5),(1,5,2),
                        (2,2,9),(2,3,2),(2,4,6),(2,6,4),
                        (3,2,5),(3,5,7),(3,9,9),
                        (4,6,5),(4,7,1),(4,8,7),
                        (5,3,9),(5,7,2),
                        (6,2,3),(6,3,8),(6,4,1),
                        (7,1,2),(7,5,9),(7,8,8),
                        (8,4,4),(8,6,1),(8,7,7),(8,8,9),
                        (9,5,5),(9,6,7),(9,8,6))

    grille_resultat_methodA1 = [
                        [[1,3,4,6,8],[3,8],[1,4,6],[4,6],[1,4,5,6],[4,5,6,7],[2],[3,5],[1,3,4,8,9]],
                        [[7],[9],[5],[2,4],[1,4],[3],[1,4],[6],[1,4,8]],
                        [[1,3,4,6],[2],[1,4,6],[4,6],[9],[8],[1,4,5,7],[3,5],[1,3,4]],
                        [[5],[6],[8],[9],[7],[1],[3],[4],[2]],
                        [[2],[1],[7],[3,4,6],[3,4,6],[4,6],[9],[8],[5]],
                        [[9],[4],[3],[5],[8],[2],[6],[1],[7]],
                        [[3,4,6,8],[3,5,8],[4,6],[1],[2],[4,5,6,9],[4,5],[7],[3,4]],
                        [[1,3,4],[3,5],[1,2,4],[7],[3,4,5],[4,5],[8],[9],[6]],
                        [[1,3,4,6,8],[3,5,7,8],[9],[3,4,6,8],[3,4,5,6],[4,5,6],[1,4,5],[2,3,5],[1,3,4]]]

    grille_resultat_methodB1 = [
                        [[1,3,4,6,8],[3,8],[1,4,6],[4,6],[1,4,5,6],[7],[2],[3,5],[9]],
                        [[7],[9],[5],[2],[1,4],[3],[1,4],[6],[8]],
                        [[1,3,4,6],[2],[1,4,6],[4,6],[9],[8],[7],[5],[1,3,4]],
                        [[5],[6],[8],[9],[7],[1],[3],[4],[2]],
                        [[2],[1],[7],[3,4,6],[3,4,6],[4,6],[9],[8],[5]],
                        [[9],[4],[3],[5],[8],[2],[6],[1],[7]],
                        [[3,4,6,8],[3,5,8],[4,6],[1],[2],[9],[4,5],[7],[3,4]],
                        [[1,3,4],[3,5],[2],[7],[3,4,5],[4,5],[8],[9],[6]],
                        [[1,3,4,6,8],[7],[9],[8],[3,4,5,6],[4,5,6],[1,4,5],[2],[1,3,4]]]

    grille_resultat_methodA2 = [
                        [[1,4,6],   [8],    [1,4,6],[4,6],  [1,4,5,6],  [7],    [2],    [3],[9]],
                        [[7],       [9],    [5],    [2],    [1,4],      [3],    [1,4],  [6],[8]],
                        [[1,3,4,6], [2],    [1,4,6],[4,6],  [9],        [8],    [7],    [5],[1,4]],
                        [[5],       [6],    [8],    [9],    [7],        [1],    [3],    [4],[2]],
                        [[2],       [1],    [7],    [3,4,6],[3,4,6],    [4,6],  [9],    [8],[5]],
                        [[9],       [4],    [3],    [5],    [8],        [2],    [6],    [1],[7]],
                        [[3,4,6,8], [3,5],  [4,6],  [1],    [2],        [9],    [4,5],  [7],[3,4]],
                        [[1,3,4],   [3,5],  [2],    [7],    [3,4,5],    [4,5],  [8],    [9],[6]],
                        [[1,3,4,6], [7],    [9],    [8],    [3,4,5,6],  [4,5,6],[1,4,5],[2],[1,3,4]]]
   

    grille_resultat_methodB2 = [
                        [[1,4,6],   [8],    [1,4,6],[4,6],  [5],        [7],    [2],    [3],    [9]],
                        [[7],       [9],    [5],    [2],    [1],        [3],    [4],    [6],    [8]],
                        [[3],       [2],    [1,4,6],[4,6],  [9],        [8],    [7],    [5],    [1]],
                        [[5],       [6],    [8],    [9],    [7],        [1],    [3],    [4],    [2]],
                        [[2],       [1],    [7],    [3],    [3,4,6],    [4,6],  [9],    [8],    [5]],
                        [[9],       [4],    [3],    [5],    [8],        [2],    [6],    [1],    [7]],
                        [[8],       [3,5],  [6],    [1],    [2],        [9],    [4,5],  [7],    [3,4]],
                        [[1],       [3,5],  [2],    [7],    [3,4,5],    [4,5],  [8],    [9],    [6]],
                        [[4],       [7],    [9],    [8],    [3,4,5,6],  [4,5,6],[1],    [2],    [1,3,4]]]

    grille_resultat_methodA3 = [
                        [[1,6],     [8],    [1],    [4],    [5],        [7],    [2],    [3],    [9]],
                        [[7],       [9],    [5],    [2],    [1],        [3],    [4],    [6],    [8]],
                        [[3],       [2],    [4],    [6],    [9],        [8],    [7],    [5],    [1]],
                        [[5],       [6],    [8],    [9],    [7],        [1],    [3],    [4],    [2]],
                        [[2],       [1],    [7],    [3],    [4],        [6],    [9],    [8],    [5]],
                        [[9],       [4],    [3],    [5],    [8],        [2],    [6],    [1],    [7]],
                        [[8],       [3],    [6],    [1],    [2],        [9],    [5],    [7],    [4]],
                        [[1],       [5],    [2],    [7],    [3],        [4],    [8],    [9],    [6]],
                        [[4],       [7],    [9],    [8],    [6],        [5],    [1],    [2],    [3]]]
   
    if grille1.setValues(list_cases_moyenne) != 28:
            print("Test 10.1 - Ko grille non mise à jour!")
            exit(1)

    print(grille1)
    print("Test 10.2 - exécution de la méthode A")
    while grille1._lookup_methodA() != 0:
        pass
    print("Test 10.2 - teste si la grille est le résultat attendu", grille1 == grille_resultat_methodA1)
    print(grille1)
    print("Test 10.3 - exécution de la méthode B :", grille1._lookup_methodB())
    print("Test 10.3 - teste si la grille est le résultat attendu", grille1 == grille_resultat_methodB1)
    print(grille1)
    print("Test 10.4 - (r)exécution de la méthode A")
    while grille1._lookup_methodA() != 0:
        pass
    print("Test 10.4 - teste si la grille est le résultat attendu", grille1 == grille_resultat_methodA2)
    print(grille1)
    print("Test 10.5 - exécution de la méthode B :", grille1._lookup_methodB())
    print("Test 10.5 - teste si la grille est le résultat attendu", grille1 == grille_resultat_methodB2)
    print(grille1)
    print("Test 10.6 - (r)exécution de la méthode A")
    while grille1._lookup_methodA() != 0:
        pass
    print("Test 10.6 - teste si la grille est le résultat attendu", grille1 == grille_resultat_methodA3)
    print(grille1)
    print("Test 10 - test sur la résolution de la grille à la main", grille1 == grille_moyenne_resultat)
    print(" ---------------------------")

    grille1 = Grid()
    grille_hard_resultat = [
        [[3],[5],[9],[7],[6],[4],[2],[1],[8]],
        [[2],[8],[7],[9],[5],[1],[6],[4],[3]],
        [[4],[6],[1],[2],[3],[8],[9],[5],[7]],
        [[6],[1],[3],[5],[4],[7],[8],[2],[9]],
        [[7],[9],[8],[3],[1],[2],[4],[6],[5]],
        [[5],[2],[4],[6],[8],[9],[3],[7],[1]],
        [[8],[4],[6],[1],[9],[5],[7],[3],[2]],
        [[9],[7],[5],[4],[2],[3],[1],[8],[6]],
        [[1],[3],[2],[8],[7],[6],[5],[9],[4]]]
    
    list_cases_hard = ((1,5,7),(1,6,5),
                       (2,1,5),(2,3,6),(2,7,4),
                       (3,1,9),(3,4,3),(3,5,8),(3,9,2),
                       (4,5,3),(4,7,1),(4,9,8),
                       (5,1,6),(5,3,3),(5,7,9),(5,9,7),
                       (6,1,4),(6,3,8),(6,5,2),
                       (7,1,2),(7,5,4),(7,6,3),(7,9,5),
                       (8,3,5),(8,7,3),(8,9,9),
                       (9,4,9),(9,5,5))

    grille_resultat_methodAB1 = [
                        [[1],   [5],    [9],    [7],    [6],    [4],    [2],    [8],    [3]],
                        [[3],   [8],    [7],    [9],    [2],    [1],    [6],    [4],    [6]],
                        [[2],   [6],    [4],    [5],    [3],    [8],    [9],    [5],    [1]],
                        [[4],   [1],    [3],    [6],    [5],    [7],    [8],    [2],    [9]],
                        [[7],   [9],    [8],    [3],    [1],    [2],    [4],    [6],    [5]],
                        [[5],   [1],    [6],    [4],    [8],    [9],    [3],    [2],    [7]],
                        [[8],   [4],    [5],    [1],    [9],    [6],    [7],    [3],    [2]],
                        [[9],   [7],    [5],    [2],    [4],    [3],    [1],    [1],    [8]],
                        [[6],   [3],    [2],    [8],    [7],    [3],    [5],    [9],    [4]]]


    if grille1.setValues(list_cases_hard) != 28:
            print("Test 11.1 - Ko grille non mise à jour!")
            exit(1)
            
    print(grille1)
            
    print("Test 11.2 - exécution de la méthode A et méthode B")
    
    resolution=True
    while resolution == True:
        while grille1._lookup_methodA() != 0:
            pass
        if grille1._lookup_methodB() == 0: resolution=False
    
    print("Test 11 - test sur la résolution de la grille à la main", grille1 == grille_hard_resultat)
    print(grille1)
    print(" ---------------------------")

    # --- Test la méthode C
    print("Test 12 - Test de la méthode de résolution C")
    grille1 = Grid()
    grille_demoniac_resultat = [
        [[8],[1],[6],[5],[7],[2],[4],[3],[9]],
        [[2],[4],[3],[6],[9],[8],[1],[5],[7]],
        [[5],[9],[7],[3],[1],[4],[8],[6],[2]],
        [[6],[5],[9],[4],[2],[7],[3],[1],[8]],
        [[1],[7],[4],[8],[3],[5],[9],[2],[6]],
        [[3],[2],[8],[9],[6],[1],[5],[7],[4]],
        [[7],[8],[1],[2],[5],[9],[6],[4],[3]],
        [[9],[6],[2],[1],[4],[3],[7],[8],[5]],
        [[4],[3],[5],[7],[8],[6],[2],[9],[1]]]

    list_cases_demoniac = ((1,2,2),(1,6,3),
                       (2,1,1),(2,2,4),(2,4,5),(2,7,8),(2,8,6),
                       (3,3,7),(3,4,9),(3,9,5),
                       (4,8,1),
                       (5,2,9),(5,4,2),(5,6,6),(5,8,4),
                       (6,2,8),
                       (7,1,4),(7,6,5),(7,7,6),
                       (8,2,5),(8,3,6),(8,6,7),(8,8,8),(8,9,9),
                       (9,4,8),(9,8,5))

    grille_resultat_methodAB1 = [
        [[8],       [1],    [6],        [2,5,7],    [5,7],      [2,5,7],    [4],    [3],    [9]],
        [[2],       [4],    [3],        [6],        [9],        [8],        [1],    [5],    [7]],
        [[5],       [9],    [7],        [3,4],      [1,3],      [1,4],      [8],    [6],    [2]],
        [[6],       [5],    [9],        [4,7],      [2],        [1,4,7],    [3],    [1,4],  [8]],
        [[1,4],     [7],    [1,4,8],    [3,4,5,8],  [1,3,5,8],  [1,4,5],    [9],    [2],    [6]],
        [[3],       [2],    [1,4,8],    [4,8,9],    [6],        [1,4,9],    [5],    [7],    [1,4]],
        [[1,4,7],   [8],    [1,4],      [2,5,7,9],  [5,7],      [2,5,7,9],  [6],    [1,4],  [3]],
        [[9],       [6],    [2],        [1],        [4],        [3],        [7],    [8],    [5]],
        [[1,4,7],   [3],    [5],        [7,8],      [7,8],      [6],        [2],    [9],    [1,4]]]
    
    grille_resultat_methodC1=[
        [[8],       [1],    [6],        [2,5,7],    [5,7],      [2,5,7],    [4],    [3],    [9]],
        [[2],       [4],    [3],        [6],        [9],        [8],        [1],    [5],    [7]],
        [[5],       [9],    [7],        [3,4],      [1,3],      [1,4],      [8],    [6],    [2]],
        [[6],       [5],    [9],        [4,7],      [2],        [1,4,7],    [3],    [1,4],  [8]],
        [[1,4],     [7],    [1,4,8],    [3,4,5,8],  [1,3,8],    [1,4,5],    [9],    [2],    [6]],
        [[3],       [2],    [1,4,8],    [4,8,9],    [6],        [1,4,9],    [5],    [7],    [1,4]],
        [[7],       [8],    [1,4],      [2,5,7,9],  [5,7],      [2,5,7,9],  [6],    [1,4],  [3]],
        [[9],       [6],    [2],        [1],        [4],        [3],        [7],    [8],    [5]],
        [[1,4,7],   [3],    [5],        [7,8],      [8],        [6],        [2],    [9],    [1,4]]]

    if grille1.setValues(list_cases_demoniac) != 26:
            print("Test 12.1 - Ko grille non mise à jour!")
            exit(1)
            
    resolution=True
    while resolution == True:
        print("Test 12.2 - exécution de la méthode A et méthode B")    
        while grille1._lookup_methodA() != 0:
            pass
        if grille1._lookup_methodB() == 0: 
            print("Test 12.3 - exécution de la méthode C")    
            if grille1._lookup_methodC() == 0:
                resolution=False
            print("test 12.3 - resultat de l'exécution de la méthode C\n", grille1)

    print("Test 12 - test sur la résolution de la grille à la main", grille1 == grille_demoniac_resultat)
    print(grille1)
    print(" ---------------------------")
    
    # --- Test de la méthode lookup
    print("Test 13 - test de la résolution avec la méthode lookup()")

    print("Test 13.1 - Résolution d'une grille de niveau facile")
    grille2 = Grid()
    grille_easy_resultat = [
        [[6],[5],[9],[7],[4],[8],[2],[1],[3]],
        [[3],[2],[8],[5],[1],[9],[6],[4],[7]],
        [[7],[4],[1],[6],[3],[2],[9],[8],[5]],
        [[5],[8],[7],[3],[9],[6],[1],[2],[4]],
        [[4],[1],[6],[8],[2],[7],[5],[3],[9]],
        [[9],[3],[2],[4],[5],[1],[8],[7],[6]],
        [[2],[9],[5],[1],[7],[4],[3],[6],[8]],
        [[1],[6],[4],[9],[8],[3],[7],[5],[2]],
        [[8],[7],[3],[2],[6],[5],[4],[9],[1]]]

    list_cases_easy = ((1,2,3),(1,4,5),(1,5,4),(2,3,4),(2,5,1),(2,6,3),(2,9,7),
                 (3,7,5),(3,9,3),(4,2,5),(4,3,6),(4,4,3),(4,5,8),
                (4,6,4),(4,7,1),(4,9,2),(5,5,2),(5,6,5),(5,7,7),
                (5,8,8),(6,1,8),(6,2,9),(6,4,6),(6,6,1),(6,9,5),
                (7,3,9),(7,7,3),(7,9,4),(8,1,1),(8,3,8),(8,4,2),
                (8,6,7),(8,7,6),(8,8,5),(9,2,7),(9,3,5),(9,4,4),
                (9,6,6),(9,7,8),(9,9,1))

    if grille2.setValues(list_cases_easy) != 40:
            print("Test 13.1 - Ko grille non mise à jour!")
            exit(1)
    grille2.lookup()
    print(grille2)
    print("Test 13.1 - test si la grille est le résultat attendu", grille2 == grille_easy_resultat)

    print(" ---------------------------")
    print("Test 13.2 - Résolution d'une grille de niveau moyenne")
    grille2 = Grid()
    grille_moyenne_resultat = [
        [[6],[8],[1],[4],[5],[7],[2],[3],[9]],
        [[7],[9],[5],[2],[1],[3],[4],[6],[8]],
        [[3],[2],[4],[6],[9],[8],[7],[5],[1]],
        [[5],[6],[8],[9],[7],[1],[3],[4],[2]],
        [[2],[1],[7],[3],[4],[6],[9],[8],[5]],
        [[9],[4],[3],[5],[8],[2],[6],[1],[7]],
        [[8],[3],[6],[1],[2],[9],[5],[7],[4]],
        [[1],[5],[2],[7],[3],[4],[8],[9],[6]],
        [[4],[7],[9],[8],[6],[5],[1],[2],[3]]]

    list_cases_moyenne = ((1,2,7),(1,4,5),(1,5,2),
                        (2,2,9),(2,3,2),(2,4,6),(2,6,4),
                        (3,2,5),(3,5,7),(3,9,9),
                        (4,6,5),(4,7,1),(4,8,7),
                        (5,3,9),(5,7,2),
                        (6,2,3),(6,3,8),(6,4,1),
                        (7,1,2),(7,5,9),(7,8,8),
                        (8,4,4),(8,6,1),(8,7,7),(8,8,9),
                        (9,5,5),(9,6,7),(9,8,6))

    if grille2.setValues(list_cases_moyenne) != 28:
            print("Test 13.2 - Ko grille non mise à jour!")
            exit(1)
            
    grille2.lookup()
    print(grille2)
    print("Test 13.2 - test si la grille est le résultat attendu", grille2 == grille_moyenne_resultat)

    print(" ---------------------------")
    print("Test 13.3 - Résolution d'une grille de niveau difficile")
    grille2 = Grid()
    grille_hard_resultat = [
        [[3],[5],[9],[7],[6],[4],[2],[1],[8]],
        [[2],[8],[7],[9],[5],[1],[6],[4],[3]],
        [[4],[6],[1],[2],[3],[8],[9],[5],[7]],
        [[6],[1],[3],[5],[4],[7],[8],[2],[9]],
        [[7],[9],[8],[3],[1],[2],[4],[6],[5]],
        [[5],[2],[4],[6],[8],[9],[3],[7],[1]],
        [[8],[4],[6],[1],[9],[5],[7],[3],[2]],
        [[9],[7],[5],[4],[2],[3],[1],[8],[6]],
        [[1],[3],[2],[8],[7],[6],[5],[9],[4]]]

    list_cases_hard = ((1,5,7),(1,6,5),
                       (2,1,5),(2,3,6),(2,7,4),
                       (3,1,9),(3,4,3),(3,5,8),(3,9,2),
                       (4,5,3),(4,7,1),(4,9,8),
                       (5,1,6),(5,3,3),(5,7,9),(5,9,7),
                       (6,1,4),(6,3,8),(6,5,2),
                       (7,1,2),(7,5,4),(7,6,3),(7,9,5),
                       (8,3,5),(8,7,3),(8,9,9),
                       (9,4,9),(9,5,5))

    if grille2.setValues(list_cases_hard) != 28:
            print("Test 13.3 - Ko grille non mise à jour!")
            exit(1)
            
    grille2.lookup()
    print(grille2)
    print("Test 13.3 - test si la grille est le résultat attendu", grille2 == grille_hard_resultat)

    print(" ---------------------------")
    print("Test 13.4 - Résolution d'une grille de niveau diabolique")
    grille2 = Grid()
    grille_demoniac_resultat = [
        [[8],[1],[6],[5],[7],[2],[4],[3],[9]],
        [[2],[4],[3],[6],[9],[8],[1],[5],[7]],
        [[5],[9],[7],[3],[1],[4],[8],[6],[2]],
        [[6],[5],[9],[4],[2],[7],[3],[1],[8]],
        [[1],[7],[4],[8],[3],[5],[9],[2],[6]],
        [[3],[2],[8],[9],[6],[1],[5],[7],[4]],
        [[7],[8],[1],[2],[5],[9],[6],[4],[3]],
        [[9],[6],[2],[1],[4],[3],[7],[8],[5]],
        [[4],[3],[5],[7],[8],[6],[2],[9],[1]]]

    list_cases_demoniac = ((1,2,2),(1,6,3),
                       (2,1,1),(2,2,4),(2,4,5),(2,7,8),(2,8,6),
                       (3,3,7),(3,4,9),(3,9,5),
                       (4,8,1),
                       (5,2,9),(5,4,2),(5,6,6),(5,8,4),
                       (6,2,8),
                       (7,1,4),(7,6,5),(7,7,6),
                       (8,2,5),(8,3,6),(8,6,7),(8,8,8),(8,9,9),
                       (9,4,8),(9,8,5))

    if grille2.setValues(list_cases_demoniac) != 26:
            print("Test 13.4 - Ko grille non mise à jour!")
            exit(1)
            
    grille2.lookup()
    print(grille2)
    print("Test 13.4 - test si la grille est le résultat attendu", grille2 == grille_demoniac_resultat)
    print(" ---------------------------")

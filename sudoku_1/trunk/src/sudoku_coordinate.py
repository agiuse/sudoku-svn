# -*- coding: utf-8 -*-
'''
Created on 27 juil. 2011

@author: eagius
'''
# -----------------------------------------------------------------------------------
class Coordinate(object):
    """
        Classe gérant les coordonnées dans la grille.
        Cette classe lie entre elles les differents objets de la grille.
        Calcule la position automatiquement en fonction de son numéro de cases
    """

    def __init__(self, _index_x, _index_y=0):

        if _index_y == 0 :
            if  _index_x < 1 or _index_x > 81 :
                raise(ValueError)
            self.__row = ((_index_x - 1 ) // 9 ) + 1
            self.__column = ((_index_x - 1 ) % 9 ) + 1
        else:
            if (_index_x < 1 or _index_x > 9) or (_index_y < 1 or _index_y > 9) :
                raise(ValueError)

            self.__column = _index_x
            self.__row = _index_y
    
    def row(self):
        return  ( self.__row )

    def column(self):
        return ( self.__column )

    def square(self):
        if self.__column >= 1 and self.__column <= 3:
            if self.__row >=1 and self.__row <=3:
                return(1)

        if self.__column >= 1 and self.__column <= 3:
            if self.__row >=4 and self.__row <=6:
                return(4)

        if self.__column >= 1 and self.__column <= 3:
            if self.__row >=7 and self.__row <=9:
                return(7)

        if self.__column >= 4 and self.__column <= 6:
            if self.__row >=1 and self.__row <=3:
                return(2)

        if self.__column >= 4 and self.__column <= 6:
            if self.__row >=4 and self.__row <=6:
                return(5)

        if self.__column >= 4 and self.__column <= 6:
            if self.__row >=7 and self.__row <=9:
                return(8)

        if self.__column >= 7 and self.__column <= 9:
            if self.__row >=1 and self.__row <=3:
                return(3)

        if self.__column >= 7 and self.__column <= 9:
            if self.__row >=4 and self.__row <=6:
                return(6)

        if self.__column >= 7 and self.__column <= 9:
            if self.__row >=7 and self.__row <=9:
                return(9)

    def getListColumn(self):
        """
        La méthode fournit une liste de coordonnées sous forme d'objet coordinate
        correspondant à toutes les coordonnées à partir de la colonne de la coordonnée courante
        """
        _row = self.row()
        return([Coordinate(_column,_row) for _column in range(1,10)])

        return(list)
        
    def getListRow(self):
        """
        La méthode fournit une liste de coordonnées sous forme d'objets Coordinate
        correspondant à toutes les coordonnées à partir de la ligne de la coordonnée courante
        """
        _column = self.column()
        return([Coordinate(_column,_row) for _row in range(1,10)])

    def getListSquare(self):   
        """
        La méthode fournit une liste de coordonnées sous forme d'objets Coordinate
        correspondant au carré de la coordonnée.
        """
        # square 1,4,7 - 1,3
        # square 2,5,8 - 4,6
        # square 3,6,9 - 7,9
        _square = self.square()
        _row_ref = ( (  _square - 1 ) // 3) * 3
        _column_ref = ( ( _square - 1 ) % 3) * 3
        
        _list_coords=[(1+_column_ref,1+ _row_ref),(1+_column_ref,2+ _row_ref),(1+_column_ref,3+ _row_ref),
                      (2+_column_ref,1+ _row_ref),(2+_column_ref,2+ _row_ref),(2+_column_ref,3+ _row_ref),
                      (3+_column_ref,1+ _row_ref),(3+_column_ref,2+ _row_ref),(3+_column_ref,3+ _row_ref)]
        
        return([Coordinate(_column,_row) for (_column,_row) in _list_coords])
    
    def __eq__(self, coord):
        """
        Compare deux coordonnées entre elles
        """
        if isinstance(coord, Coordinate):
            return( self.column() == coord.column() and self.row() == coord.row() and self.square() == coord.square())

        if isinstance(coord,tuple):
            return( (self.column(), self.row(), self.square()) == coord)

        return(None)

    def __ne__(self, coord):
        """
        Compare deux coordonnées entre elles
        """
        return(not self.__eq__(coord))
    
    def __str__(self):
        """
        Affichage dans l'interpreteur
        """
        return("(c = {0}, r = {1}, s = {2})".format(self.column(), self.row(), self.square()))

    def __repr__(self):
        """
        Affichage dans l'interpreteur
        """
        return("(c = {0}, r = {1}, s = {2})".format(self.column(), self.row(), self.square()))
        
# -----------------------------------------------------------------------------------
if __name__ == '__main__':

    # --- Test hors limite
    print("Test 1 - test hors limite")
    try:
        c = Coordinate(0,5)
    except ValueError:
        print("Test 1.1 - test hors limite x < 1 Ko")
    
    try:
        c = Coordinate(10,5)
    except ValueError:
        print("Test 1.2 - test hors limite x > 10 Ko")

    try:
        c = Coordinate(5,0)
    except ValueError:
        print("Test 1.3 - test hors limite y < 1 Ko")

    try:
        c = Coordinate(5,10)
    except ValueError:  
        print("Test 1.4 - test hors limite y > 9 Ko")
        

    # 1 tuple contient 9 tuples de 
    coordinate_grid_9x9=[
            [
            [(1,3,1),(2,3,1),(3,3,1),(4,3,2),(5,3,2),(6,3,2),(7,3,3),(8,3,3),(9,3,3)],
            [(2,1,1),(2,2,1),(2,3,1),(2,4,4),(2,5,4),(2,6,4),(2,7,7),(2,8,7),(2,9,7)],
            [(1,1,1),(1,2,1),(1,3,1),(2,1,1),(2,2,1),(2,3,1),(3,1,1),(3,2,1),(3,3,1)]
            ],[
            [(1,2,1),(2,2,1),(3,2,1),(4,2,2),(5,2,2),(6,2,2),(7,2,3),(8,2,3),(9,2,3)],
            [(6,1,2),(6,2,2),(6,3,2),(6,4,5),(6,5,5),(6,6,5),(6,7,8),(6,8,8),(6,9,8)],
            [(4,1,2),(4,2,2),(4,3,2),(5,1,2),(5,2,2),(5,3,2),(6,1,2),(6,2,2),(6,3,2)]
            ],[
            [(1,1,1),(2,1,1),(3,1,1),(4,1,2),(5,1,2),(6,1,2),(7,1,3),(8,1,3),(9,1,3)],
            [(7,1,3),(7,2,3),(7,3,3),(7,4,6),(7,5,6),(7,6,6),(7,7,9),(7,8,9),(7,9,9)],
            [(7,1,3),(7,2,3),(7,3,3),(8,1,3),(8,2,3),(8,3,3),(9,1,3),(9,2,3),(9,3,3)]
            ],[
            [(1,4,4),(2,4,4),(3,4,4),(4,4,5),(5,4,5),(6,4,5),(7,4,6),(8,4,6),(9,4,6)],
            [(1,1,1),(1,2,1),(1,3,1),(1,4,4),(1,5,4),(1,6,4),(1,7,7),(1,8,7),(1,9,7)],
            [(1,4,4),(1,5,4),(1,6,4),(2,4,4),(2,5,4),(2,6,4),(3,4,4),(3,5,4),(3,6,4)],
            ],[
            [(1,5,4),(2,5,4),(3,5,4),(4,5,5),(5,5,5),(6,5,5),(7,5,6),(8,5,6),(9,5,6)],
            [(5,1,2),(5,2,2),(5,3,2),(5,4,5),(5,5,5),(5,6,5),(5,7,8),(5,8,8),(5,9,8)],
            [(4,4,5),(4,5,5),(4,6,5),(5,4,5),(5,5,5),(5,6,5),(6,4,5),(6,5,5),(6,6,5)]
            ],[
            [(1,6,4),(2,6,4),(3,6,4),(4,6,5),(5,6,5),(6,6,5),(7,6,6),(8,6,6),(9,6,6)],
            [(9,1,3),(9,2,3),(9,3,3),(9,4,6),(9,5,6),(9,6,6),(9,7,9),(9,8,9),(9,9,9)],
            [(7,4,6),(7,5,6),(7,6,6),(8,4,6),(8,5,6),(8,6,6),(9,4,6),(9,5,6),(9,6,6)]
            ],[
            [(1,8,7),(2,8,7),(3,8,7),(4,8,8),(5,8,8),(6,8,8),(7,8,9),(8,8,9),(9,8,9)],
            [(3,1,1),(3,2,1),(3,3,1),(3,4,4),(3,5,4),(3,6,4),(3,7,7),(3,8,7),(3,9,7)],
            [(1,7,7),(1,8,7),(1,9,7),(2,7,7),(2,8,7),(2,9,7),(3,7,7),(3,8,7),(3,9,7)]
            ],[
            [(1,9,7),(2,9,7),(3,9,7),(4,9,8),(5,9,8),(6,9,8),(7,9,9),(8,9,9),(9,9,9)],
            [(4,1,2),(4,2,2),(4,3,2),(4,4,5),(4,5,5),(4,6,5),(4,7,8),(4,8,8),(4,9,8)],
            [(4,7,8),(4,8,8),(4,9,8),(5,7,8),(5,8,8),(5,9,8),(6,7,8),(6,8,8),(6,9,8)]
            ],[
            [(1,7,7),(2,7,7),(3,7,7),(4,7,8),(5,7,8),(6,7,8),(7,7,9),(8,7,9),(9,7,9)],
            [(8,1,3),(8,2,3),(8,3,3),(8,4,6),(8,5,6),(8,6,6),(8,7,9),(8,8,9),(8,9,9)],
            [(7,7,9),(7,8,9),(7,9,9),(8,7,9),(8,8,9),(8,9,9),(9,7,9),(9,8,9),(9,9,9)]
            ]]

    # --- Test de la création de la coordonnées avec le numero de case
    print("Test 2 - vérification que les coordonnées soient correctes avec la méthode __init__()")
    coord_array = ((2,3),(6,2),(7,1),(1,4),(5,5),(9,6),(3,8),(4,9),(8,7))
    coord_resultat_array = ((2,3,1),(6,2,2),(7,1,3),(1,4,4),(5,5,5),(9,6,6),(3,8,7),(4,9,8),(8,7,9))
    for index_test in range(0,9):
        # --- creation de l'objet coordinate
        coord = Coordinate(coord_array[index_test][0],coord_array[index_test][1])
        # --- charge les coordonnées complète de la coordonnée
        coord_result = coord_resultat_array[ index_test ]
        
        print("Test 2.",index_test + 1, " - verifie que le calcul des coordonnées fonctionne pour la case", coord)
        # -- teste la méthode __eq__
        if coord != coord_result:
            print("Test Coordonnée incorrecte pour", coord, coord_result)
 
    
    # --- Test de la création de la coordonnées avec les coordonnées de case
    print("Test 3 - vérification que les coordonnées soient correctes avec la méthode __init__()")
    coord_array = (20,15,7,28,41,54,66,76,62)
    coord_resultat_array = ((2,3,1),(6,2,2),(7,1,3),(1,4,4),(5,5,5),(9,6,6),(3,8,7),(4,9,8),(8,7,9))
    for index_test in range(0,9):
        # --- creation de l'objet coordinate
        coord = Coordinate(coord_array[index_test])
        # --- charge les coordonnées complète de la coordonnée
        coord_result = coord_resultat_array[ index_test ]
        print("Test 3.",index_test+1, " - verifie que le calcul des coordonnées fonctionne pour", coord)
        # -- teste la méthode __eq__
        if coord != coord_result:
            print("Test Coordonnée incorrecte pour", coord,coord_result)

    # --- Verification des cases voisines
    print("Test 4 - vérification que les coordonnées voisines soient correctes avec les méthodes")
    coord_array = ((2,3),(6,2),(7,1),(1,4),(5,5),(9,6),(3,8),(4,9),(8,7))
    for index_test in range(0,9):
        # --- creation de l'objet coordinate
        coord = Coordinate(coord_array[index_test][0],coord_array[index_test][1])
        # --- Charge la liste des coordonnées pour cette coordonnée
        list_resultat = coordinate_grid_9x9[ index_test ]
        
        print("Test 4.",index_test+1, " - verifie que le calcul des coordonnées des cases voisines fonctionnent pour", coord)
        
        # -- test list des colonnes
        for (coordonnee, t_coordonnee) in zip(coord.getListColumn(),list_resultat[0]):
            if coordonnee != t_coordonnee:
                print("Test Column Ko")
                print("Object  :", coordonnee)
                print("Attendu :",t_coordonnee)

        for (coordonnee, t_coordonnee) in zip(coord.getListRow(),list_resultat[1]):
            if coordonnee != t_coordonnee:
                print("Test Row Ko")
                print("Object  :", coordonnee)
                print("Attendu :",t_coordonnee)
            
        for (coordonnee, t_coordonnee) in zip(coord.getListSquare(),list_resultat[2]):
            if coordonnee != t_coordonnee:
                print("Test Square Ko")
                print("Object  :", coordonnee)
                print("Attendu :",t_coordonnee)

    # --- test la comparaison
    c1 = Coordinate(3,6)
    c2 = Coordinate(3,6)
    c3 = Coordinate(8,6)
    
    print("Test 11 - comparaison de deux objets égaux")
    if  c1 != c2 :
        print('Ko')
        
    print("Test 12 - comparaison de deux objets différents")
    if c1 == c3:
        print('Ko')
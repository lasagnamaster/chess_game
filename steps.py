def check_step(figure, desk):
    """
    types:
    type 0 - pawn
    type 1 - lad'ya
    type 2 - slon
    type 3 - horse
    type 4 - queen
    type 5 - king
    """
    steps = [] 
    if figure.color == 0: k = -1
    else: k = 1

    #need rework!!
    if figure.type == 0:
        #not finished!!
        if figure.moved == False:
            if desk[self.x][self.y+k]==False:
                steps.append([0,1])
            if desk[self.x][self.y+2*k]==False:
                steps.append([0,2])
        else:
            if desk[self.x][self.y+k]==False:
                steps.append([0,1])

    if figure.type == 1:
        pass

    if figure.type == 2:
        pass

    if figure.type == 3:
        pass

    if figure.type == 4:
        pass

    if figure.type == 5:
        pass

    return steps
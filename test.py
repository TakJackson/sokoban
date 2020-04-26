def move(coord, direction, distance):
    '''
    finds and returns the coordinates of an element if it were moved in
    a given direction

    @param coord: the current coordinates of an element ex. (3, 4)

    @param direction

    @return
        the new coordinates of a moved element
    '''
    if direction == 'Up':
        return (coord[0], coord[1] - distance)
    if direction == 'Down':
        print(coord)
        return (coord[0], coord[1] + distance)
    if direction == 'Left':
        return (coord[0] - distance, coord[1])
    if direction == 'right':
        return (coord[0] + distance, coord[1])

move((2,3), 'Up', 1)
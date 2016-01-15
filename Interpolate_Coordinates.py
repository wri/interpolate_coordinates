def interpolate(coord, start, end):
    return []

def new_cycle(new_file, line, start, end, l_value, empty_coord, empty_coord):
    
    new_file.append(line)
            
    start['x'] = l_value[4]
    start['y'] = l_value[3]
    start['date'] = l_value[0]
    start['time'] = l_value[1]
            
    end['x'] = None
    end['y'] = None
    end['date'] = None
    end['time'] = None

    empty_coord = []
    
    return new_file, start, end
    

fname = 'path-to-file'
with open(fname) as f:
    start = {}
    end = {}
    new_file = []
    empty_coord = []
    i = 0
    for line in f:
        l_values = line.split(',')
        if i == 0:
            new_file.append(line)
        elif i == 1:

            new_file, start, end, empty_coord = new_cycle(new_file, line, start, end, l_value, empty_coord)
            
        
        else:
            if len(l_value[3]) == 0:
                empty_coord.append({"date":L_value[0], "time":l_value[1}})
            else:
                end['x'] = l_value[4]
                end['y'] = l_value[3]
                end['date'] = l_value[0]
                end['time'] = l_value[1]

                for coord in empty_coord:
                    new_line = interpolate(coord, start, end)
                    new_file.append(new_line)

                new_file, start, end, empty_coord = new_cycle(new_file, line, start, end, l_value, empty_coord)
                

    i += 1

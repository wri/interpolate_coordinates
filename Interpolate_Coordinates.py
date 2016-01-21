from datetime import datetime
import calendar
import os
import operator


def interpolate(coord, start, end, prop):

    if prop == "time":
        # extracting date and time into one object
        t0 = datetime.strptime('{0} {1}'.format(start['date'], start['time']), '%d-%b-%y %I:%M:%S %p')
        t1 = datetime.strptime('{0} {1}'.format(end['date'], end['time']), '%d-%b-%y %I:%M:%S %p')
        t_ = datetime.strptime('{0} {1}'.format(coord['date'], coord['time']), '%d-%b-%y %I:%M:%S %p')

        # calculating the time differences
        dt = calendar.timegm(t1.timetuple())-calendar.timegm(t0.timetuple())
        dt_ = calendar.timegm(t_.timetuple())-calendar.timegm(t0.timetuple())

        # calculate the coordinates using time difference
        coord['lat'] = float(start['lat']) + (float(end['lat'])-float(start['lat'])) * (float(dt_)/float(dt))
        coord['lon'] = float(start['lon']) + (float(end['lon'])-float(start['lon'])) * (float(dt_)/float(dt))

    elif prop == "dist":
        # calculate the coordinates using distance difference
        coord['lat'] = float(start['lat']) + (float(end['lat'])-float(start['lat'])) * ((float(coord['dist'])-float(start['dist']))/(float(end['dist'])-float(start['dist'])))
        coord['lon'] = float(start['lon']) + (float(end['lon'])-float(start['lon'])) * ((float(coord['dist'])-float(start['dist']))/(float(end['dist'])-float(start['dist'])))

    else:
        raise Exception("Unknown value")

    # return new line
    return coord


def update_coordinates(f, prop):

    fields = dict()
    fields['date'] = 2
    fields['time'] = 3
    fields['lat'] = 0
    fields['lon'] = 1
    fields['dist'] = 4

    sorted_fields = sorted(fields.items(), key=operator.itemgetter(1))

    start = dict()
    new_file = list()
    empty_coord = list()

    i = 0
    for line in f:
        l = line.split(',')

        l_value = dict()
        for key in fields.keys():
            l_value[key] = l[fields[key]].strip()

        if i == 0:
            new_file.append(line)
        elif i == 1:

            new_file.append(line)
            start = l_value
            empty_coord = list()

        else:
            if len(l_value['lat']) == 0:
                empty_coord.append(l_value)
            else:

                end = l_value

                for coord in empty_coord:
                    if len(coord[prop]) > 0:
                        coord = interpolate(coord, start, end, prop)

                    new_line = ''
                    i = 0
                    for sorted_field in sorted_fields:
                        if i == 0:
                            new_line = coord[sorted_field[0]]
                        else:
                            new_line = "{0},{1}".format(new_line, coord[sorted_field[0]])
                        i += 1
                    new_line = "{0}\n".format(new_line)
                    new_file.append(new_line)



                new_file.append(line)
                start = l_value
                empty_coord = list()

        i += 1
    return new_file



fname = r'C:\Users\Thomas.Maschler\Desktop\pa\Book1.csv'

print fname

# assumed file structure
# date, time, lat, lon, dist

with open(fname) as f:
    new_file = update_coordinates(f, "dist")

new_file = update_coordinates(new_file, "time")

dir_name = os.path.dirname(fname)
new_name = "{0}_new{1}".format(os.path.splitext(fname)[0],os.path.splitext(fname)[1])


with open(new_name, 'w') as f:
    for line in new_file:
      f.write("%s\n" % line)
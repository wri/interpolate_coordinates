from datetime import datetime
import calendar
import os
import operator

from optparse import OptionParser


def interpolate(coord, start, end, prop):

    if prop == "time":
        # extracting date and time into one object
        t0 = datetime.strptime('{0} {1}'.format(start['date'], start['time']), '%m/%d/%Y %H:%M:%S')
        t1 = datetime.strptime('{0} {1}'.format(end['date'], end['time']), '%m/%d/%Y %H:%M:%S')
        t_ = datetime.strptime('{0} {1}'.format(coord['date'], coord['time']), '%m/%d/%Y %H:%M:%S')

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


def update_coordinates(f, prop, fields):

    sorted_fields = sorted(fields.items(), key=operator.itemgetter(1))

    start = dict()
    new_file = list()
    empty_coord = list()

    i = 0
    for line in f:
        l = line.split(',')

        l_value = dict()
        for key in fields.keys():
            l_value[key] = l[int(fields[key])].strip()

        if i == 0:
            new_file.append(line)
        elif i == 1:

            new_file.append(line)
            start = l_value
            empty_coord = list()

        elif len(l_value['lon']) == 0 or len(l_value[prop]) == 0:
                empty_coord.append(l_value)

        else:





                end = l_value

                for coord in empty_coord:
                    if len(coord[prop]) > 0:
                        coord = interpolate(coord, start, end, prop)

                    new_line = ''
                    j = 0

                    for sorted_field in sorted_fields:
                        if j == 0:

                            new_line = coord[sorted_field[0]]
                        else:
                            new_line = "{0},{1}".format(new_line, coord[sorted_field[0]])
                        j += 1

                    new_line = "{0}\n".format(new_line)
                    new_file.append(new_line)



                new_file.append(line)
                start = l_value
                empty_coord = list()

        i += 1
    return new_file


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="input file", metavar="FILE")
    parser.add_option("-d", "--date", dest="date",
                      help="Date column", default=2)

    parser.add_option("-t", "--time", dest="time",
                      help="Time column", default=3)

    parser.add_option("-x", "--lon", dest="lon",
                      help="Lon column", default=1)

    parser.add_option("-y", "--lat", dest="lat",
                      help="Lat column", default=0)


    parser.add_option("-z", "--dist", dest="dist",
                      help="Dist column", default=4)

    parser.add_option("-m", "--methode", dest="methode",
                      help="Methode (dist, time)", default="dist")

    (options, args) = parser.parse_args()

    print options
    print args

    fields = dict()
    fields['date'] = options.date
    fields['time'] = options.time
    fields['lat'] = options.lat
    fields['lon'] = options.lon
    fields['dist'] = options.dist

    fname = options.filename #r'C:\Users\Thomas.Maschler\Desktop\lefini.csv'
    print fname

    # assumed file structure
    # date, time, lat, lon, dist

    with open(fname) as f:
       print "Interpolate coordinates using {}".format(options.methode)
       new_file = update_coordinates(f, options.methode, fields)

    dir_name = os.path.dirname(fname)

    
    new_name = "{0}_new{1}".format(os.path.splitext(fname)[0],os.path.splitext(fname)[1])
    print "Write result to {}".format(new_name) 
    with open(new_name, 'w') as f:
        for line in new_file:
          f.write("%s" % line)

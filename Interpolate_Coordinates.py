from datetime import datetime
from datetime import timedelta
import calendar
import os
import operator
import math

from optparse import OptionParser


def interpolate(value, start, end, options):

    if options.value == "time":
        if options.methode == 'dist':
            #try:
                t0 = datetime.strptime('{0} {1}'.format(start['date'], start['time']), '%m/%d/%Y %H:%M:%S')
                t1 = datetime.strptime('{0} {1}'.format(end['date'], end['time']), '%m/%d/%Y %H:%M:%S')
                dt = t1 - t0

                d0 = float(start['dist'])
                d1 = float(end['dist'])
                d_ = float(value['dist'])
                dd = d1 - d0
                dd_ = d_ - d0

                dt_ = dt.total_seconds() * dd_ / dd

                value['time'] = (t0 + timedelta(0, dt_)).strftime("%H:%M:%S")
            #except ValueError:
            #    print "Can't read date time:"
            #    print "{} {}".format(value['date'], value['time'])
        elif options.methode == 'lat':
            t0 = datetime.strptime('{0} {1}'.format(start['date'], start['time']), '%m/%d/%Y %H:%M:%S')
            t1 = datetime.strptime('{0} {1}'.format(end['date'], end['time']), '%m/%d/%Y %H:%M:%S')

            # calculating the time differences
            dt = t1 - t0

            dlat = float(end['lat']) - float(start['lat'])
            dlat_ = float(value['lat']) - float(start['lat'])
            dlon = float(end['lon']) - float(start['lon'])
            dlon_ = float(value['lon']) - float(start['lon'])

            dt_lat = dlat_ * dt.total_seconds()/dlat
            dt_lon = dlon_ * dt.total_seconds()/dlon
            dt_ = math.sqrt(dt_lat**2 + dt_lon**2)

            value['time'] = (t0 + timedelta(0, dt_)).strftime("%H:%M:%S")


    else:
        if options.methode == "time":
            try:
                # extracting date and time into one object
                t0 = datetime.strptime('{0} {1}'.format(start['date'], start['time']), '%m/%d/%Y %H:%M:%S')
                t1 = datetime.strptime('{0} {1}'.format(end['date'], end['time']), '%m/%d/%Y %H:%M:%S')
                t_ = datetime.strptime('{0} {1}'.format(value['date'], value['time']), '%m/%d/%Y %H:%M:%S')


                # calculating the time differences
                dt = calendar.timegm(t1.timetuple())-calendar.timegm(t0.timetuple())
                dt_ = calendar.timegm(t_.timetuple())-calendar.timegm(t0.timetuple())

                # calculate the coordinates using time difference
                value['lat'] = float(start['lat']) + (float(end['lat'])-float(start['lat'])) * (float(dt_)/float(dt))
                value['lon'] = float(start['lon']) + (float(end['lon'])-float(start['lon'])) * (float(dt_)/float(dt))
            except ValueError:
                print "Can't read date time:"
                print "{} {}".format(value['date'], value['time'])
        elif options.methode == "dist":
            # calculate the coordinates using distance difference
            value['lat'] = float(start['lat']) + (float(end['lat'])-float(start['lat'])) * ((float(value['dist'])-float(start['dist']))/(float(end['dist'])-float(start['dist'])))
            value['lon'] = float(start['lon']) + (float(end['lon'])-float(start['lon'])) * ((float(value['dist'])-float(start['dist']))/(float(end['dist'])-float(start['dist'])))

        else:
            raise Exception("Unknown value")

    # return new line
    return value


def update_values(f, options):
    
    fields = dict()
    fields['date'] = options.date
    fields['time'] = options.time
    fields['lat'] = options.lat
    fields['lon'] = options.lon
    fields['dist'] = options.dist

    sorted_fields = sorted(fields.items(), key=operator.itemgetter(1))

    start = dict()
    new_file = list()
    empty_values = list()

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
            empty_values = list()

        elif options.value == "coord" and len(l_value['lon']) == 0 or len(l_value[options.methode]) == 0:
                empty_values.append(l_value)
        
        elif options.value == "time" and len(l_value['time']) == 0:
                empty_values.append(l_value)

        else:

                end = l_value

                for value in empty_values:
                    if len(value[options.methode]) > 0:
                        value = interpolate(value, start, end, options)

                    new_line = ''
                    j = 0

                    for sorted_field in sorted_fields:
                        if j == 0:

                            new_line = value[sorted_field[0]]
                        else:
                            new_line = "{0},{1}".format(new_line, value[sorted_field[0]])
                        j += 1

                    new_line = "{0}\n".format(new_line)
                    new_file.append(new_line)

                new_file.append(line)
                start = l_value
                empty_values = list()

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
                      help="Methode (dist, time, lat)", default="dist")

    parser.add_option("-v", "--value", dest="value",
                      help="Value to interpolate (coord, time)", default="coord")

    (options, args) = parser.parse_args()

    print options
    print args

    fname = options.filename
    #fname =  r'C:\Users\Thomas.Maschler\Documents\oogue.csv'
    print fname

    # assumed file structure
    # date, time, lat, lon, dist

    with open(fname) as f:
       print "Interpolate coordinates using {}".format(options.methode)
       new_file = update_values(f, options)

    dir_name = os.path.dirname(fname)

    new_name = "{0}_new{1}".format(os.path.splitext(fname)[0],os.path.splitext(fname)[1])
    print "Write result to {}".format(new_name) 
    with open(new_name, 'w') as f:
        for line in new_file:
          f.write("%s" % line)

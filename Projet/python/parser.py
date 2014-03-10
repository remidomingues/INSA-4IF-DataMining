import csv, sys

def parse_csv(filepath, limit=-1):
    print "Parsing file {}...".format(filepath)
    
    headersDict = dict()
    data = []

    with open(filepath, 'rb') as f:
        reader = csv.reader(f)
        try:
            #Building headers indexes
            headers = reader.next()

            for i in range(0, len(headers)):
                headersDict[headers[i]] = i

            #Parsing data
            i = 0
            for row in reader:
                if i == limit:
                    break 
                data.append(row)
                i += 1

        except csv.Error as e:
            sys.exit('File %s, line %d: %s' % (filename, reader.line_num, e))

    print "Done ({} rows read)".format(len(data))

    return headersDict, data

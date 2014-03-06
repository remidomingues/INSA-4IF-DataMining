import csv, sys

class Parser(object):
    @staticmethod
    def parse_csv(filepath):
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
                    data.append(row)

            except csv.Error as e:
                sys.exit('File %s, line %d: %s' % (filename, reader.line_num, e))

        print "Done ({} rows read)".format(len(data))

        return headersDict, data

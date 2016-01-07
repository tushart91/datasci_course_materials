import MapReduce
import sys

"""
Problem 1: Inverted Index in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = set(value.split())
    for w in words:
        mr.emit_intermediate(w, key)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    mr.emit((key, list_of_values))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    debug = False
    # debug = True
    input = open(sys.argv[1])
    lines = open(sys.argv[2])
    dict = {}
    for line in lines:
        dict[line[0]] = set(line[1])

    for output in mr.execute(input, mapper, reducer):
        if debug:
            flag = True
            for value in output[1]:
                if value not in dict[output[0]]:
                    flag = False
                    break
                if not flag:
                    print output, flag
        if not debug:
            print output

    input.close()
    lines.close()

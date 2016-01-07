import MapReduce
import sys
from collections import defaultdict

"""
Problem 1: Inverted Index in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[1]
    value = record
    mr.emit_intermediate(key, value)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    dict = defaultdict(list)
    for record in list_of_values:
        dict[record[0]].append(record)

    for record_1 in dict["order"]:
        for record_2 in dict["line_item"]:
            row = []
            row.extend(record_1)
            row.extend(record_2)
            mr.emit(row)


# Do not modify below this line
# =============================
if __name__ == '__main__':
    debug = False
    # debug = True
    input = open(sys.argv[1])
    if debug:
        lines = open(sys.argv[2])

        for output in mr.__execute__(input, mapper, reducer):
            flag = False
            lines.seek(0)
            for line in lines:
                flag = line.strip() == output
                if flag:
                    break
            if not flag:
                print output
        lines.close()
    else:
        mr.execute(input, mapper, reducer)
    input.close()

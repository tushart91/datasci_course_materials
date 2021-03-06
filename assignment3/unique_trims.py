import MapReduce
import sys

"""
Unique Trims in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key   = record[1][:-10]
    value = True
    mr.emit_intermediate(key, value)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
    debug = False
    # debug = True
    input = open(sys.argv[1])
    if debug:
        lines = open(sys.argv[2])
        for output in mr.__execute__(input, mapper, reducer):
            flag = True
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

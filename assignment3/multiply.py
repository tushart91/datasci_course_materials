import MapReduce
import sys
from collections import defaultdict

"""
Matrix Multiply in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    for i in range(5):
        if record[0] == "a":
            key   = (record[1], i)
            value = [record[2], record[3]]
        else:
            key   = (i, record[2])
            value = [record[1], record[3]]
        mr.emit_intermediate(key, value)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    ret = list(key)
    dict = defaultdict(list)
    for i in range(len(list_of_values)):
        dict[list_of_values[i][0]].append(list_of_values[i][1])
    sum = 0
    for key, value in dict.items():
        if len(value) == 2:
            sum += value[0] * value[1]
    ret.append(sum)
    mr.emit(ret)

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

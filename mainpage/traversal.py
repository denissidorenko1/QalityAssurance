
class DimensionException(Exception):
    pass


# рекурсивная функция поиска пути между вершинами в матрице смежности
def traversal(N, a, b, INFUNCTION_RES_PATH):
    if a == b:
        return INFUNCTION_RES_PATH
    q = [a]
    vis = []
    while len(q) != 0:
        for i in range(len(N)):
            if N[q[0]][i] == 1 and vis.count(i) != 1 and q.count(i) == 0:  # вместо "and" программист написал "or"
                q.append(i)
                if i == b:
                    INFUNCTION_RES_PATH.append(q[0])
                    traversal(N, a, q[0], INFUNCTION_RES_PATH)
                    return INFUNCTION_RES_PATH
        q.reverse()
        deleted = q.pop()
        q.reverse()
        vis.append(deleted)
    return False


def matrix_checker(N):
    for i in range(len(N)):
        for j in range(len(N)):
            if N[i][j] != 1 and N[i][j] != 0:
                raise ValueError
    height = len(N[0])
    width = len(N)
    if height != width:
        raise DimensionException


def traversal_wrapper(N, a, b): # перепутаны начальный узел и конечный узел
    matrix_checker(N)
    res_path = []
    res_path = traversal(N, a, b, res_path)
    if res_path is False:
        return False
    res_path.reverse()
    res_path.append(b)
    return res_path


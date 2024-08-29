FIBONACCI = {}


def fibonacci3(n):
    if n in FIBONACCI:
        return FIBONACCI[n]
    tmp = None
    match n:
        case 0: tmp = 1
        case 1: tmp = 2
        case 2: tmp = 4
        case _: tmp = fibonacci3(n-1)+fibonacci3(n-2)+fibonacci3(n-3)
    FIBONACCI[n] = tmp
    return tmp


for i in range(100):
    print(i, end="\t")
    print(fibonacci3(i))

from os import listdir

def route_list():
    lst = listdir("App/routes")
    lst2= []
    for i in lst:
        x = i.replace('.py','')
        lst2.append(x)
    return (lst2)


__all__ = route_list()
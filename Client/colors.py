from random import randint
"""this made by kfir-rabinovitch-levi and can't be used by anyone else without his permission"""

def intofoas_ps(color,data, end='\n'):
    if colors.off:
        print(*data, end=end)
        return
        
    print(color, end='')
    if len(data) >= 1:
        print(data[0], end='')
        if len(data) > 1:
            for d in data[1:]:
                print("",d, end='')
    print(end=end)
    print("\033[00m", flush=True, end='')

class colors:
    off = False
    def Red(*data, end='\n'):
        intofoas_ps("\033[91m",data, end)

    def Green(*data, end='\n'):
        intofoas_ps("\033[92m",data, end)

    def Yellow(*data, end='\n'):
        intofoas_ps("\033[93m",data, end)
        
    def LightPurple(*data, end='\n'):
        intofoas_ps("\033[94m",data, end)

    def Purple(*data, end='\n'):
        intofoas_ps("\033[95m",data, end)

    def Cyan(*data, end='\n'):
        intofoas_ps("\033[96m",data, end)

    def LightGray(*data, end='\n'):
        intofoas_ps("\033[97m",data, end)

    def Black(*data, end='\n'):
        intofoas_ps("\033[98m",data, end)
    
    def Clear(*data, end='\n'):
        intofoas_ps("\033[00m",data, end)
    options = [Black, Cyan, Green, LightGray, LightPurple, Purple, Red, Yellow]
    count = len(options)

    def random(*data, end='\n'):
        colors.options[randint(0,colors.count-1)](*data, end='')

t = int(input())

for i in range(1 , t + 1) :
    
    x , y = map(int , input().split()) 
    
    if x == y :
        
        if x % 2 == 0 :
            
            time = x * 2
            
        else :
            
            time = x * 2 - 1
            
    elif y == x - 2 :
        
        if x % 2 == 0 :
            
            time = x + y
            
        else :
            
            time = x + y - 1
            
    else :
        
        time = -1
            
    print(time)

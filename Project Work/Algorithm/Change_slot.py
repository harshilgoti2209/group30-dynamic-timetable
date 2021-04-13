def change_slot(cube,genes,slots) : 
    for i in slots.keys() : 
        print(i)

    slot = input("Select subject that you want to change : ")
    c=0
    while(c==0) : 
        if(slot in slots.keys()) : 
            c=1
        else : 
            print("Selected subject is not available please enter again !")
            slot = input("Select Slot that you want to change : ")
    
    temp = []
    print("Input subject is in slots : ")
    for ii in range(cube.shape[1]) : 
        for jj in range(cube.shape[2]) : 
            for kk in range(cube.shape[0]) :
                if(cube[kk,ii,jj] != -1) : 
                    if(genes[cube[kk,ii,jj]].subject_id == slot) : 
                        temp.append([kk,ii,jj])
                        print([kk,ii,jj])
    
    inp = input("Enter old slot : ").split(',')
    kk=int(inp[0])
    ii=int(inp[1])
    jj=int(inp[2])

    c=0
    while(c==0) : 
        if([kk,ii,jj] in temp) : 
            c=1
        else : 
            print("Selected old slot is not available please enter again !")
            inp = input("Input old slot : ").split(',')
            kk=int(inp[0])
            ii=int(inp[1])
            jj=int(inp[2])

    print("Available slot for selected subject is : ")
    for i in slots[slot] : 
        print(i)

    inp = input("Input new slot : ").split(',')
    i=int(inp[0])
    j=int(inp[1])

    c=0
    while(c==0) : 
        if([i,j] in slots[slot]) : 
            c=1
        else : 
            print("Selected new slot is not available please enter again !")
            inp = input("Input new slot : ").split(',')
            i=int(inp[0])
            j=int(inp[1])

    for k in range(cube.shape[0]) : 
        if(cube[k,i,j] == -1) : 
            cube[k,i,j] = cube[kk,ii,jj]
            cube[kk,ii,jj] = -1

    return cube
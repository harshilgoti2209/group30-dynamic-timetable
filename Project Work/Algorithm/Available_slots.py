def available_slots(genes, cube) : 
    slots = {}
    a=0
    for i in range(len(genes)) : 
        if(genes[i].subject_id in slots.keys()) : 
            a=a+1
        else : 
            slots[genes[i].subject_id] = []
            for ii in range(cube.shape[1]) : 
                for jj in range(cube.shape[2]) : 
                    c=0
                    t=0
                    for kk in range(cube.shape[0]) : 
                        if(cube[kk,ii,jj] != -1) : 
                            t=t+1
                            if(genes[cube[kk,ii,jj]].prof_id != genes[i].prof_id) : 
                                c=c+1
                            if(genes[cube[kk,ii,jj]].batch_id != genes[i].batch_id) : 
                                c=c+1
                    if((2*t) == c) : 
                        slots[genes[i].subject_id].append([ii,jj])

    return slots
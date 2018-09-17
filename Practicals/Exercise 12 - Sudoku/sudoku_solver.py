def sudoku_solver(sudoku):
    changes = True
    while changes:
        changes = False
        for i in range(9):
            #print("i=",i)
            for j in range(9):
                #print ("j=",j)
                if n[i,j]==0:
                    cand = np.arange(1,10,dtype='int').tolist() 
                    for k in range(0,9):
                        if n[k,j]==0: continue
                        try:
                            cand.remove(n[k,j])
                        except ValueError:
                            continue
                    for k in range(0,9):
                        if n[i,k]==0: continue
                        try:
                            cand.remove(n[i,k])
                        except ValueError:
                            continue
                    i3 = 3*int(i/3)
                    j3 = 3*int(j/3)
                    print(i3,j3)
                    for k in range(i3,i3+3):
                        for l in range(j3,j3+3):
                            if n[k,l]==0: continue
                            try:
                                cand.remove(n[k,l])
                            except ValueError:
                                continue
                    if len(cand)==1: 
                        n [i,j] = cand[0]
                        changes = True
    return sudoku

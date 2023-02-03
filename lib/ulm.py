import random

######## INIZIO FUNZIONI DI COSTRUZIONE ########

def costruisci_matrice(n_righe,n_colonne,valore):
    ret = []
    for i in range(n_righe):
        riga = [valore] * n_colonne
        ret.append(riga)
    return ret

def costruisci_matrice_nulla(n_righe,n_colonne):
    return costruisci_matrice(n_righe,n_colonne,0)

def costruisci_matrice_quadrata(ordine,valore):
    return costruisci_matrice(ordine,ordine,valore)

def costruisci_matrice_valori_casuali(n_righe,n_colonne,valore):
    risultato = costruisci_matrice_nulla(n_righe,n_colonne)
    for i in range(n_righe):
        for j in range(n_colonne):
            risultato[i][j] = random.randint(0,valore)
    return risultato

def costruisci_matrice_identita(ordine):
    risultato = costruisci_matrice_quadrata(ordine,0)
    for i in range(len(risultato)):
        risultato[i][i] = 1
    return risultato

######## FINE FUNZIONI DI COSTRUZIONE ########

######## INIZIO FUNZIONI DI CALCOLO ########

def somma_riga(M,i):
    return sum(M[i])

def somma_colonna(M,j):
    s = 0
    for riga in M:
        s = s + riga[j]
    return s

def somma_vettori(vettore_1,vettore_2):
    n = len(vettore_1)
    risultato = [0] * n
    for i in range(n):
        risultato[i] = vettore_1[i] + vettore_2[i]
    return risultato

def prodotto_vettore_scalare(vettore,scalare):
    n = len(vettore)
    risultato = [0] * n
    for i in range(n):
        risultato[i] = vettore[i] * scalare
    return risultato

def prodotto_scalare(vettore_1,vettore_2):
    n = len(vettore_1)
    risultato = 0
    for i in range(n):
        risultato += vettore_1[i] * vettore_2[i]
    return risultato

def prodotto_matrice_scalare(matrice,scalare):
    nr = len(matrice)
    nc = len(matrice[0])
    risultato = costruisci_matrice_nulla(nr,nc)
    for i in range(nr):
        for j in range(nc):
            risultato[i][j] = matrice[i][j] * scalare
    return risultato

def prodotto_matrice_vettore(matrice,vettore):
    nr = len(matrice)
    risultato = [0] * nr
    for i in range(nr):
        risultato[i] = prodotto_scalare(matrice[i],vettore)
    return risultato

def prodotto_matrici(A,B):
    nr_A = len(A)
    nc_B = len(B[0])
    risultato = costruisci_matrice_nulla(nr_A,nc_B)
    for i in range(nr_A):
        for j in range(nc_B):
            riga_A = A[i]
            colonna_B = copia_colonna(B,j)
            risultato[i][j] = prodotto_scalare(riga_A,colonna_B)
    return risultato
    
def trasposta(matrice):
    nr = len(matrice)
    nc = len(matrice[0])
    risultato = costruisci_matrice_nulla(nc,nr)
    for i in range(nr):
        for j in range(nc):
            risultato[j][i] = matrice[i][j]
    return risultato
    
######## FINE FUNZIONI DI CALCOLO ########

######## INIZIO FUNZIONI DI COPIA E MODIFICA ########

def elimina_riga(M,i):
    del M[i]

def elimina_colonna(M,j):
    for riga in M:
        del riga[j]

def copia_riga(matrice,i):
    return matrice[i][:]

def copia_colonna(matrice,j):
    risultato = []
    for riga in matrice:
        risultato.append(riga[j])
    return risultato
    
def scambia_righe(matrice,i1,i2):
    t = matrice[i1]
    matrice[i1] = matrice[i2]
    matrice[i2] = t

def scambia_colonne(matrice,j1,j2):
    for riga in matrice:
        t = riga[j1]
        riga[j1] = riga[j2]
        riga[j2] = t

def copia_matrice(matrice):
    risultato = []
    for riga in matrice:
        risultato.append(riga[:])
    return risultato
    
######## FINE FUNZIONI DI COPIA E MODIFICA ########

######## INIZIO FUNZIONI DI VERIFICA ########

def e_quadrata(matrice):
    return len(matrice) == len(matrice[0])

def e_nulla(matrice):
    n_righe = len(matrice)
    n_colonne = len(matrice[0])
    for i in range(n_righe):
        for j in range(n_colonne):
            if matrice[i][j] != 0:
                return False
    return True
    
def e_diagonale(matrice):
    if not e_quadrata(matrice):
        return False
    ordine = len(matrice)
    for i in range(ordine):
        for j in range(ordine):
            if matrice[i][j] != 0 and i != j:
                return False
    return True

def e_scalare(matrice):
    if not e_diagonale(matrice):
        return False
    ordine = len(matrice)
    for i in range(ordine - 1):
        if matrice[i][i] != matrice[i + 1][i + 1]:
            return False
    return True

def e_identita(matrice):
    return e_scalare(matrice) and matrice[0][0] == 1

def matrici_uguali(matrice_1,matrice_2):
    nr_1 = len(matrice_1)
    nc_1 = len(matrice_1[0])
    nr_2 = len(matrice_2)
    nc_2 = len(matrice_2[0])
    if nr_1 != nr_2 or nc_1 != nc_2:
        return False
    for i in range(nr_1):
        for j in range(nc_1):
            if matrice_1[i][j] != matrice_2[i][j]:
                return False
    return True

def e_simmetrica(matrice):
    if not e_quadrata(matrice):
        return False
    ordine = len(matrice)
    for i in range(ordine - 1):
        for j in range(i + 1, ordine):
            if matrice[i][j] != matrice[j][i]:
                return False
    return True

######## FINE FUNZIONI DI VERIFICA ########

######## INIZIO FUNZIONI DI INPUT-OUTPUT ########

def leggi_lista_int_lunghezza(n):
    ret = []
    for i in range(n):
        v = int(input("Inserisci l'elemento di indice "+str(i)+":"))
        ret.append(v)
    return ret

def leggi_lista_int():
    n = int(input('Lunghezza:'))
    return leggi_lista_int_lunghezza(n)

def leggi_lista_float_lunghezza(n):
    ret = []
    for i in range(n):
        v = float(input("Inserisci l'elemento di indice "+str(i)+":"))
        ret.append(v)
    return ret

def leggi_lista_float():
    n = int(input('Lunghezza:'))
    return leggi_lista_float_lunghezza(n)

def leggi_matrice_int_dimensioni(nr,nc):
    matrice = []
    for i in range(nr):
        print('-- Riga '+str(i)+' --')
        riga = leggi_lista_int_lunghezza(nc)
        matrice.append(riga)
    return matrice

def leggi_matrice_int():
    r = int(input('Numero righe = '))
    c = int(input('Numero colonne = '))
    return leggi_matrice_int_dimensioni(r,c)

def leggi_matrice_float_dimensioni(nr,nc):
    matrice = []
    for i in range(nr):
        print('-- Riga '+str(i)+' --')
        riga = leggi_lista_float_lunghezza(nc)
        matrice.append(riga)
    return matrice

def leggi_matrice_float():
    r = int(input('Numero righe = '))
    c = int(input('Numero colonne = '))
    return leggi_matrice_float_dimensioni(r,c)

def stampa_matrice(m):
    for riga in m:
        print(riga)

def stampa_matrice_incolonnata(matrice,n_cifre):
    for riga in matrice:
        for elemento in riga:
            print(str(elemento).rjust(n_cifre+1), end='')
        print()

def scrivi_lista_su_file(lista,nome_file):
    f = open(nome_file,'w')
    f.write(str(lista[0]))
    for n in lista[1:]:
        f.write(','+str(n))
    f.close()

def leggi_lista_interi_da_file(nome_file):
    f = open(nome_file,'r')
    risultato = []
    linea = f.readline()
    valori = linea.split(',')
    for x in valori:
        risultato.append(int(x))
    f.close()
    return risultato

def scrivi_matrice_su_file(matrice,nome_file):
    f = open(nome_file,'w')
    for riga in matrice:
        f.write(str(riga[0]))
        for n in riga[1:]:
            f.write(','+str(n))
        f.write('\n')
    f.close()

def leggi_matrice_interi_da_file(nome_file):
    risultato = []
    f = open(nome_file,'r')
    for linea in f:
        riga = []
        valori = linea.split(',')
        for x in valori:
            riga.append(int(x))
        risultato.append(riga)
    f.close()
    return risultato

######## FINE FUNZIONI DI INPUT-OUTPUT ########

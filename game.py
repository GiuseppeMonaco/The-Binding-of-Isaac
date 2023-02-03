import lib.ulm as ulm
import random
import pygame
import json
from datetime import timedelta

# JSON
def carica_dati():
    f = open('data/save.json','r')
    dati = json.load(f)
    f.close()
    return dati

def salva_dati(chiave, valore):
    dati = carica_dati()
    dati[chiave]  = valore
    f = open('data/save.json','w')
    json.dump(dati,f)
    f.close()

risoluzioni = {
    'HD': (1280,720)
}

# POSSIBILI POSIZIONI NEMICI
posizioni_stanza = [
    (230,150),(1050,150),
    (560,280),(640,280),(720,280),
    (560,360),(640,360),(720,360),
    (560,440),(640,440),(720,440),
    (230,550),(1050,550)
]

# POSSIBILI PATTERN DI SPAWN DEI NEMICI
pattern_nemici = [
    [posizioni_stanza[0],posizioni_stanza[1],posizioni_stanza[11],posizioni_stanza[12]],
    [posizioni_stanza[0],posizioni_stanza[1],posizioni_stanza[6],posizioni_stanza[11],posizioni_stanza[12]],
    [posizioni_stanza[3],posizioni_stanza[5],posizioni_stanza[7],posizioni_stanza[9]],
    [posizioni_stanza[2],posizioni_stanza[4],posizioni_stanza[8],posizioni_stanza[10]],
    [posizioni_stanza[6]],
    [posizioni_stanza[5],posizioni_stanza[7]],
    [posizioni_stanza[3],posizioni_stanza[9]],
    [posizioni_stanza[0],posizioni_stanza[1],posizioni_stanza[5],posizioni_stanza[7],posizioni_stanza[11],posizioni_stanza[12]],
    [posizioni_stanza[0],posizioni_stanza[4],posizioni_stanza[8],posizioni_stanza[12]],
    [posizioni_stanza[1],posizioni_stanza[2],posizioni_stanza[10],posizioni_stanza[11]]
]

# POSSIBILI POSIZIONI ROCCE
posizioni_stanza_rocce = [
    (380,200),(900,200),
    (280,260),(1000,260),
    (500,220),(640,220),(780,220),
    (500,360),(780,360),
    (500,500),(640,500),(780,500),
    (280,460),(1000,460),
    (380,520),(900,520)
]

# POSSIBILI PATTERN DI SPAWN DELLE ROCCE
pattern_rocce = [
    [posizioni_stanza_rocce[0],posizioni_stanza_rocce[1],posizioni_stanza_rocce[2],posizioni_stanza_rocce[3],posizioni_stanza_rocce[12],posizioni_stanza_rocce[13],posizioni_stanza_rocce[14],posizioni_stanza_rocce[15]],
    [posizioni_stanza_rocce[4],posizioni_stanza_rocce[6],posizioni_stanza_rocce[9],posizioni_stanza_rocce[11]],
    [posizioni_stanza_rocce[5],posizioni_stanza_rocce[7],posizioni_stanza_rocce[8],posizioni_stanza_rocce[10]],
    [posizioni_stanza_rocce[0],posizioni_stanza_rocce[1],posizioni_stanza_rocce[5],posizioni_stanza_rocce[10],posizioni_stanza_rocce[14],posizioni_stanza_rocce[15]],
    [posizioni_stanza_rocce[2],posizioni_stanza_rocce[3],posizioni_stanza_rocce[7],posizioni_stanza_rocce[8],posizioni_stanza_rocce[12],posizioni_stanza_rocce[13]]
]

# Funzione per generare la mappa di gioco, dove lo 0 rappresenta stanze vuote, mentre 1 le stanze esistenti
def genera_mappa(dimensione_matrice,stanze_totali):
    map = ulm.costruisci_matrice_quadrata(dimensione_matrice,0)
    map[dimensione_matrice//2][dimensione_matrice//2] = 1

    n_stanze = 1
    while n_stanze < stanze_totali:
        stanze_da_scegliere = []
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] == 1:
                    for stanza in info_stanza(map,i,j)['vuoti_adiacenti']:
                        if info_stanza(map,stanza[0],stanza[1])['n_stanze_adiacenti'] == 1:
                            if stanza not in stanze_da_scegliere:
                                stanze_da_scegliere.append(stanza)
        scelta = random.choice(stanze_da_scegliere)
        map[scelta[0]][scelta[1]] = 1
        n_stanze += 1
    crea_stanza_finale(map)
    return map

# Funzione che sceglie una stanza finale più lontana possibile dalla stanza centrale, rappresentata nella matrice da un 2
def crea_stanza_finale(map):
    stanza_finale_i = 0
    stanza_finale_j = 0
    distanza_finale = 0
    for i in range(len(map)):
        for j in range(len(map[0])):
            distanza_dal_centro = abs(len(map)//2 - i) + abs(len(map[0])//2 - j)
            if map[i][j] == 1 and distanza_dal_centro > distanza_finale:
                stanza_finale_i = i
                stanza_finale_j = j
                distanza_finale = distanza_dal_centro
    map[stanza_finale_i][stanza_finale_j] = 2
            

# Restituisce un dizionario con le informazioni di una stanza
def info_stanza(m,i,j):
    indice_max = len(m) - 1
    ret = {
        'stanze_adiacenti':[],
        'n_stanze_adiacenti':0,
        'vuoti_adiacenti':[]
    }

    if i < indice_max:
        if m[i+1][j]:
            ret['stanze_adiacenti'].append([i+1,j])
        else:
            ret['vuoti_adiacenti'].append([i+1,j])
    if j < indice_max:
        if m[i][j+1]:
            ret['stanze_adiacenti'].append([i,j+1])
        else:
            ret['vuoti_adiacenti'].append([i,j+1])
    if i > 0:
        if m[i-1][j]:
            ret['stanze_adiacenti'].append([i-1,j])
        else:
            ret['vuoti_adiacenti'].append([i-1,j])
    if j > 0:
        if m[i][j-1]:
            ret['stanze_adiacenti'].append([i,j-1])
        else:
            ret['vuoti_adiacenti'].append([i,j-1])
    ret['n_stanze_adiacenti'] = len(ret['stanze_adiacenti'])
    return ret

# Funzione di debug che stampa in console l'anteprima della mappa
def map_preview(m):
    ret = ulm.copia_matrice(m)
    for i in range(len(ret)):
        for j in range(len(ret[0])):
            if ret[i][j] == 0:
                ret[i][j] = '⬛'
            elif ret[i][j] == 1 and i == len(m)//2 and j == len(m)//2:
                ret[i][j] = '🟩'
            elif ret[i][j] == 2:
                ret[i][j] = '🟥'
            else:
                ret[i][j] = '⬜'
    ulm.stampa_matrice_incolonnata(ret,1)

# Restituisce un dizionario di booleani che rappresentano la direzione delle stanze adiacenti
def porte_stanza(map,i,j):
    coordinate_stanze_adiacenti = info_stanza(map,i,j)['stanze_adiacenti']
    ret = {
        'up': False,
        'down': False,
        'right': False,
        'left': False
    }
    if [i-1,j] in coordinate_stanze_adiacenti:
        ret['up'] = True
    if [i+1,j] in coordinate_stanze_adiacenti:
        ret['down'] = True
    if [i,j+1] in coordinate_stanze_adiacenti:
        ret['right'] = True
    if [i,j-1] in coordinate_stanze_adiacenti:
        ret['left'] = True
    return ret

# Funzione che restituisce un'immagine utilizzando la libreria pygame
def carica_immagine(percorso, scala = (1,1)):
    scala_x,scala_y = scala
    image = pygame.image.load(percorso)
    dim_x,dim_y = image.get_size()
    image = pygame.transform.scale(image, (dim_x*scala_x,dim_y*scala_y))
    return image.convert_alpha()

# Funzione che restituisce un testo
def crea_testo(testo,dimensione,colore):
    return pygame.font.Font('res/font/Pixeltype.ttf', dimensione).render(testo,False,colore)

# Funzione che restituisce l'opportuno frame di animazione del player
def player_animation(player_data, player_frames, velocita_animazione,comandi,metti_pausa):
    current = player_frames['current_frame'][0]
    current_counter = player_frames['current_frame'][1]
    player_acc = player_data['player_acc']
    in_movimento = player_acc['W'] + player_acc['S'] + player_acc['A'] + player_acc['D'] != 0
    cambia_frame = current_counter == velocita_animazione

    if player_data['vita'][1] > 0 and player_data['vita'][1] % 15 in (14,13,12,11,10,9):
        return 'res/img/player/player_blank.png'

    if metti_pausa:
        return player_frames['down'][0]
    if not in_movimento:
        player_frames['current_frame'] = [0,0]
        if comandi['LEFT']:
            return player_frames['sx'][0]
        elif comandi['RIGHT']:
            return player_frames['dx'][0]
        elif comandi['DOWN']:
            return player_frames['down'][0]
        elif comandi['UP']:
            return player_frames['up'][0]
        else:
            return player_frames['down'][0]
    
    player_frames['current_frame'][1] += 1

    if cambia_frame:
        player_frames['current_frame'][1] = 0
        if current == 0:
            player_frames['current_frame'][0] = 1
        elif current == 1:
            player_frames['current_frame'][0] = 2
        elif current == 2:
            player_frames['current_frame'][0] = 3
        elif current == 3:
            player_frames['current_frame'][0] = 0

    if comandi['LEFT']:
        return player_frames['sx'][current]
    elif comandi['RIGHT']:
        return player_frames['dx'][current]
    elif comandi['DOWN']:
        return player_frames['down'][current]
    elif comandi['UP']:
        return player_frames['up'][current]

    if player_acc['W']*3 > player_acc['S']+player_acc['A']+player_acc['D']:
        return player_frames['up'][current]
    elif player_acc['S']*3 > player_acc['W'] + player_acc['A'] + player_acc['D']:
        return player_frames['down'][current]
    elif player_acc['A']*3 > player_acc['W'] + player_acc['S'] + player_acc['D']:
        return player_frames['sx'][current]
    elif player_acc['D']*3 > player_acc['W'] + player_acc['A'] + player_acc['S']:
        return player_frames['dx'][current]

# Funzione che restituisce l'opportuno frame di animazione del nemico
def nemico1_animation(nemico, player_pos, nemico1_frames, velocita_animazione, metti_pausa, variante):
    current = nemico['frame_animazione'][0]
    current_counter = nemico['frame_animazione'][1]
    direzione = direzione_nemico(nemico['pos'],player_pos)
    cambia_frame = current_counter == velocita_animazione
    red_timer = nemico['frame_animazione'][2]

    if red_timer == -1:
        if variante == 0:
            red = '.png'
        if variante == 1:
            red = '_elite.png'
    else:
        red = '_red.png'

    if not direzione or metti_pausa:
        nemico['frame_animazione'][0] = 0
        nemico['frame_animazione'][1] = 0
        return nemico1_frames['down'][0] + red
    
    nemico['frame_animazione'][1] += 1

    if cambia_frame:
        nemico['frame_animazione'][1] = 0
        if current == 0:
            nemico['frame_animazione'][0] = 1
        elif current == 1:
            nemico['frame_animazione'][0] = 2
        elif current == 2:
            nemico['frame_animazione'][0] = 3
        elif current == 3:
            nemico['frame_animazione'][0] = 0

    if direzione == 'up':
        return nemico1_frames['up'][current] + red
    if direzione == 'down':
        return nemico1_frames['down'][current] + red
    if direzione == 'sx':
        return nemico1_frames['sx'][current] + red
    if direzione == 'dx':
        return nemico1_frames['dx'][current] + red

# Funzione che restituisce la direzione verso la quale il nemico deve guardare
def direzione_nemico(nemico_pos,player_pos):
    dx = player_pos[0] - nemico_pos[0]
    dy = player_pos[1] - nemico_pos[1]
    vettore_direzione = pygame.math.Vector2(dx,dy)
    vettore_direzione.normalize()
    x = vettore_direzione[0]
    y = vettore_direzione[1]
    if abs(x) < y:
        return 'up'
    elif abs(x) < -y:
        return 'down'
    elif abs(y) < x:
        return 'dx'
    elif abs(y) < -x:
        return 'sx'
    elif y == 0 and x == 0:
        return False

# Funzione che restituisce una lista contenente i nemici da inserire in una stanza
def genera_nemici(vita,freeze_countdown, lista_posizioni):
    ret = []
    if not lista_posizioni:
        lista_posizioni = random.choice(pattern_nemici)
    for posizione in lista_posizioni:
        ret.append({'pos': list(posizione), 'rect': None, 'vita': vita, 'freeze_countdown':freeze_countdown, 'frame_animazione':[0,0,-1]})
    return ret

def genera_rocce(lista_posizioni):
    ret = []
    if not lista_posizioni:
        lista_posizioni = random.choice(pattern_rocce)
    for posizione in lista_posizioni:
        png = random.choice([
            'res/img/roccia_0.png',
            'res/img/roccia_1.png',
            'res/img/roccia_2.png'
        ])
        image = carica_immagine(png,(2.7,2.7))
        rect = image.get_rect(center=posizione)
        ret.append({'pos':posizione, 'rect':rect, 'image':image})
    return ret

# Funzione che restituisce un dizionario con le informazioni di una stanza, compresi i nemici
def informazioni_stanze(map):
    ret = {}
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] != 0:
                ret[(i,j)] = {}
                ret[(i,j)]['porte'] = porte_stanza(map,i,j)
                if i == len(map)//2 and j == len(map[0])//2:
                    ret[(i,j)]['nemici'] = []
                    ret[(i,j)]['rocce'] = []
                elif map[i][j] == 1:
                    ret[(i,j)]['nemici'] = genera_nemici(5,30,False)
                    ret[(i,j)]['rocce'] = genera_rocce(False)
                elif map[i][j] == 2:
                    ret[(i,j)]['nemici'] = genera_nemici(15,30,[posizioni_stanza[3],posizioni_stanza[5],posizioni_stanza[7],posizioni_stanza[9]])
                    ret[(i,j)]['rocce'] = []
    return ret

# Funzione che fa muovere i nemici verso il player
def cammina(nemico, destinazione, lista_nemici, lista_rocce, velocita):
    dx = destinazione[0] - nemico['pos'][0]
    dy = destinazione[1] - nemico['pos'][1]
    vettore_direzione = pygame.math.Vector2(dx,dy)
    vettore_direzione.normalize()
    if vettore_direzione.length() > 30:
        vettore_direzione.scale_to_length(velocita)
        nemico['pos'][0] += vettore_direzione[0]
        nemico['pos'][1] += vettore_direzione[1]

    for altro_nemico in lista_nemici:
        if altro_nemico != nemico:
            dx = nemico['pos'][0] - altro_nemico['pos'][0]
            dy = nemico['pos'][1] - altro_nemico['pos'][1]
            vettore_direzione = pygame.math.Vector2(dx,dy)
            vettore_direzione.normalize()
            if vettore_direzione.length() < 60:
                nemico['pos'][0] += vettore_direzione[0] * 0.015
                nemico['pos'][1] += vettore_direzione[1] * 0.015
    
    for roccia in lista_rocce:
        dx = nemico['pos'][0] - roccia['pos'][0]
        dy = nemico['pos'][1] - roccia['pos'][1]
        vettore_direzione = pygame.math.Vector2(dx,dy)
        vettore_direzione.normalize()
        if vettore_direzione.length() < 60:
            nemico['pos'][0] += vettore_direzione[0] * 0.045
            nemico['pos'][1] += vettore_direzione[1] * 0.045

# Funzione che restituisce l'opportuno frame di animazione delle porte
def animazione_porta(lato, lista_nemici, porte_frames, velocita_animazione, sound_door_close, sound_door_open):
    current = porte_frames['current_frame'][0]
    current_counter = porte_frames['current_frame'][1]
    cambia_frame = current_counter == velocita_animazione
    porte_frames['current_frame'][1] += 1
    
    if cambia_frame:
        porte_frames['current_frame'][1] = 0
        
        if lista_nemici == []:
            if current > 0:
                porte_frames['current_frame'][0] -= 1
            if current == 1:
                sound_door_open.play()
        else:
            if current < 2:
                porte_frames['current_frame'][0] += 1
            if current == 0:
                sound_door_close.play()
    
    if lato == 'up':
        return porte_frames['up'][current]
    if lato == 'down':
        return porte_frames['down'][current]
    if lato == 'left':
        return porte_frames['sx'][current]
    if lato == 'right':
        return porte_frames['dx'][current]     

# Funzione che restituisce l'opportuno frame di animazione della botola finale
def animazione_botola(botola_frames, lista_nemici, velocita_animazione):
    current = botola_frames['current_frame'][0]
    current_counter = botola_frames['current_frame'][1]
    cambia_frame = current_counter == velocita_animazione
    botola_frames['current_frame'][1] += 1
    
    if cambia_frame:
        botola_frames['current_frame'][1] = 0
        
        if lista_nemici == []:
            if current < 8:
                botola_frames['current_frame'][0] += 1

    return botola_frames['frames'][current]

# Funzione che genera i proiettili sparati dal player
def genera_proiettile(direzione,lista_proiettili,pos_player):
    posizione = pos_player.copy()
    proiettile = {'pos': posizione, 'rect': None, 'direzione': direzione, 'frame_animazione':[0,0], 'impact': False}
    lista_proiettili.append(proiettile)

# Funzione che fa muovere i proiettili
def spostamento_proiettile(proiettile, velocita):
    if not proiettile['impact']:
        if proiettile['direzione'] == 'UP':
            proiettile['pos'][1] -= velocita
        elif proiettile['direzione'] == 'LEFT':
            proiettile['pos'][0] -= velocita
        elif proiettile['direzione'] == 'DOWN':
            proiettile['pos'][1] += velocita
        elif proiettile['direzione'] == 'RIGHT':
            proiettile['pos'][0] += velocita

# Funzione che restituisce l'opportuno frame di animazione di un proiettile
def proiettile_animation(proiettile, proiettile_frames, velocita_animazione):
    current_frame = proiettile['frame_animazione'][0]
    current_counter = proiettile['frame_animazione'][1]
    cambia_frame = current_counter == velocita_animazione
    
    if proiettile['impact']:
        proiettile['frame_animazione'][1] += 1

    if cambia_frame:
        proiettile['frame_animazione'][1] = 0
        if current_frame < 6:
            proiettile['frame_animazione'][0] += 1

    if current_frame < 6:
        return proiettile_frames[current_frame]
    else:
        return proiettile_frames[0]

# Funzione che manda indietro un nemico quando viene colpito
def respingi_nemico(direzione_proiettile, pos_nemico, forza):
    if direzione_proiettile == 'UP':
        pos_nemico[1] -= forza
    elif direzione_proiettile == 'LEFT':
        pos_nemico[0] -= forza
    elif direzione_proiettile == 'DOWN':
        pos_nemico[1] += forza
    elif direzione_proiettile == 'RIGHT':
        pos_nemico[0] += forza

# Funzione che sceglie un suono casuale da una tupla di suoni
def riproduci_suono_random(tupla_suoni):
    suono = random.choice(tupla_suoni)
    suono.play()

# Funzione principale che viene avviata all'avvio del gioco
def game(map,n_stanze):
    global moltiplicatore_audio

    risoluzione = risoluzioni['HD']
    res_x, res_y = risoluzione
    schermo = pygame.display.set_mode(risoluzione)
    clock = pygame.time.Clock()
    pygame.display.set_caption('The Binding of Isaac')

    # GENERAZIONE MAPPA
    info_stanze = informazioni_stanze(map)

    # DATI
    dati_salvataggio = carica_dati()
    
    is_pausa = False
    is_inizio = True
    is_game_over = False
    is_vittoria = False
    riproduci_sound_menu_appear = True
    assegna_punteggio_finale = True
    tempo = 0
    punteggio = 0

    # STANZA
    stanza_background = carica_immagine('res/img/stanza.jpeg')
    stanza_inizio_background = carica_immagine('res/img/stanza_inizio.jpeg')
    
    wall_sup = pygame.Surface((res_x,res_y-700))
    wall_inf = pygame.Surface((res_x,res_y-700))
    wall_dx = pygame.Surface((res_x-700,res_y))
    wall_sx = pygame.Surface((res_x-700,res_y))

    wall_sup = pygame.Surface((res_x,res_y-660))
    wall_inf = pygame.Surface((res_x,res_y-600))
    wall_dx = pygame.Surface((res_x-1110,res_y))
    wall_sx = pygame.Surface((res_x-1110,res_y))

    wall_sup_rect = wall_sup.get_rect(midtop= (res_x//2,0))
    wall_inf_rect = wall_inf.get_rect(midbottom= (res_x//2,res_y))
    wall_dx_rect = wall_dx.get_rect(midright= (res_x,res_y//2))
    wall_sx_rect = wall_sx.get_rect(midleft= (0,res_y//2))

    # IMMAGINI
    pausa_pergamena = carica_immagine('res/img/pergamena.png',(2.5,2.5))
    pausa_pergamena_rect = pausa_pergamena.get_rect(center= (res_x//2,res_y//2))

    # TESTI
    pausa_title = crea_testo('PAUSA',100,'gray20')
    pausa_title_rect = pausa_title.get_rect(center= (res_x//2,res_y//2-150))
    
    inizio_title = crea_testo('THE BINDING OF ISAAC',70,'gray20')
    inizio_title_rect = inizio_title.get_rect(center= (res_x//2,res_y//2-150))

    record_title = crea_testo(f'Record: {dati_salvataggio["record"]}',70,'gray20')
    record_title_rect = record_title.get_rect(center= (res_x//2,res_y//2-50))

    game_over_title = crea_testo('GAME OVER', 100,'gray20')
    game_over_title_rect = game_over_title.get_rect(center= (res_x//2,res_y//2-150))
    
    vittoria_title = crea_testo('VITTORIA', 130,'gray20')
    vittoria_title_rect = vittoria_title.get_rect(center= (res_x//2,res_y//2-130))

    # AUDIO 
    moltiplicatore_audio = dati_salvataggio['volume']
    moltiplicatore_audio_perc = moltiplicatore_audio/10
    
    pygame.mixer.music.load('res/audio/main_soundtrack.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05*moltiplicatore_audio_perc)

    sound_nemico1_1 = pygame.mixer.Sound('res/audio/sound_nemico1_1.wav')
    sound_nemico1_2 = pygame.mixer.Sound('res/audio/sound_nemico1_2.wav')
    sound_tear_1 = pygame.mixer.Sound('res/audio/tear_1.wav')
    sound_tear_2 = pygame.mixer.Sound('res/audio/tear_2.wav')
    sound_tear_end = pygame.mixer.Sound('res/audio/tear_end.wav')
    sound_danno = pygame.mixer.Sound('res/audio/danno.wav')
    sound_door_close = pygame.mixer.Sound('res/audio/door_close.wav')
    sound_door_open = pygame.mixer.Sound('res/audio/door_open.wav')
    sound_menu_appear = pygame.mixer.Sound('res/audio/menu_appear.wav')
    sound_menu_hide = pygame.mixer.Sound('res/audio/menu_hide.wav')

    sound_nemico1_1.set_volume(0.035*moltiplicatore_audio_perc)
    sound_nemico1_2.set_volume(0.035*moltiplicatore_audio_perc)
    sound_tear_1.set_volume(0.07*moltiplicatore_audio_perc)
    sound_tear_2.set_volume(0.07*moltiplicatore_audio_perc)
    sound_tear_end.set_volume(0.07*moltiplicatore_audio_perc)
    sound_danno.set_volume(0.04*moltiplicatore_audio_perc)
    sound_door_close.set_volume(0.05*moltiplicatore_audio_perc)
    sound_door_open.set_volume(0.05*moltiplicatore_audio_perc)
    sound_menu_appear.set_volume(0.2*moltiplicatore_audio_perc)
    sound_menu_hide.set_volume(0.2*moltiplicatore_audio_perc)

    # PULSANTI
    start_button_inizio_color = 'gray40'
    riprendi_button_pausa_color = 'gray40'
    ricomincia_button_color = 'gray40'
    exit_button_color = 'gray40'
    volume_up_button_color = 'gray40'
    volume_down_button_color = 'gray40'

    # PLAYER
    proiettili_timer = 40
    player_data = {
        'pos': [res_x//2,res_y//2],
        'velocita': 4,
        'player_acc': {'W': 0,'A': 0,'S': 0,'D': 0},
        'vita': [3,0],
        'stanza': [len(map)//2,len(map)//2],
        'timer_stanza': 0,
        'proiettili': {'timer': proiettili_timer, 'lista':[]}
    }
    
    player_frames = {
    'current_frame': [0,0],
    'down': [
        'res/img/player/player_down_0.png',
        'res/img/player/player_down_1.png',
        'res/img/player/player_down_0.png',
        'res/img/player/player_down_2.png'
    ],
    'dx': [
        'res/img/player/player_dx_0.png',
        'res/img/player/player_dx_1.png',
        'res/img/player/player_dx_0.png',
        'res/img/player/player_dx_2.png'
    ],
    'sx': [
        'res/img/player/player_sx_0.png',
        'res/img/player/player_sx_1.png',
        'res/img/player/player_sx_0.png',
        'res/img/player/player_sx_2.png'
    ],
    'up': [
        'res/img/player/player_up_0.png',
        'res/img/player/player_up_1.png',
        'res/img/player/player_up_0.png',
        'res/img/player/player_up_2.png'
    ]}

    # NEMICO 1
    nemico1_frames = {
    'down': [
        'res/img/nemico1/nemico1_down_0',
        'res/img/nemico1/nemico1_down_1',
        'res/img/nemico1/nemico1_down_0',
        'res/img/nemico1/nemico1_down_2'
    ],
    'dx': [
        'res/img/nemico1/nemico1_dx_0',
        'res/img/nemico1/nemico1_dx_1',
        'res/img/nemico1/nemico1_dx_0',
        'res/img/nemico1/nemico1_dx_2'
    ],
    'sx': [
        'res/img/nemico1/nemico1_sx_0',
        'res/img/nemico1/nemico1_sx_1',
        'res/img/nemico1/nemico1_sx_0',
        'res/img/nemico1/nemico1_sx_2'
    ],
    'up': [
        'res/img/nemico1/nemico1_up_0',
        'res/img/nemico1/nemico1_up_1',
        'res/img/nemico1/nemico1_up_0',
        'res/img/nemico1/nemico1_up_2'
    ]}

    # PROIETTILI
    proiettile_frames = [
        'res/img/tears/tear.png',
        'res/img/tears/tear_2.png',
        'res/img/tears/tear_3.png',
        'res/img/tears/tear_4.png',
        'res/img/tears/tear_5.png',
        'res/img/tears/tear_6.png',
    ]

    # PORTE
    porte_frames = {
    'current_frame': [0,0],
    'down': [
        'res/img/porte/porta_bottom.png',
        'res/img/porte/porta_bottom_2.png',
        'res/img/porte/porta_bottom_chiusa.png'
    ],
    'dx': [
        'res/img/porte/porta_right.png',
        'res/img/porte/porta_right_2.png',
        'res/img/porte/porta_right_chiusa.png'
    ],
    'sx': [
        'res/img/porte/porta_left.png',
        'res/img/porte/porta_left_2.png',
        'res/img/porte/porta_left_chiusa.png'
    ],
    'up': [
        'res/img/porte/porta_up.png',
        'res/img/porte/porta_up_2.png',
        'res/img/porte/porta_up_chiusa.png'
    ]}

    # BOTOLA
    botola_frames = {
        'current_frame': [0,0],
        'frames': [
            'res/img/botola/botola_0.png',
            'res/img/botola/botola_1.png',
            'res/img/botola/botola_0.png',
            'res/img/botola/botola_2.png',
            'res/img/botola/botola_5.png',
            'res/img/botola/botola_3.png',
            'res/img/botola/botola_5.png',
            'res/img/botola/botola_4.png',
            'res/img/botola/botola_5.png'
        ]}

    # VITE
    vite_frames = [
        'res/img/0_vite.png',
        'res/img/1_vite.png',
        'res/img/2_vite.png',
        'res/img/3_vite.png'
    ]

    # COMANDI
    comandi = {
        'W': False,
        'A': False,
        'S': False,
        'D': False,
        'UP': False,
        'LEFT': False,
        'DOWN': False,
        'RIGHT': False
    }

    # Ciclo principale per la gestione degli elementi dinamici
    while True:
        pos_mouse = pygame.mouse.get_pos()
        metti_pausa = is_inizio or is_pausa or is_game_over or is_vittoria

        # TESTI DINAMICI
        tempo_testo = crea_testo(f'Tempo: {timedelta(seconds= tempo//60)}',50,'gray80')
        tempo_testo_rect = tempo_testo.get_rect(topright=(res_x - 20,20))

        punteggio_testo = crea_testo(f'Punti: {punteggio}',50,'gray80')
        punteggio_testo_rect = punteggio_testo.get_rect(topleft=(20,20))

        volume_text = crea_testo(f'Volume: {moltiplicatore_audio * 10}%', 70,'gray20')
        volume_text_rect = volume_text.get_rect(center= (res_x//2,res_y//2+50))

        # PULSANTI
        start_button_inizio = crea_testo('Nuova Partita',70,start_button_inizio_color)
        start_button_inizio_rect = start_button_inizio.get_rect(center=(res_x//2,res_y//2+140))
        if start_button_inizio_rect.collidepoint(pos_mouse):
            start_button_inizio_color = 'gray20'
        else:
            start_button_inizio_color = 'gray40'
        
        riprendi_button_pausa = crea_testo('Riprendi',70,riprendi_button_pausa_color)
        riprendi_button_pausa_rect = riprendi_button_pausa.get_rect(center=(res_x//2,res_y//2+90))
        if riprendi_button_pausa_rect.collidepoint(pos_mouse):
            riprendi_button_pausa_color = 'gray20'
        else:
            riprendi_button_pausa_color = 'gray40'

        ricomincia_button = crea_testo('Ricomincia',70,ricomincia_button_color)
        ricomincia_button_rect = ricomincia_button.get_rect(center=(res_x//2,res_y//2+140))
        if ricomincia_button_rect.collidepoint(pos_mouse):
            ricomincia_button_color = 'tomato3'
        else:
            ricomincia_button_color = 'gray40'

        exit_button = crea_testo('Esci',70,exit_button_color)
        exit_button_rect = exit_button.get_rect(center=(res_x//2,res_y//2+190))
        if exit_button_rect.collidepoint(pos_mouse):
            exit_button_color = 'tomato3'
        else:
            exit_button_color = 'gray40'
        
        volume_up_button = crea_testo('+',80,volume_up_button_color)
        volume_up_button_rect = volume_up_button.get_rect(center=(res_x//2+160,res_y//2+45))
        if volume_up_button_rect.collidepoint(pos_mouse):
            volume_up_button_color = 'gray20'
        else:
            volume_up_button_color = 'gray40'
        
        volume_down_button = crea_testo('-',80,volume_down_button_color)
        volume_down_button_rect = volume_down_button.get_rect(center=(res_x//2-160,res_y//2+50))
        if volume_down_button_rect.collidepoint(pos_mouse):
            volume_down_button_color = 'gray20'
        else:
            volume_down_button_color = 'gray40'

        # SPRITE
        player = carica_immagine(player_animation(player_data,player_frames,10,comandi,metti_pausa),(2.5,2.5))
        player_rect = player.get_rect(center= player_data['pos'])

        vita_image = carica_immagine(vite_frames[player_data['vita'][0]], (3,3))
        vita_rect = vita_image.get_rect(midtop= (res_x//3.5, 15))

        # PORTE
        porta_sup = carica_immagine(animazione_porta('up',info_stanze[tuple(player_data['stanza'])]['nemici'], porte_frames, 50, sound_door_close, sound_door_open))
        porta_sup_rect = porta_sup.get_rect(midtop=(res_x//2,35))
        porta_inf = carica_immagine(animazione_porta('down',info_stanze[tuple(player_data['stanza'])]['nemici'], porte_frames, 50, sound_door_close, sound_door_open))
        porta_inf_rect = porta_inf.get_rect(midbottom=(res_x//2,res_y - 35))
        porta_dx = carica_immagine(animazione_porta('right',info_stanze[tuple(player_data['stanza'])]['nemici'], porte_frames, 50, sound_door_close, sound_door_open))
        porta_dx_rect = porta_dx.get_rect(midright=(res_x - 105,res_y//2))
        porta_sx = carica_immagine(animazione_porta('left',info_stanze[tuple(player_data['stanza'])]['nemici'], porte_frames, 50, sound_door_close, sound_door_open))
        porta_sx_rect = porta_sx.get_rect(midleft=(105,res_y//2))

        # BOTOLA
        botola_image = carica_immagine('res/img/botola/botola_0.png', (2.5,2.5))
        botola_rect = botola_image.get_rect(center= (res_x//2, res_y//2))

        # GESTIONE EVENTI
        for evento in pygame.event.get():
            key_pressed = evento.type == pygame.KEYDOWN
            key_released = evento.type == pygame.KEYUP
            mouse_click = evento.type == pygame.MOUSEBUTTONDOWN

            if key_pressed and evento.key == pygame.K_ESCAPE:
                if not metti_pausa:
                    is_pausa = True
                    sound_menu_appear.play()
                elif not is_inizio and not is_game_over and not is_vittoria:
                    is_pausa = False
                    sound_menu_hide.play()
            
            if key_pressed and evento.key == pygame.K_RETURN:
                if is_inizio:
                    sound_menu_hide.play()
                is_inizio = False

            if mouse_click and evento.button == pygame.BUTTON_LEFT:
                if is_inizio and start_button_inizio_rect.collidepoint(pos_mouse):
                    is_inizio = False
                    sound_menu_hide.play()
                elif is_inizio and volume_up_button_rect.collidepoint(pos_mouse):
                    if moltiplicatore_audio < 100:
                        moltiplicatore_audio += 1
                        moltiplicatore_audio_perc = moltiplicatore_audio/10
                        pygame.mixer.music.set_volume(0.05*moltiplicatore_audio_perc)
                        sound_nemico1_1.set_volume(0.035*moltiplicatore_audio_perc)
                        sound_nemico1_2.set_volume(0.035*moltiplicatore_audio_perc)
                        sound_tear_1.set_volume(0.07*moltiplicatore_audio_perc)
                        sound_tear_2.set_volume(0.07*moltiplicatore_audio_perc)
                        sound_tear_end.set_volume(0.07*moltiplicatore_audio_perc)
                        sound_danno.set_volume(0.04*moltiplicatore_audio_perc)
                        sound_door_close.set_volume(0.05*moltiplicatore_audio_perc)
                        sound_door_open.set_volume(0.05*moltiplicatore_audio_perc)
                        sound_menu_appear.set_volume(0.2*moltiplicatore_audio_perc)
                        sound_menu_hide.set_volume(0.2*moltiplicatore_audio_perc)
                        salva_dati('volume', moltiplicatore_audio)
                elif is_inizio and volume_down_button_rect.collidepoint(pos_mouse):
                    if moltiplicatore_audio > 0:
                        moltiplicatore_audio -= 1
                        moltiplicatore_audio_perc = moltiplicatore_audio/10
                        pygame.mixer.music.set_volume(0.05*moltiplicatore_audio_perc)
                        sound_nemico1_1.set_volume(0.035*moltiplicatore_audio_perc)
                        sound_nemico1_2.set_volume(0.035*moltiplicatore_audio_perc)
                        sound_tear_1.set_volume(0.07*moltiplicatore_audio_perc)
                        sound_tear_2.set_volume(0.07*moltiplicatore_audio_perc)
                        sound_tear_end.set_volume(0.07*moltiplicatore_audio_perc)
                        sound_danno.set_volume(0.04*moltiplicatore_audio_perc)
                        sound_door_close.set_volume(0.05*moltiplicatore_audio_perc)
                        sound_door_open.set_volume(0.05*moltiplicatore_audio_perc)
                        sound_menu_appear.set_volume(0.2*moltiplicatore_audio_perc)
                        sound_menu_hide.set_volume(0.2*moltiplicatore_audio_perc)
                        salva_dati('volume', moltiplicatore_audio)
                elif is_pausa and riprendi_button_pausa_rect.collidepoint(pos_mouse):
                    is_pausa = False
                    sound_menu_hide.play()
                elif (is_pausa or is_game_over or is_vittoria) and ricomincia_button_rect.collidepoint(pos_mouse):
                    return True
                elif metti_pausa and exit_button_rect.collidepoint(pos_mouse):
                    pygame.quit()
                    return False
            
            if key_pressed and evento.key == pygame.K_w:
                comandi['W'] = True
            if key_pressed and evento.key == pygame.K_a:
                comandi['A'] = True
            if key_pressed and evento.key == pygame.K_s:
                comandi['S'] = True
            if key_pressed and evento.key == pygame.K_d:
                comandi['D'] = True
            if key_released and evento.key == pygame.K_w:
                comandi['W'] = False
            if key_released and evento.key == pygame.K_a:
                comandi['A'] = False
            if key_released and evento.key == pygame.K_s:
                comandi['S'] = False
            if key_released and evento.key == pygame.K_d:
                comandi['D'] = False
            
            if key_pressed and evento.key == pygame.K_UP:
                comandi['UP'] = True
            if key_pressed and evento.key == pygame.K_LEFT:
                comandi['LEFT'] = True
            if key_pressed and evento.key == pygame.K_DOWN:
                comandi['DOWN'] = True
            if key_pressed and evento.key == pygame.K_RIGHT:
                comandi['RIGHT'] = True
            if key_released and evento.key == pygame.K_UP:
                comandi['UP'] = False
            if key_released and evento.key == pygame.K_LEFT:
                comandi['LEFT'] = False
            if key_released and evento.key == pygame.K_DOWN:
                comandi['DOWN'] = False
            if key_released and evento.key == pygame.K_RIGHT:
                comandi['RIGHT'] = False
        
            if evento.type == pygame.QUIT:
                pygame.quit()
                return False
        
        # GESTIONE PLAYER
        if not metti_pausa:
            if comandi['W'] and player_data['player_acc']['W'] < 1:
                player_data['player_acc']['W'] += 0.1
            elif player_data['player_acc']['W'] > 0:
                player_data['player_acc']['W'] -= 0.1
            elif player_data['player_acc']['W'] < 0:
                player_data['player_acc']['W'] = 0
            if comandi['A'] and player_data['player_acc']['A'] < 1:
                player_data['player_acc']['A'] += 0.1
            elif player_data['player_acc']['A'] > 0:
                player_data['player_acc']['A'] -= 0.1
            elif player_data['player_acc']['A'] < 0:
                player_data['player_acc']['A'] = 0
            if comandi['S'] and player_data['player_acc']['S'] < 1:
                player_data['player_acc']['S'] += 0.1
            elif player_data['player_acc']['S'] > 0:
                player_data['player_acc']['S'] -= 0.1
            elif player_data['player_acc']['S'] < 0:
                player_data['player_acc']['S'] = 0
            if comandi['D'] and player_data['player_acc']['D'] < 1:
                player_data['player_acc']['D'] += 0.1
            elif player_data['player_acc']['D'] > 0:
                player_data['player_acc']['D'] -= 0.1
            elif player_data['player_acc']['D'] < 0:
                player_data['player_acc']['D'] = 0
        else:
            for key in player_data['player_acc']:
                player_data['player_acc'][key] = 0

        if not player_rect.colliderect(wall_sup_rect):
            player_data['pos'][1] -= player_data['velocita']*player_data['player_acc']['W']
        if not player_rect.colliderect(wall_sx_rect):
            player_data['pos'][0] -= player_data['velocita']*player_data['player_acc']['A']
        if not player_rect.colliderect(wall_inf_rect):
            player_data['pos'][1] += player_data['velocita']*player_data['player_acc']['S']
        if not player_rect.colliderect(wall_dx_rect):
            player_data['pos'][0] += player_data['velocita']*player_data['player_acc']['D']
        
        for roccia in info_stanze[tuple(player_data['stanza'])]['rocce']:
            dx = player_data['pos'][0] - roccia['pos'][0]
            dy = player_data['pos'][1] - roccia['pos'][1]
            vettore_direzione = pygame.math.Vector2(dx,dy)
            vettore_direzione.normalize()
            if vettore_direzione.length() < 40:
                player_data['pos'][0] += vettore_direzione[0] * 0.125
                player_data['pos'][1] += vettore_direzione[1] * 0.125

        if player_data['vita'][1] > 0:
            player_data['vita'][1] -= 1
        
        if player_data['vita'][0] == 0:
            is_game_over = True
            if riproduci_sound_menu_appear: 
                riproduci_sound_menu_appear = False
                sound_menu_appear.play()
        
        # ATTACCO PLAYER
        if player_data['proiettili']['timer'] > 0:
            player_data['proiettili']['timer'] -= 1
        
        if player_data['proiettili']['timer'] == 0 and not metti_pausa:
            if comandi['LEFT']:
                player_data['proiettili']['timer'] = proiettili_timer
                genera_proiettile('LEFT',player_data['proiettili']['lista'],player_data['pos'])
                riproduci_suono_random((sound_tear_1,sound_tear_2))
            elif comandi['RIGHT']:
                player_data['proiettili']['timer'] = proiettili_timer
                genera_proiettile('RIGHT',player_data['proiettili']['lista'],player_data['pos'])
                riproduci_suono_random((sound_tear_1,sound_tear_2))
            elif comandi['DOWN']:
                player_data['proiettili']['timer'] = proiettili_timer
                genera_proiettile('DOWN',player_data['proiettili']['lista'],player_data['pos'])
                riproduci_suono_random((sound_tear_1,sound_tear_2))
            elif comandi['UP']:
                player_data['proiettili']['timer'] = proiettili_timer
                genera_proiettile('UP',player_data['proiettili']['lista'],player_data['pos'])
                riproduci_suono_random((sound_tear_1,sound_tear_2))

        if not metti_pausa:
            # GESTIONE PROIETTILI
            for proiettile in player_data['proiettili']['lista']:
                spostamento_proiettile(proiettile, 6)
                if proiettile['rect'] and (proiettile['rect'].colliderect(wall_dx_rect) or proiettile['rect'].colliderect(wall_sx_rect) or proiettile['rect'].colliderect(wall_inf_rect) or proiettile['rect'].colliderect(wall_sup_rect)):
                    if not proiettile['impact']:
                        sound_tear_end.play()
                    proiettile['impact'] = True
                for nemico in info_stanze[tuple(player_data['stanza'])]['nemici']:
                    if proiettile['rect'] and proiettile['rect'].collidepoint(nemico['pos'][0],nemico['pos'][1]):
                        if not proiettile['impact']:
                            nemico['vita'] -= 1
                            respingi_nemico(proiettile['direzione'], nemico['pos'], 10)
                            nemico['frame_animazione'][2] += 1
                            sound_tear_end.play()
                        proiettile['impact'] = True
                for roccia in info_stanze[tuple(player_data['stanza'])]['rocce']:
                    if proiettile['rect'] and proiettile['rect'].collidepoint(roccia['pos'][0],roccia['pos'][1]):
                        if not proiettile['impact']:
                            sound_tear_end.play()
                        proiettile['impact'] = True
                if proiettile['impact'] and proiettile['frame_animazione'][0] == 6:
                    player_data['proiettili']['lista'].remove(proiettile)

            # GESTIONE NEMICI
            for nemico in info_stanze[tuple(player_data['stanza'])]['nemici']:
                direzione_nemico(nemico['pos'],player_data['pos'])
                if nemico['freeze_countdown'] != 0:
                    nemico['freeze_countdown'] -= 1
                else:
                    cammina(nemico, player_data['pos'], info_stanze[tuple(player_data['stanza'])]['nemici'],info_stanze[tuple(player_data['stanza'])]['rocce'], 2.5)
                    if random.choices([True,False],weights=[1,500], k=1)[0]:
                        riproduci_suono_random((sound_nemico1_1,sound_nemico1_2))
                
                if nemico['vita'] == 0:
                    info_stanze[tuple(player_data['stanza'])]['nemici'].remove(nemico)
                    punteggio += 10
                
                if nemico['rect'].collidepoint(player_data['pos'][0],player_data['pos'][1]) and player_data['vita'][1] == 0:
                    player_data['vita'][0] -= 1
                    player_data['vita'][1] = 120
                    punteggio -= 25
                    sound_danno.play()

                if nemico['frame_animazione'][2] == 15:
                    nemico['frame_animazione'][2] = -1
                elif nemico['frame_animazione'][2] >= 0:
                    nemico['frame_animazione'][2] += 1

        # CAMBIO STANZA PLAYER
        if info_stanze[tuple(player_data['stanza'])]['nemici'] == []:
            player_data['timer_stanza'] = 0
        else:
            player_data['timer_stanza'] += 1

        if info_stanze[tuple(player_data['stanza'])]['nemici'] == []:
            if porte_stanza(map,player_data['stanza'][0],player_data['stanza'][1])['up'] and player_rect.collidepoint((porta_sup_rect.centerx, porta_sup_rect.centery - 10)) and comandi['W']:
                player_data['stanza'][0] -= 1
                player_data['pos'][1] = porta_inf_rect.centery - 75
                player_data['proiettili']['lista'] = []
            if porte_stanza(map,player_data['stanza'][0],player_data['stanza'][1])['down'] and player_rect.collidepoint((porta_inf_rect.centerx, porta_inf_rect.centery - 45)) and comandi['S']:
                player_data['stanza'][0] += 1
                player_data['pos'][1] = porta_sup_rect.centery + 25
                player_data['proiettili']['lista'] = []
            if porte_stanza(map,player_data['stanza'][0],player_data['stanza'][1])['right'] and player_rect.collidepoint((porta_dx_rect.centerx - 30, porta_dx_rect.centery)) and comandi['D']:
                player_data['stanza'][1] += 1
                player_data['pos'][0] = porta_sx_rect.centerx + 50
                player_data['proiettili']['lista'] = []
            if porte_stanza(map,player_data['stanza'][0],player_data['stanza'][1])['left'] and player_rect.collidepoint((porta_sx_rect.centerx + 30, porta_sx_rect.centery)) and comandi['A']:
                player_data['stanza'][1] -= 1
                player_data['pos'][0] = porta_dx_rect.centerx - 50
                player_data['proiettili']['lista'] = []
            if map[player_data['stanza'][0]][player_data['stanza'][1]] == 2 and player_rect.collidepoint((botola_rect.centerx, botola_rect.centery)):
                is_vittoria = True
                if assegna_punteggio_finale:
                    if tempo//60 < 300:
                        punteggio += 100 * n_stanze
                    elif tempo//60 < 600:
                        punteggio += 80 * n_stanze
                    elif tempo//60 < 900:
                        punteggio += 60 * n_stanze
                    else:
                        punteggio += 40 * n_stanze
                    assegna_punteggio_finale = False

                if riproduci_sound_menu_appear: 
                    riproduci_sound_menu_appear = False
                    sound_menu_appear.play()
        
        # RENDER ELEMENTI
        if player_data['stanza'] == [len(map)//2,len(map)//2]:
            schermo.blit(stanza_inizio_background,(0,0))
        else:
            schermo.blit(stanza_background,(0,0))
        
        schermo.blits((
            (tempo_testo, tempo_testo_rect),
            (punteggio_testo, punteggio_testo_rect),
            (vita_image, vita_rect)
        ))

        # RENDER PORTE
        if info_stanze[tuple(player_data['stanza'])]['porte']['up']:
            schermo.blit(porta_sup,porta_sup_rect)
        if info_stanze[tuple(player_data['stanza'])]['porte']['down']:
            schermo.blit(porta_inf,porta_inf_rect)
        if info_stanze[tuple(player_data['stanza'])]['porte']['right']:
            schermo.blit(porta_dx,porta_dx_rect)
        if info_stanze[tuple(player_data['stanza'])]['porte']['left']:
            schermo.blit(porta_sx,porta_sx_rect)

        # RENDER BOTOLA
        if map[player_data['stanza'][0]][player_data['stanza'][1]] == 2:
            botola_image = carica_immagine(animazione_botola(botola_frames, info_stanze[tuple(player_data['stanza'])]['nemici'], 3),(2.5,2.5))
            schermo.blit(botola_image, botola_rect)
        
        # RENDER DINAMICO ENTITA
        entita_da_renderizzare = [
            (player,player_rect)
        ]

        for nemico in info_stanze[tuple(player_data['stanza'])]['nemici']:
            if map[player_data['stanza'][0]][player_data['stanza'][1]] == 2:
                nemico_image = carica_immagine(nemico1_animation(nemico, player_data['pos'], nemico1_frames, 10, metti_pausa, 1),(2.5,2.5))
            else:
                nemico_image = carica_immagine(nemico1_animation(nemico, player_data['pos'], nemico1_frames, 10, metti_pausa, 0),(2.5,2.5))
            nemico_rect = nemico_image.get_rect(center= nemico['pos'])
            nemico['rect'] = nemico_rect
            entita_da_renderizzare.append((nemico_image,nemico_rect))
        
        for proiettile in player_data['proiettili']['lista']:
            proiettile_image = carica_immagine(proiettile_animation(proiettile,proiettile_frames,1), (3.2,3.2))
            proiettile_rect = proiettile_image.get_rect(center= proiettile['pos'])
            proiettile['rect'] = proiettile_rect
            entita_da_renderizzare.append((proiettile_image,proiettile_rect))
        
        for roccia in info_stanze[tuple(player_data['stanza'])]['rocce']:
            entita_da_renderizzare.append((roccia['image'], roccia['rect']))

        entita_da_renderizzare.sort(key=lambda x: x[1].centery)
        schermo.blits(entita_da_renderizzare)

        # MENU INIZIO
        if is_inizio:
            schermo.blits((
                (pausa_pergamena, pausa_pergamena_rect),
                (inizio_title, inizio_title_rect),
                (record_title, record_title_rect),
                (start_button_inizio,start_button_inizio_rect),
                (exit_button, exit_button_rect),
                (volume_text, volume_text_rect),
                (volume_up_button, volume_up_button_rect),
                (volume_down_button, volume_down_button_rect)
            ))

        # MENU PAUSA
        if is_pausa:
            schermo.blits((
                (pausa_pergamena, pausa_pergamena_rect),
                (pausa_title, pausa_title_rect),
                (record_title, record_title_rect),
                (riprendi_button_pausa, riprendi_button_pausa_rect),
                (ricomincia_button, ricomincia_button_rect),
                (exit_button, exit_button_rect)
            ))
        
        # MENU GAME OVER
        if is_game_over:
            punteggio_finale_title = crea_testo(f'Hai totalizzato {punteggio} punti', 70,'gray20')
            punteggio_finale_title_rect = punteggio_finale_title.get_rect(center= (res_x//2,res_y//2))
            
            if punteggio > dati_salvataggio["record"]:
                salva_dati('record', punteggio)

            schermo.blits((
                (pausa_pergamena, pausa_pergamena_rect),
                (game_over_title, game_over_title_rect),
                (punteggio_finale_title, punteggio_finale_title_rect),
                (ricomincia_button, ricomincia_button_rect),
                (exit_button, exit_button_rect)
            ))

        # MENU VITTORIA
        if is_vittoria:
            punteggio_finale_title = crea_testo(f'Hai totalizzato {punteggio} punti', 70,'gray20')
            punteggio_finale_title_rect = punteggio_finale_title.get_rect(center= (res_x//2,res_y//2))
            
            if punteggio > dati_salvataggio["record"]:
                salva_dati('record', punteggio)

            schermo.blits((
                (pausa_pergamena, pausa_pergamena_rect),
                (vittoria_title, vittoria_title_rect),
                (punteggio_finale_title, punteggio_finale_title_rect),
                (ricomincia_button, ricomincia_button_rect),
                (exit_button, exit_button_rect)
            ))

        if not metti_pausa:
            tempo += 1

        pygame.display.update()
        clock.tick(60)

def main():
    pygame.init()
    while True:
        numero_stanze = 20
        map = genera_mappa(numero_stanze, numero_stanze)
        
        if not game(map, numero_stanze):
            break

main()
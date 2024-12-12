from random import randint
import time
import berserk
from dotenv import load_dotenv
import os

load_dotenv()

lichess_token = os.getenv('LICHESS_TOKEN')

session = berserk.TokenSession(lichess_token)
client = berserk.Client(session)

def initialisation_zobrist(): #cree le tableau necessaire au zobrist hashing
    return [[[randint(1,2**64-1) for i in range(12)] for j in range(8)] for k in range (8)]

def zobrist_hash(echiquier,tab_zobrist): #hash qui permet d'indentifier de maniere unique une position
    h = 0
    for n in range(12):
        cases = decomposition_position(echiquier[n])
        for case in cases:
            indices = indices_binaire(case)
            h ^= tab_zobrist[indices[0]][indices[1]][n]
    return h

def coups_piece(position,position_piece,piece_index,manger): #donne l'ensemble des coups possibles pour une piece donnée
    position_blanc = position[12]
    position_noir = position[13]
    position_tot = position[-1]
    petit_rock_blanc,grand_rock_blanc,petit_rock_noir,grand_rock_noir = position[15],position[16],position[17],position[18]
    if piece_index == 5 :
        position_copie = position_piece
        roi_centre = ((position_piece & 35604928818740736) >> 1) | ((position_piece & 35604928818740736) << 1) | ((position_piece & 35604928818740736) >> 8) | ((position_piece & 35604928818740736) << 8) | ((position_piece & 35604928818740736) >> 7) | ((position_piece & 35604928818740736) << 7) | ((position_piece & 35604928818740736) >> 9) | ((position_piece & 35604928818740736) << 9)
        roi_1 = ((position_piece & 9079256848778919936) >> 1) | ((position_piece & 9079256848778919936) << 1) | ((position_piece & 9079256848778919936) >> 8) | ((position_piece & 9079256848778919936) >> 7) | ((position_piece & 9079256848778919936) >> 9)
        roi_8 = ((position_piece & 126) >> 1) | ((position_piece & 126) << 1) | ((position_piece & 126) << 8) | ((position_piece & 126) << 7) | ((position_piece & 126) << 9)
        roi_A = ((position_piece & 36170086419038208) >> 1) | ((position_piece & 36170086419038208) >> 8) | ((position_piece & 36170086419038208) << 8) | ((position_piece & 36170086419038208) << 7) | ((position_piece & 36170086419038208) >> 9)
        roi_H = ((position_piece & 282578800148736) << 1) | ((position_piece & 282578800148736) >> 8) | ((position_piece & 282578800148736) << 8) | ((position_piece & 282578800148736) << 9) | ((position_piece & 282578800148736) >> 7)
        roi_A1 = ((position_piece & 9223372036854775808) >> 1) | ((position_piece & 9223372036854775808) >> 8) | ((position_piece & 9223372036854775808) >> 9)
        roi_H1 = ((position_piece & 72057594037927936) << 1) | ((position_piece & 72057594037927936) >> 8) | ((position_piece & 72057594037927936) >> 7)
        roi_A8 = ((position_piece & 128) >> 1) | ((position_piece & 128) << 8) | ((position_piece & 128) << 7)
        roi_H8 = ((position_piece & 1) << 1) | ((position_piece & 1) << 8) | ((position_piece & 1) << 9)
        position_piece = roi_centre | roi_1 | roi_8 | roi_A | roi_H | roi_A1 | roi_H1 | roi_A8 | roi_H8
        if petit_rock_blanc == True and (position_tot & 432345564227567616)==0 and (position[1] & 72057594037927936) and not manger:
            position_piece |= ((position_copie & 576460752303423488) >> 2)
        if grand_rock_blanc == True and (position_tot & 8070450532247928832)==0 and (position[1] & 9223372036854775808) and not manger:
            position_piece |= ((position_copie & 576460752303423488) << 2)
        if not manger:
            position_piece &= ~position_blanc
        return position_piece
    elif piece_index == 4:
        if manger:
            prise_pions = ((position_piece & 9187201950435737471) >> 7) | ((position_piece & 18374403900871474942) >> 9)
            return prise_pions
        else :
            prise_pions = (((position_piece & 9187201950435737471) >> 7) | ((position_piece & 18374403900871474942) >> 9)) & (position_noir | position[19][1])
            pions_init = ((position_piece & 71776119061217280) & (~((((position_piece & 71776119061217280) >> 8) & position_tot) << 8))) >> 16
            position_piece >>= 8
            position_piece |= pions_init
            position_piece &= ~position_tot
            position_piece |= prise_pions
            return position_piece
    elif piece_index == 3:
        caval_centre = ((position_piece & 66229406269440) >> 17) | ((position_piece & 66229406269440) >> 15) | ((position_piece & 66229406269440) >> 10) | ((position_piece & 66229406269440) >> 6) | ((position_piece & 66229406269440) << 6) | ((position_piece & 66229406269440) << 10) | ((position_piece & 66229406269440) << 15) | ((position_piece & 66229406269440) << 17)
        caval_1 = ((position_piece & 4323455642275676160) >> 17) | ((position_piece & 4323455642275676160) >> 15) | ((position_piece & 4323455642275676160) >> 10) | ((position_piece & 4323455642275676160) >> 6)
        caval_2 = ((position_piece & 16888498602639360) >> 17) | ((position_piece & 16888498602639360) >> 15) | ((position_piece & 16888498602639360) >> 10) | ((position_piece & 16888498602639360) >> 6) | ((position_piece & 16888498602639360) << 10) | ((position_piece & 16888498602639360) << 6)
        caval_7 = ((position_piece & 15360) >> 10) | ((position_piece & 15360) >> 6) | ((position_piece & 15360) << 6) | ((position_piece & 15360) << 10) | ((position_piece & 15360) << 15) | ((position_piece & 15360) << 17)
        caval_8 = ((position_piece & 60) << 6) | ((position_piece & 60) << 10) | ((position_piece & 60) << 15) | ((position_piece & 60) << 17)
        caval_A = ((position_piece & 141289400041472) >> 17) | ((position_piece & 141289400041472) >> 10) | ((position_piece & 141289400041472) << 15) | ((position_piece & 141289400041472) << 6)
        caval_B = ((position_piece & 70644700020736) >> 17) | ((position_piece & 70644700020736) >> 10) | ((position_piece & 70644700020736) << 15) | ((position_piece & 70644700020736) << 6) | ((position_piece & 70644700020736) >> 15) | ((position_piece & 70644700020736) << 17)
        caval_G = ((position_piece & 2207646875648) >> 17) | ((position_piece & 2207646875648) << 10) | ((position_piece & 2207646875648) << 15) | ((position_piece & 2207646875648) >> 6) | ((position_piece & 2207646875648) >> 15) | ((position_piece & 2207646875648) << 17)
        caval_H = ((position_piece & 1103823437824) << 10) | ((position_piece & 1103823437824) >> 6) | ((position_piece & 1103823437824) >> 15) | ((position_piece & 1103823437824) << 17)
        caval_A1 = ((position_piece & 9223372036854775808) >> 17) | ((position_piece & 9223372036854775808) >> 10)
        caval_B1 = ((position_piece & 4611686018427387904) >> 17) | ((position_piece & 4611686018427387904) >> 15) | ((position_piece & 4611686018427387904) >> 10)
        caval_G1 = ((position_piece & 144115188075855872) >> 17) | ((position_piece & 144115188075855872) >> 15) | ((position_piece & 144115188075855872) >> 6)
        caval_H1 = ((position_piece & 72057594037927936) >> 6) | ((position_piece & 72057594037927936) >> 15)
        caval_A2 = ((position_piece & 36028797018963968) >> 17) | ((position_piece & 36028797018963968) >> 10) | ((position_piece & 36028797018963968) << 6)
        caval_B2 = ((position_piece & 18014398509481984) >> 17) | ((position_piece & 18014398509481984) >> 15) | ((position_piece & 18014398509481984) >> 10) | ((position_piece & 18014398509481984) << 6)
        caval_G2 = ((position_piece & 562949953421312) >> 17) | ((position_piece & 562949953421312) >> 15) | ((position_piece & 562949953421312) << 10) | ((position_piece & 562949953421312) >> 6)
        caval_H2 = ((position_piece & 281474976710656) >> 6) | ((position_piece & 281474976710656) >> 15) | ((position_piece & 281474976710656) << 10)
        caval_A7 = ((position_piece & 32768) << 6) | ((position_piece & 32768) << 15) | ((position_piece & 32768) >> 10)
        caval_B7 = ((position_piece & 16384) << 17) | ((position_piece & 16384) << 15) | ((position_piece & 16384) >> 10) | ((position_piece & 16384) << 6)
        caval_G7 = ((position_piece & 512) << 17) | ((position_piece & 512) << 15) | ((position_piece & 512) << 10) | ((position_piece & 512) >> 6)
        caval_H7 = ((position_piece & 256) << 17) | ((position_piece & 256) >> 6) | ((position_piece & 256) << 10)
        caval_A8 = ((position_piece & 128) << 6) | ((position_piece & 128) << 15)
        caval_B8 = ((position_piece & 64) << 17) | ((position_piece & 64) << 15) | ((position_piece & 64) << 6)
        caval_G8 = ((position_piece & 2) << 17) | ((position_piece & 2) << 15) | ((position_piece & 2) << 10)
        caval_H8 = ((position_piece & 1) << 17) | ((position_piece & 1) << 10)
        position_piece = caval_centre | caval_A | caval_B | caval_G | caval_H | caval_1 | caval_2 | caval_7 | caval_8 | caval_A1 | caval_A2 | caval_A7 | caval_A8 | caval_B1 | caval_B2 | caval_B7 | caval_B8 | caval_G1 | caval_G2 | caval_G7 | caval_G8 | caval_H1 | caval_H2 | caval_H7 | caval_H8
        if not manger :
            position_piece &= ~position_blanc
        return position_piece
    elif piece_index == 2:
        pieces_pos = decomposition_position(position_piece)
        union_pos_piece = 0
        for pos_piece in pieces_pos:
            indices = indices_binaire(pos_piece)
            copie_position1,copie_position2,copie_position3,copie_position4 = pos_piece,pos_piece,pos_piece,pos_piece
            i1,i2,i3,i4,j1,j2,j3,j4 = indices[0],indices[0],indices[0],indices[0],indices[1],indices[1],indices[1],indices[1]
            while (copie_position1 & (position_tot & ~pos_piece)) == 0 and i1<7 and j1<7:
                i1+=1
                j1+=1
                copie_position1 |= copie_position1 >> 9
            while (copie_position2 & (position_tot & ~pos_piece)) == 0 and i2<7 and j2>0:
                i2+=1
                j2-=1
                copie_position2 |= copie_position2 >> 7
            while (copie_position3 & (position_tot & ~pos_piece)) == 0 and i3>0 and j3<7:
                i3-=1
                j3+=1
                copie_position3 |= copie_position3 << 7
            while (copie_position4 & (position_tot & ~pos_piece)) == 0 and i4>0 and j4>0:
                i4-=1
                j4-=1
                copie_position4 |= copie_position4 << 9
            union_pos_piece |= copie_position1 | copie_position2 | copie_position3 | copie_position4
        if not manger :
            union_pos_piece &= ~position_blanc
        else :
            union_pos_piece &= ~position_piece
        return union_pos_piece
    elif piece_index == 1:
        pieces_pos = decomposition_position(position_piece)
        union_pos_piece = 0
        for pos_piece in pieces_pos:
            indices = indices_binaire(pos_piece)
            copie_position1,copie_position2,copie_position3,copie_position4 = pos_piece,pos_piece,pos_piece,pos_piece
            i1,i2,j1,j2 = indices[0],indices[0],indices[1],indices[1]
            while (copie_position1 & (position_tot & ~pos_piece)) == 0 and i1<7:
                i1+=1
                copie_position1 |= copie_position1 >> 8
            while (copie_position2 & (position_tot & ~pos_piece)) == 0 and i2>0:
                i2-=1
                copie_position2 |= copie_position2 << 8
            while (copie_position3 & (position_tot & ~pos_piece)) == 0 and j1<7:
                j1+=1
                copie_position3 |= copie_position3 >> 1
            while (copie_position4 & (position_tot & ~pos_piece)) == 0 and j2>0:
                j2-=1
                copie_position4 |= copie_position4 << 1
            union_pos_piece |= copie_position1 | copie_position2 | copie_position3 | copie_position4
        if not manger :
            union_pos_piece &= ~position_blanc
        else :
            union_pos_piece &= ~position_piece
        return union_pos_piece
    elif piece_index == 0:
        pieces_pos = decomposition_position(position_piece)
        union_pos_piece = 0
        for pos_piece in pieces_pos:
            indices = indices_binaire(pos_piece)
            copie_position1,copie_position2,copie_position3,copie_position4,copie_position5,copie_position6,copie_position7,copie_position8 = pos_piece,pos_piece,pos_piece,pos_piece,pos_piece,pos_piece,pos_piece,pos_piece
            i1,i2,i3,i4,i5,i6,j1,j2,j3,j4,j5,j6=indices[0],indices[0],indices[0],indices[0],indices[0],indices[0],indices[1],indices[1],indices[1],indices[1],indices[1],indices[1]
            while (copie_position1 & (position_tot & ~pos_piece)) == 0 and i1 < 7 and j1 < 7:
                i1+=1
                j1+=1
                copie_position1 |= copie_position1 >> 9
            while (copie_position2 & (position_tot & ~pos_piece)) == 0 and i2 < 7 and j2 > 0:
                i2+=1
                j2-=1
                copie_position2 |= copie_position2 >> 7
            while (copie_position3 & (position_tot & ~pos_piece)) == 0 and i3 > 0 and j3 < 7:
                i3-=1
                j3+=1
                copie_position3 |= copie_position3 << 7
            while (copie_position4 & (position_tot & ~pos_piece)) == 0 and i4 > 0 and j4 > 0:
                i4-=1
                j4-=1
                copie_position4 |= copie_position4 << 9
            while (copie_position5 & (position_tot & ~pos_piece)) == 0 and i5<7:
                i5+=1
                copie_position5 |= copie_position5 >> 8
            while (copie_position6 & (position_tot & ~pos_piece)) == 0 and i6>0:
                i6-=1
                copie_position6 |= copie_position6 << 8
            while (copie_position7 & (position_tot & ~pos_piece)) == 0 and j5<7:
                j5+=1
                copie_position7 |= copie_position7 >> 1
            while (copie_position8 & (position_tot & ~pos_piece)) == 0 and j6>0:
                j6-=1
                copie_position8 |= copie_position8 << 1
            union_pos_piece |= copie_position1 | copie_position2 | copie_position3 | copie_position4 | copie_position5 | copie_position6 | copie_position7 | copie_position8
        if not manger:
            union_pos_piece &= ~position_blanc
        else :
            union_pos_piece &= ~position_piece
        return union_pos_piece
    elif piece_index == 11 :
        position_copie = position_piece
        roi_centre = ((position_piece & 35604928818740736) >> 1) | ((position_piece & 35604928818740736) << 1) | ((position_piece & 35604928818740736) >> 8) | ((position_piece & 35604928818740736) << 8) | ((position_piece & 35604928818740736) >> 7) | ((position_piece & 35604928818740736) << 7) | ((position_piece & 35604928818740736) >> 9) | ((position_piece & 35604928818740736) << 9)
        roi_1 = ((position_piece & 9079256848778919936) >> 1) | ((position_piece & 9079256848778919936) << 1) | ((position_piece & 9079256848778919936) >> 8) | ((position_piece & 9079256848778919936) >> 7) | ((position_piece & 9079256848778919936) >> 9)
        roi_8 = ((position_piece & 126) >> 1) | ((position_piece & 126) << 1) | ((position_piece & 126) << 8) | ((position_piece & 126) << 7) | ((position_piece & 126) << 9)
        roi_A = ((position_piece & 36170086419038208) >> 1) | ((position_piece & 36170086419038208) >> 8) | ((position_piece & 36170086419038208) << 8) | ((position_piece & 36170086419038208) << 7) | ((position_piece & 36170086419038208) >> 9)
        roi_H = ((position_piece & 282578800148736) << 1) | ((position_piece & 282578800148736) >> 8) | ((position_piece & 282578800148736) << 8) | ((position_piece & 282578800148736) << 9) | ((position_piece & 282578800148736) >> 7)
        roi_A1 = ((position_piece & 9223372036854775808) >> 1) | ((position_piece & 9223372036854775808) >> 8) | ((position_piece & 9223372036854775808) >> 9)
        roi_H1 = ((position_piece & 72057594037927936) << 1) | ((position_piece & 72057594037927936) >> 8) | ((position_piece & 72057594037927936) >> 7)
        roi_A8 = ((position_piece & 128) >> 1) | ((position_piece & 128) << 8) | ((position_piece & 128) << 7)
        roi_H8 = ((position_piece & 1) << 1) | ((position_piece & 1) << 8) | ((position_piece & 1) << 9)
        position_piece = roi_centre | roi_1 | roi_8 | roi_A | roi_H | roi_A1 | roi_H1 | roi_A8 | roi_H8
        if petit_rock_noir == True and (position_tot & 6)==0 and (position[7] & 1) and not manger:
            position_piece |= ((position_copie & 8) >> 2)
        if grand_rock_noir == True and (position_tot & 112)==0 and (position[7] & 128) and not manger:
            position_piece |= ((position_copie & 8) << 2)
        if not manger :
            position_piece &= ~position_noir
        return position_piece
    elif piece_index == 10:
        if manger :
            prise_pions = ((position_piece & 9187201950435737471) << 9) | ((position_piece & 18374403900871474942) << 7)
            return prise_pions
        else :
            prise_pions = (((position_piece & 9187201950435737471) << 9) | ((position_piece & 18374403900871474942) <<7)) & (position_blanc | position[19][0])
            pions_init = ((position_piece & 65280) & (~((((position_piece & 65280) << 8) & position_tot) >> 8))) << 16
            position_piece <<= 8
            position_piece |= pions_init
            position_piece &= ~position_tot
            position_piece |= prise_pions
            return position_piece
    elif piece_index == 9:
        caval_centre = ((position_piece & 66229406269440) >> 17) | ((position_piece & 66229406269440) >> 15) | ((position_piece & 66229406269440) >> 10) | ((position_piece & 66229406269440) >> 6) | ((position_piece & 66229406269440) << 6) | ((position_piece & 66229406269440) << 10) | ((position_piece & 66229406269440) << 15) | ((position_piece & 66229406269440) << 17)
        caval_1 = ((position_piece & 4323455642275676160) >> 17) | ((position_piece & 4323455642275676160) >> 15) | ((position_piece & 4323455642275676160) >> 10) | ((position_piece & 4323455642275676160) >> 6)
        caval_2 = ((position_piece & 16888498602639360) >> 17) | ((position_piece & 16888498602639360) >> 15) | ((position_piece & 16888498602639360) >> 10) | ((position_piece & 16888498602639360) >> 6) | ((position_piece & 16888498602639360) << 10) | ((position_piece & 16888498602639360) << 6)
        caval_7 = ((position_piece & 15360) >> 10) | ((position_piece & 15360) >> 6) | ((position_piece & 15360) << 6) | ((position_piece & 15360) << 10) | ((position_piece & 15360) << 15) | ((position_piece & 15360) << 17)
        caval_8 = ((position_piece & 60) << 6) | ((position_piece & 60) << 10) | ((position_piece & 60) << 15) | ((position_piece & 60) << 17)
        caval_A = ((position_piece & 141289400041472) >> 17) | ((position_piece & 141289400041472) >> 10) | ((position_piece & 141289400041472) << 15) | ((position_piece & 141289400041472) << 6)
        caval_B = ((position_piece & 70644700020736) >> 17) | ((position_piece & 70644700020736) >> 10) | ((position_piece & 70644700020736) << 15) | ((position_piece & 70644700020736) << 6) | ((position_piece & 70644700020736) >> 15) | ((position_piece & 70644700020736) << 17)
        caval_G = ((position_piece & 2207646875648) >> 17) | ((position_piece & 2207646875648) << 10) | ((position_piece & 2207646875648) << 15) | ((position_piece & 2207646875648) >> 6) | ((position_piece & 2207646875648) >> 15) | ((position_piece & 2207646875648) << 17)
        caval_H = ((position_piece & 1103823437824) << 10) | ((position_piece & 1103823437824) >> 6) | ((position_piece & 1103823437824) >> 15) | ((position_piece & 1103823437824) << 17)
        caval_A1 = ((position_piece & 9223372036854775808) >> 17) | ((position_piece & 9223372036854775808) >> 10)
        caval_B1 = ((position_piece & 4611686018427387904) >> 17) | ((position_piece & 4611686018427387904) >> 15) | ((position_piece & 4611686018427387904) >> 10)
        caval_G1 = ((position_piece & 144115188075855872) >> 17) | ((position_piece & 144115188075855872) >> 15) | ((position_piece & 144115188075855872) >> 6)
        caval_H1 = ((position_piece & 72057594037927936) >> 6) | ((position_piece & 72057594037927936) >> 15)
        caval_A2 = ((position_piece & 36028797018963968) >> 17) | ((position_piece & 36028797018963968) >> 10) | ((position_piece & 36028797018963968) << 6)
        caval_B2 = ((position_piece & 18014398509481984) >> 17) | ((position_piece & 18014398509481984) >> 15) | ((position_piece & 18014398509481984) >> 10) | ((position_piece & 18014398509481984) << 6)
        caval_G2 = ((position_piece & 562949953421312) >> 17) | ((position_piece & 562949953421312) >> 15) | ((position_piece & 562949953421312) << 10) | ((position_piece & 562949953421312) >> 6)
        caval_H2 = ((position_piece & 281474976710656) >> 6) | ((position_piece & 281474976710656) >> 15) | ((position_piece & 281474976710656) << 10)
        caval_A7 = ((position_piece & 32768) << 6) | ((position_piece & 32768) << 15) | ((position_piece & 32768) >> 10)
        caval_B7 = ((position_piece & 16384) << 17) | ((position_piece & 16384) << 15) | ((position_piece & 16384) >> 10) | ((position_piece & 16384) << 6)
        caval_G7 = ((position_piece & 512) << 17) | ((position_piece & 512) << 15) | ((position_piece & 512) << 10) | ((position_piece & 512) >> 6)
        caval_H7 = ((position_piece & 256) << 17) | ((position_piece & 256) >> 6) | ((position_piece & 256) << 10)
        caval_A8 = ((position_piece & 128) << 6) | ((position_piece & 128) << 15)
        caval_B8 = ((position_piece & 64) << 17) | ((position_piece & 64) << 15) | ((position_piece & 64) << 6)
        caval_G8 = ((position_piece & 2) << 17) | ((position_piece & 2) << 15) | ((position_piece & 2) << 10)
        caval_H8 = ((position_piece & 1) << 17) | ((position_piece & 1) << 10)
        position_piece = caval_centre | caval_A | caval_B | caval_G | caval_H | caval_1 | caval_2 | caval_7 | caval_8 | caval_A1 | caval_A2 | caval_A7 | caval_A8 | caval_B1 | caval_B2 | caval_B7 | caval_B8 | caval_G1 | caval_G2 | caval_G7 | caval_G8 | caval_H1 | caval_H2 | caval_H7 | caval_H8
        if not manger :
            position_piece &= ~position_noir
        return position_piece
    elif piece_index == 8:
        pieces_pos = decomposition_position(position_piece)
        union_pos_piece = 0
        for pos_piece in pieces_pos:
            indices = indices_binaire(pos_piece)
            copie_position1,copie_position2,copie_position3,copie_position4 = pos_piece,pos_piece,pos_piece,pos_piece
            i1,i2,i3,i4,j1,j2,j3,j4 = indices[0],indices[0],indices[0],indices[0],indices[1],indices[1],indices[1],indices[1]
            while (copie_position1 & (position_tot & ~pos_piece)) == 0 and i1<7 and j1<7:
                i1+=1
                j1+=1
                copie_position1 |= copie_position1 >> 9
            while (copie_position2 & (position_tot & ~pos_piece)) == 0 and i2<7 and j2>0:
                i2+=1
                j2-=1
                copie_position2 |= copie_position2 >> 7
            while (copie_position3 & (position_tot & ~pos_piece)) == 0 and i3>0 and j3<7:
                i3-=1
                j3+=1
                copie_position3 |= copie_position3 << 7
            while (copie_position4 & (position_tot & ~pos_piece)) == 0 and i4>0 and j4>0:
                i4-=1
                j4-=1
                copie_position4 |= copie_position4 << 9
            union_pos_piece |= copie_position1 | copie_position2 | copie_position3 | copie_position4
        if not manger :
            union_pos_piece &= ~position_noir
        else :
            union_pos_piece &= ~position_piece
        return union_pos_piece
    elif piece_index == 7:
        pieces_pos = decomposition_position(position_piece)
        union_pos_piece = 0
        for pos_piece in pieces_pos:
            indices = indices_binaire(pos_piece)
            copie_position1,copie_position2,copie_position3,copie_position4 = pos_piece,pos_piece,pos_piece,pos_piece
            i1,i2,j1,j2 = indices[0],indices[0],indices[1],indices[1]
            while (copie_position1 & (position_tot & ~pos_piece)) == 0 and i1<7:
                i1+=1
                copie_position1 |= copie_position1 >> 8
            while (copie_position2 & (position_tot & ~pos_piece)) == 0 and i2>0:
                i2-=1
                copie_position2 |= copie_position2 << 8
            while (copie_position3 & (position_tot & ~pos_piece)) == 0 and j1<7:
                j1+=1
                copie_position3 |= copie_position3 >> 1
            while (copie_position4 & (position_tot & ~pos_piece)) == 0 and j2>0:
                j2-=1
                copie_position4 |= copie_position4 << 1
            union_pos_piece |= copie_position1 | copie_position2 | copie_position3 | copie_position4
        if not manger:
            union_pos_piece &= ~position_noir
        else :
            union_pos_piece &= ~position_piece
        return union_pos_piece
    elif piece_index == 6:
        pieces_pos = decomposition_position(position_piece)
        union_pos_piece = 0
        for pos_piece in pieces_pos:
            indices = indices_binaire(pos_piece)
            copie_position1,copie_position2,copie_position3,copie_position4,copie_position5,copie_position6,copie_position7,copie_position8 = pos_piece,pos_piece,pos_piece,pos_piece,pos_piece,pos_piece,pos_piece,pos_piece
            i1,i2,i3,i4,i5,i6,j1,j2,j3,j4,j5,j6=indices[0],indices[0],indices[0],indices[0],indices[0],indices[0],indices[1],indices[1],indices[1],indices[1],indices[1],indices[1]
            while (copie_position1 & (position_tot & ~pos_piece)) == 0 and i1 < 7 and j1 < 7:
                i1+=1
                j1+=1
                copie_position1 |= copie_position1 >> 9
            while (copie_position2 & (position_tot & ~pos_piece)) == 0 and i2 < 7 and j2 > 0:
                i2+=1
                j2-=1
                copie_position2 |= copie_position2 >> 7
            while (copie_position3 & (position_tot & ~pos_piece)) == 0 and i3 > 0 and j3 < 7:
                i3-=1
                j3+=1
                copie_position3 |= copie_position3 << 7
            while (copie_position4 & (position_tot & ~pos_piece)) == 0 and i4 > 0 and j4 > 0:
                i4-=1
                j4-=1
                copie_position4 |= copie_position4 << 9
            while (copie_position5 & (position_tot & ~pos_piece)) == 0 and i5<7:
                i5+=1
                copie_position5 |= copie_position5 >> 8
            while (copie_position6 & (position_tot & ~pos_piece)) == 0 and i6>0:
                i6-=1
                copie_position6 |= copie_position6 << 8
            while (copie_position7 & (position_tot & ~pos_piece)) == 0 and j5<7:
                j5+=1
                copie_position7 |= copie_position7 >> 1
            while (copie_position8 & (position_tot & ~pos_piece)) == 0 and j6>0:
                j6-=1
                copie_position8 |= copie_position8 << 1
            union_pos_piece |= copie_position1 | copie_position2 | copie_position3 | copie_position4 | copie_position5 | copie_position6 | copie_position7 | copie_position8
        if not manger:
            union_pos_piece &= ~position_noir
        else:
            union_pos_piece &= ~position_piece
        return union_pos_piece

def coups_piece_tri(position,position_piece,piece_index,couleur,prise): # enleve tous les coups inutiles d'une piece (en prise par une piece de plus faible valeur)
    coups_piece_brut = coups_piece(position,position_piece,piece_index,False)
    coups_piece_trie = coups_piece_brut
    cases_controlees = 0
    cases_necessaires = 0
    pieces_inf = tab_pieces_inf_sup[piece_index][0]
    pieces_sup = tab_pieces_inf_sup[piece_index][1]
    if piece_index==5:
        for elt in pieces_inf:
            cases_controlees |= coups_piece(position,position[elt],elt,True)
        cases_controlees |= coups_piece(position, position[11], 11, True)
        coups_piece_trie &= ~cases_controlees
        if position[15] and (cases_controlees & (position_piece | 288230376151711744)):
            coups_piece_trie &= ~144115188075855872
        if position[16] and (cases_controlees & (position_piece | 1152921504606846976)):
            coups_piece_trie &= ~2305843009213693952
    elif piece_index == 11:
        for elt in pieces_inf:
            cases_controlees |= coups_piece(position,position[elt],elt,True)
        cases_controlees |= coups_piece(position, position[5], 5, True)
        coups_piece_trie &= ~cases_controlees
        if position[17] and (cases_controlees & (position_piece | 4)):
            coups_piece_trie &= ~2
        if position[18] and (cases_controlees & (position_piece | 16)):
            coups_piece_trie &= ~32
    else :
        if not endgame:
            for elt in pieces_inf:
                if position[elt] != 0:
                    cases_controlees |= coups_piece(position,position[elt],elt,True)
            for elt in pieces_sup:
                cases_necessaires |= position[elt]
            if couleur == 12:
                cases_necessaires |= (position[10] & 18446742974197923840)
            if couleur == 13:
                cases_necessaires |= (position[4] & 16777215)
            coups_piece_trie &= (~(cases_controlees & ~cases_necessaires))
        if couleur == 12 and prise :
            coups_piece_trie &= position[13]
            if piece_index == 4:
                coups_piece_trie |= (coups_piece_brut & 65535)
        elif couleur == 13 and prise :
            coups_piece_trie &= position[12]
            if piece_index == 10:
                coups_piece_trie |= (coups_piece_brut & 18446462598732840960)
    return coups_piece_trie

def coups_possibles(position,couleur,prise): #return tous les coups possibles (triés) d'une position pour une couleur donnée sous la forme d'une liste de listes avec comme premier element la piece en question puis des couples [case de départ,case d'arrivée]
    coups_possibles = []
    if couleur == 12 :
        for i in range(6):
            coups_possibles_piece = [i]
            position_piece = position[i]
            position_unites_piece = decomposition_position(position_piece)
            for elt in position_unites_piece:
                coups_piece = coups_piece_tri(position,elt,i,couleur,prise)
                coups_piece_unite = decomposition_position(coups_piece)
                for coup in coups_piece_unite:
                    coups_possibles_piece.append([elt,coup])
            coups_possibles.append(coups_possibles_piece)
    elif couleur == 13 :
        for i in range(6,12):
            coups_possibles_piece = [i]
            position_piece = position[i]
            position_unites_piece = decomposition_position(position_piece)
            for elt in position_unites_piece:
                coups_piece = coups_piece_tri(position, elt, i,couleur,prise)
                coups_piece_unite = decomposition_position(coups_piece)
                for coup in coups_piece_unite:
                    coups_possibles_piece.append([elt, coup])
            coups_possibles.append(coups_possibles_piece)
    return coups_possibles

def decomposition_position(position_piece): # prend une position et return une liste des positions individuelles
    L=[]
    for i in range(64):
        r = position_piece%2
        if r :
            L.append(2**i)
        position_piece//=2
        if position_piece == 0:
            break
    return L


def indices_binaire(case): #converti le binaire d'une case en son indice
    L=[]
    for i in range(64):
        case%2
        if case%2 :
            L.append(7 - (i // 8))
            L.append(7 -  (i% 8))
            break
        case//=2
    return L

def binaire_indice(indice): #converti un indice de case en binaire
    numero = indice[0]*8+indice[1]
    bin = '1' + (63 - numero)*'0'
    return int(bin,2)

def visualiser_position(position): #permet de print une position
    L = []
    L2 = []
    for i in range(64):
        r = position % 2
        if r:
            L.append(1)
        else :
            L.append(0)
        position //= 2
    for n in range(8):
        L3 = L[8*n:8*(n+1)]
        L3.reverse()
        L2.append(L3)
    for elt in L2:
        print(elt)

def piece_couleur_case(position,case): # return couple [couleur,piece_index] pour une case donnée
    if not(position[-1] & case):
        return
    elif position[12] & case :
        for i in range(6):
            if position[i] & case :
                return [12,i]
    elif position[13] & case :
        for i in range(6,12):
            if position[i] & case :
                return [13,i]

def creer_position_fils(position,coup,piece_index,indice_cases,couleur):
    position_fils = position.copy()
    position_fils[19] = [0,0] #reinitialiser droits en passant
    if (coup[0] & 65280) and piece_index==4: #promotion dame blanc
        adv_case_arrivee = piece_couleur_case(position, coup[1])
        if adv_case_arrivee:
            position_fils[adv_case_arrivee[1]] &= ~coup[1]
            position_fils[adv_case_arrivee[0]] &= ~coup[1]
            position_fils[14] ^= tab_zobrist[indice_cases[1][0]][indice_cases[1][1]][adv_case_arrivee[1]]
        position_fils[piece_index] &= ~coup[0]
        position_fils[couleur] &= ~coup[0]
        position_fils[-1] &= ~coup[0]
        position_fils[0] |= coup[1]
        position_fils[couleur] |= coup[1]
        position_fils[-1] |= coup[1]
        position_fils[14] ^= tab_zobrist[indice_cases[0][0]][indice_cases[0][1]][piece_index] ^ tab_zobrist[indice_cases[1][0]][indice_cases[1][1]][0]
    elif (coup[0] & 71776119061217280) and piece_index == 10: #promotion dame noir
        adv_case_arrivee = piece_couleur_case(position, coup[1])
        if adv_case_arrivee:
            position_fils[adv_case_arrivee[1]] &= ~coup[1]
            position_fils[adv_case_arrivee[0]] &= ~coup[1]
            position_fils[14] ^= tab_zobrist[indice_cases[1][0]][indice_cases[1][1]][adv_case_arrivee[1]]
        position_fils[piece_index] &= ~coup[0]
        position_fils[couleur] &= ~coup[0]
        position_fils[-1] &= ~coup[0]
        position_fils[6] |= coup[1]
        position_fils[couleur] |= coup[1]
        position_fils[-1] |= coup[1]
        position_fils[14] ^= tab_zobrist[indice_cases[0][0]][indice_cases[0][1]][piece_index] ^ tab_zobrist[indice_cases[1][0]][indice_cases[1][1]][0]
    else:
        if couleur == 12: #modifier droits rock/en passant blanc
            if coup[0] == 576460752303423488:
                position_fils[15], position_fils[16] = False, False
            elif coup[0] == 72057594037927936:
                position_fils[15] = False
            elif coup[0] == 9223372036854775808:
                position_fils[16] = False
            if piece_index == 4 and (coup[0] & 71776119061217280) and (coup[1] & 1095216660480):
                position_fils[19][0] = coup[0] >> 8
        elif couleur == 13: #modifier droits rock/en passant noir
            if coup[0] == 8:
                position_fils[17], position_fils[18] = False, False
            elif coup[0] == 1:
                position_fils[17] = False
            elif coup[0] == 128:
                position_fils[18] = False
            if piece_index == 10 and (coup[0] & 65280) and (coup[1] & 4278190080):
                position_fils[19][1] = coup[0] << 8
        adv_case_arrivee = piece_couleur_case(position,coup[1])
        if adv_case_arrivee: # manger piece adv
            position_fils[adv_case_arrivee[1]] &= ~coup[1]
            position_fils[adv_case_arrivee[0]] &= ~coup[1]
            position_fils[14] ^= tab_zobrist[indice_cases[1][0]][indice_cases[1][1]][adv_case_arrivee[1]]
        elif piece_index == 4 and indice_cases[0][1] != indice_cases[1][1] and not adv_case_arrivee: # prise en passant blanc
            case_en_passant = coup[1] << 8
            position_fils[10] &= ~case_en_passant
            position_fils[13] &= ~case_en_passant
            position_fils[-1] &= ~case_en_passant
            position_fils[14] ^= tab_zobrist[indice_cases[1][0]-1][indice_cases[1][1]][10]
        elif piece_index == 10 and indice_cases[0][1] != indice_cases[1][1] and not adv_case_arrivee: # prise en passant noir
            case_en_passant = coup[1] >> 8
            position_fils[4] &= ~case_en_passant
            position_fils[12] &= ~case_en_passant
            position_fils[-1] &= ~case_en_passant
            position_fils[14] ^= tab_zobrist[indice_cases[1][0]+1][indice_cases[1][1]][10]
        position_fils[piece_index] &= ~coup[0]
        position_fils[couleur] &= ~coup[0]
        position_fils[-1] &= ~coup[0]
        position_fils[piece_index] |= coup[1]
        position_fils[couleur] |= coup[1]
        position_fils[-1] |= coup[1]
        position_fils[14] ^= tab_zobrist[indice_cases[0][0]][indice_cases[0][1]][piece_index] ^ tab_zobrist[indice_cases[1][0]][indice_cases[1][1]][piece_index]
        if indice_cases == [[0,4],[0,6]] and piece_index == 5 : #petit rock blanc
            position_fils[1] &= ~72057594037927936
            position_fils[12] &= ~72057594037927936
            position_fils[-1] &= ~72057594037927936
            position_fils[1] |= 288230376151711744
            position_fils[12] |= 288230376151711744
            position_fils[-1] |= 288230376151711744
            position_fils[14] ^= tab_zobrist[0][7][1] ^ tab_zobrist[0][5][1]
        elif indice_cases == [[0, 4], [0, 2]] and piece_index == 5: #grand rock blanc
            position_fils[1] &= ~9223372036854775808
            position_fils[12] &= ~9223372036854775808
            position_fils[-1] &= ~9223372036854775808
            position_fils[1] |= 1152921504606846976
            position_fils[12] |= 1152921504606846976
            position_fils[-1] |= 1152921504606846976
            position_fils[14] ^= tab_zobrist[0][0][1] ^ tab_zobrist[0][3][1]
        elif indice_cases == [[7, 4], [7, 6]] and piece_index == 11: #petit rock noir
            position_fils[7] &= ~1
            position_fils[13] &= ~1
            position_fils[-1] &= ~1
            position_fils[7] |= 4
            position_fils[13] |= 4
            position_fils[-1] |= 4
            position_fils[14] ^= tab_zobrist[7][7][7] ^ tab_zobrist[7][5][7]
        elif indice_cases == [[7, 4], [7, 2]] and piece_index == 11: #grand rock noir
            position_fils[7] &= ~128
            position_fils[13] &= ~128
            position_fils[-1] &= ~128
            position_fils[7] |= 16
            position_fils[13] |= 16
            position_fils[-1] |= 16
            position_fils[14] ^= tab_zobrist[7][0][7] ^ tab_zobrist[7][3][7]
    return position_fils

def echiquier_gen(echiquier): #permet de creer les echiquier blanc/noir et total
    echiquier_blanc = 0
    echiquier_noir = 0
    for k in range(6):
        echiquier_blanc |= echiquier[k]
    for l in range(6,12):
        echiquier_noir |= echiquier[l]
    echiquier_tot = echiquier_blanc | echiquier_noir
    return [echiquier_blanc,echiquier_noir,echiquier_tot]

def evaluation(position): #fonction d'evaluation d'une position pour l'IA
    evaluation = 0
    for k in range(6):
        bin_piece = bin(position[k])[2:]
        taille = len(bin_piece)
        num_dep = 64 - taille
        for binary in bin_piece:
            if int(binary):
                evaluation += valeurs[k] + tab_valeurs_ponderees[k][num_dep]
            num_dep+=1
    for l in range(6,12):
        bin_piece = bin(position[l])[2:]
        taille = len(bin_piece)
        num_dep = 64 - taille
        for binary in bin_piece:
            if int(binary):
                evaluation -= (valeurs[l] + tab_valeurs_ponderees[l][num_dep])
            num_dep += 1
    pions_blanc = []
    pions_noir = []
    for elt in tab_colonnes:
        pion_blanc_colonne = elt & position[4]
        pion_noir_colonne = elt & position[10]
        pions_blanc.append(bin(pion_blanc_colonne).count('1'))
        pions_noir.append(bin(pion_noir_colonne).count('1'))
    for m in range(8):
        if pions_blanc[m]:
            pions_blanc_colonne = pions_blanc[m]
            evaluation -= (pions_blanc_colonne-1)*40 #pions doublés blanc
            try :
                pion_avant_blanc = pions_blanc[m-1]
            except:
                pion_avant_blanc = 0
            try :
                pion_après_blanc = pions_blanc[m+1]
            except :
                pion_après_blanc = 0
            if pion_avant_blanc == 0 and pion_après_blanc == 0:
                evaluation -= (pions_blanc_colonne)*40 #pions isolés blanc
        if pions_noir[m]:
            pions_noir_colonne = pions_noir[m]
            evaluation += (pions_noir_colonne-1)*40 #pions doublés noir
            try :
                pion_avant_noir = pions_noir[m-1]
            except:
                pion_avant_noir = 0
            try :
                pion_après_noir = pions_noir[m+1]
            except :
                pion_après_noir = 0
            if pion_avant_noir == 0 and pion_après_noir == 0:
                evaluation += (pions_noir_colonne)*40 #pions isolés noir
    if couleur_IA == 13:
        evaluation *= -1
    return evaluation


def minimax(position,profondeur,joueur,alpha,beta): #creer l'arbre des possibilités pour ressortir la meilleure variante
    global a
    global b
    global c
    if profondeur==prf: #evaluer la position une fois arrivé à la profondeur maximale
        if partie.count(position) == 2:
            evaluation_position = 0
        elif position[14] in transposition_table_evaluations:
            a+=1
            evaluation_position = transposition_table_evaluations[position[14]]
        else :
            evaluation_position = evaluation(position)
            transposition_table_evaluations[position[14]]=evaluation_position
        return [evaluation_position]
    elif joueur == 'IA': # joueur IA donc choisi l'evaluation maximale de ses positions fils
        if profondeur < prf-prof_prise:
            coups_possible = coups_possibles(position,couleur_IA,False)
        else :
            coups_possible = coups_possibles(position,couleur_IA,True)
        best = [MIN]
        stop = False
        for coup_pieces in coups_possible:
            if stop:
                break
            for coup in coup_pieces[1:] :
                indices_cases = [indices_binaire(coup[0]),indices_binaire(coup[1])]
                position_fils = creer_position_fils(position,coup,coup_pieces[0],indices_cases,couleur_IA)
                if partie.count(position_fils) == 2:
                    minimax_fils = [0]
                elif position_fils[14] in transposition_table_positions:
                    b+=1
                    minimax_fils = transposition_table_positions[position_fils[14]]
                elif (position_fils[5] == 0 and couleur_IA == 12) or (position_fils[11] == 0 and couleur_IA == 13): #si on perd le roi inutile de continuer l'analyse plus loin
                    minimax_fils = [MIN]
                else :
                    minimax_fils = minimax(position_fils,profondeur+1,'ADV',alpha,beta)
                    if profondeur == 0:
                        transposition_table_positions[position_fils[14]]=minimax_fils
                if minimax_fils[0] > best[0]: #on garde en memoire le meilleur coup pour l'instant
                    best = minimax_fils.copy()
                    best.append(coup)
                alpha = max(alpha,best[0])
                if beta <= alpha : #si la branche est inutile (noeud actuel maximal, donc père minimal. Si frère plus faible qu'un des fils, inutile de continuer plus loin)
                    stop = True
                    break
        return best
    else : # joueur adverse donc choisi l'evaluation minimale de ses position fils
        if profondeur < prf-prof_prise:
            coups_possible = coups_possibles(position,couleur_ADV,False)
        else :
            coups_possible = coups_possibles(position,couleur_ADV,True)
        best = [MAX]
        stop = False
        for coup_pieces in coups_possible:
            if stop:
                break
            for coup in coup_pieces[1:]:
                indices_cases = [indices_binaire(coup[0]), indices_binaire(coup[1])]
                position_fils = creer_position_fils(position, coup, coup_pieces[0], indices_cases, couleur_ADV)
                if position_fils[14] in transposition_table_positions:
                    c+=1
                    minimax_fils = transposition_table_positions[position_fils[14]]
                elif (position_fils[5] == 0 and couleur_ADV == 12) or (position_fils[11] == 0 and couleur_ADV == 13): #si on perd le roi inutile de continuer l'analyse plus loin
                    minimax_fils = [MAX]
                else:
                    minimax_fils = minimax(position_fils, profondeur + 1, 'IA', alpha, beta)
                if minimax_fils[0] < best[0]: #on garde en memoire le meilleur coup pour l'instant
                    best = minimax_fils.copy()
                    best.append(coup)
                beta = min(beta, best[0])
                if beta <= alpha: #si la branche est inutile (noeud actuel minimal, donc père maximal. Si frère plus grand qu'un des fils, inutile de continuer plus loin)
                    stop = True
                    break
        return best


tab_pieces_inf_sup = [[[7,8,9,10],[6,11]],[[8,9,10],[6,7,11]],[[10],[6,7,8,9,11]],[[10],[6,7,8,9,11]],[[],[]],[[6,7,8,9,10],[]],[[1,2,3,4],[0,5]],[[2,3,4],[0,1,5]],[[4],[0,1,2,3,5]],[[4],[0,1,2,3,5]],[[],[]],[[0,1,2,3,4],[]]] #tableau donnant pour chaque piece (index) la liste des pieces plus faibles/fortes
tab_zobrist = [[[13228706764895879793, 8984491559086771384, 6979060087885526202, 18260143982251475200, 15125343188630121173, 11269822408121749618, 15565617085852638756, 4324145492661210523, 11251179921122579808, 10749806763240217829, 14774122563240995513, 13773068453080163893], [11727982049646151932, 6461960238993556636, 12576978491271331596, 2658941250482349446, 7245097322227312755, 13399265617691759448, 9210860369710111552, 14565655338027010297, 2638886551151351649, 11453978754968078478, 7712651797614008260, 12260235071775251100], [1851628504164588211, 11684678723757251485, 10421305839825820456, 3945233404475073183, 8959567885221323195, 10803827928141618220, 3451358244955029753, 15080788761837768057, 6482241775383190134, 2736469919737792105, 13287508885776053484, 351084104237650806], [5153309343699142620, 6464644825809770511, 6997777757664674479, 14055699748453499674, 17554969204750021093, 675953289282839563, 10277064133086042063, 13568707521188435965, 17866300834531377158, 6129813253235103821, 13266040424644678685, 17718925657332933347], [7269042161679262567, 8383149115264724174, 4645387231939990036, 13056536950291024550, 9893970243275035442, 8948371763614026228, 6312606962268507974, 17554166852876612679, 16068190351629520392, 5945989128526726403, 17106071629244468833, 1202915578495160916], [8307416871152667699, 4001419497763176665, 13516742623444227066, 10785226943313243733, 16757191110353008977, 14061061034519139726, 374972113343186947, 1244451447890339955, 11371119022907725843, 8020709600187273843, 5140298984917025061, 1017774658158993531], [7110819911346684931, 11325428078667855222, 8331844472321278546, 3677138542355972206, 2660176084860468487, 13517999134550448241, 1938700120990459137, 1055179498251555060, 17122963018582503021, 122748134406593517, 4165283083442464066, 9110063920389639760], [6567248712679324953, 13322853734529734970, 17601239551380049686, 13043928769974528250, 8589527812399578654, 12333136525340780376, 18310404094567832448, 15239802391628334965, 6479582143974381494, 5445507071191863306, 8746876120029909803, 14477234524491581076]], [[10875819605531892847, 12881834378527516403, 18391627319899619514, 5443005962498606960, 2286153374972925838, 11829971515707572252, 13278548260515326627, 9797131015958984511, 3259189469358175833, 4534043837357448435, 18390317172004036713, 12180283624807989762], [1793675074558570040, 14548709261630924162, 1762035079804536630, 9898891246785247795, 3978540658940505548, 11321622415321892857, 17438095719774880101, 17599646362857855477, 18168882710560922406, 1781576416541835602, 9199421080488849335, 12539394459819849628], [16405456089017097205, 5873580735165044472, 8920177091160159182, 12217045074786077226, 7176886755989860633, 6737864224234307128, 3329830790523366097, 11824946315232464793, 15788449723313497800, 17156586852093372285, 6347429245161049228, 13825870118587164336], [7609495100531422038, 7824919433022853439, 5057202417113751605, 701228179286304098, 1974347959925989848, 8694150741689072587, 11968772985514313783, 902640299481568228, 10284406970570118090, 1578592159012898324, 14390775360995054353, 17340184760146089616], [5066712544171951352, 4014842225091890408, 12275384315737322474, 8539288535468179350, 16387388371337330553, 4120494596300230959, 16327771173903523590, 13291388402921207840, 3425151381117997098, 17134585283392751048, 1832149039696411287, 15673170066481550339], [1861386048681290530, 6885088094736926356, 16803296418248466425, 12582113086988204769, 17807967345181463985, 14677623367280707789, 11616154852821137510, 5450769574970226255, 9711265247420622035, 796175102665307195, 10356707462132394631, 15912111304711516304], [16329432993763753272, 6288052657529367076, 10640829798675368788, 11967809930653283176, 15784301932909623028, 3519871067786182792, 4703702749542760601, 119609902657359300, 3039616674327331740, 14516666052367942433, 14793652102410775326, 2824463727394254058], [15795118916355128273, 9606005461553018563, 4191996103603974319, 2731075896071120249, 17436291089397460299, 7403541729305668156, 9913327447398952649, 7347304758818455559, 5632182512080406330, 16142330521037674314, 2601393210299213705, 1262771170064759232]], [[14831523968032361714, 4764384581209922302, 6092319800022013619, 12341710429843731681, 309210666093478171, 9904010049511336507, 3091384538111848670, 7433906155311527938, 15606242795797429890, 12710742186210453559, 15755332045706161699, 7799039243801335241], [16738345189764386167, 5822520880149274494, 13334377547503206975, 1903454178309661423, 16123487215782015817, 5359966801752849913, 9289766673546178102, 13491187293984873779, 1707529011109171523, 2544046286884227754, 3767794180662995605, 15071328737021858639], [17277620082602921560, 17041407274483195659, 3617116009516557825, 10910962935689488396, 3168361860167114656, 6295240609139181305, 13989076785718853781, 15368234549935341429, 15231701045570039241, 15965133791828887406, 3832131301873407362, 4610626034135791312], [1598533229385670893, 3631694533211079600, 16324021105431036275, 7752695664307017716, 851729734909516041, 6250735142961568235, 4569241416295350311, 10976527350003315478, 5442426681312111229, 5768457290772417889, 17386856114274033912, 14198629936205093606], [8277506430510783666, 10941952159494709911, 18023235210082880664, 2489329565837663158, 2599598860000550682, 7120179699283282075, 3800095040612912321, 15764018865620623010, 3157666092907491541, 1014014665083908847, 13110023422675901989, 189416031533488734], [4434069431548890769, 17874764366297174344, 12506244684081843745, 2403860564493867741, 152140698585418646, 13040233359092463446, 11773926369897105036, 16215779218810832861, 15243573942591668308, 10936198580118984668, 15298711017462244029, 9407113940539783946], [5999236170909844301, 2758305812208055184, 1951918561219874036, 13459517525358696108, 16288105741903224585, 10761269037153703059, 3824757240341077421, 9459806980964652398, 5907425684078735267, 4338807848276612880, 10050439044638041376, 8254388074789506631], [5286543289136675086, 15813198515831207395, 1187888900550820499, 12339669024463822249, 2411371496200191818, 11344598727837173140, 4071262592726142951, 49650081573621768, 3991294328560722354, 10308175470610918902, 9490658109350775056, 3185209264548820558]], [[695602873794928823, 7823382147047395114, 14241523974707480403, 2739523848160824309, 12223101288467109610, 14950464090108443666, 11548962389100619972, 9241830183600326492, 18380822572658637138, 12001615217962769709, 17808620119470790123, 5353628368389445101], [15817575218253079921, 2466552588690804278, 12073358015525441159, 18134865885209521671, 544896979846155266, 17943606838461426689, 5682148940902723547, 10870728973418530639, 13751792311693384621, 12797154081293054836, 9193570712997972751, 17943388010140663245], [9780319568342259832, 10437180861894557967, 6919130580270056481, 10180967774664424743, 16203284581598923351, 13014464278310021653, 6863343442376497315, 16851050614820528396, 5863980819145790223, 8405371091376178331, 17971473002459056446, 13088912132003197223], [9211403276725425523, 7200298949096423691, 12435193126905421601, 8766235815157641886, 6343543279363953913, 1735974828489551126, 16640584749757242609, 15034687377085241939, 2141059448064648213, 2209123878749227428, 1292426370966981002, 6865401559426708993], [1262472348061858522, 18062247476906796879, 2437744320750102839, 11208849180596637060, 15573412925704830737, 17401342916424286360, 7250897114980697840, 6106770416341153627, 11919534130900388660, 5331488321374935469, 17042783183846094505, 7132066268290978140], [7218638727080242083, 2294364850913942898, 15262487434859858367, 12138005123407383522, 12137549357994096857, 11610219014056425976, 16436988951184618547, 7640926989396169695, 5122631198007266190, 11480579983444727674, 7860249044207403030, 10653785673122900690], [11066372407118282689, 5214115267275237556, 13639293219203898342, 14582550442456539647, 17213610491910140103, 18229615407050793032, 10184293491932785348, 16640503941757794095, 3463831729567165218, 3885140193535752875, 14989479096900312315, 13129124653455930800], [4842820724734151213, 15924500571149641570, 16715495689584832859, 16583004676535676582, 14795591685062317094, 18005003785964857457, 8033792528266411271, 14818928244795459273, 12424910167435243566, 12617112522535866291, 5500833144971949322, 11414231623146880579]], [[15948611625961296619, 13889781304309542222, 14605607287552345728, 2329417484198105187, 3251100776011765706, 14466364292980518269, 11893013580284369351, 6822264195283031805, 13408763499209624568, 8106520361321542281, 11624714577989917463, 14089279054936151853], [13179040586757601970, 18378374630100011711, 13366231449042640746, 4740889720636258916, 8354262057303726797, 16272851517487451220, 15764221672536390218, 14859123110628566376, 17026463397458978683, 3443603882495821730, 1147689893671729409, 15135286414034600764], [12949778888270135925, 12777219109130216083, 16955380585814103833, 17106040748726792610, 18417723610790984964, 3946268943884736986, 7200354966229333164, 17691434776919319428, 1744368720829333436, 16608587524167845667, 17752493087660528719, 15316096663824218686], [17566642197574669433, 16436124726542100850, 15896965394047129338, 16208653448299607505, 16838118166334439450, 13221621176945891806, 5440275306828696026, 18014851847112701905, 9306859533996691790, 2112627315113237019, 7910786336737158691, 13069542169725324245], [9855773757026190974, 17342883322672609982, 1224216536679763728, 15212211829581196226, 9535977450799965281, 9565714907797000510, 710644045077254166, 10480501118933382019, 17051480957876116170, 5186466892917612398, 14292742956308360397, 3356113913928277958], [15995678752561909619, 11936093957910669040, 16516454029154149134, 14449995875241464748, 5681869907217269076, 1781958705256395295, 10370292217874096341, 1165325883975743783, 2618007982201222205, 14741331768055624318, 18113217959325089785, 14095211485266806757], [9676202810019444622, 8022044612175895775, 1704680411749670005, 6574857048390466115, 3915678927558201561, 3914014999404132204, 10092820163622630516, 12275365564262481352, 11913673561552804840, 13170227622076379721, 3432413443140733412, 17165128917453064870], [3010738326877268157, 1463296740409522100, 585819371194208801, 16344162924313292559, 16430333934348771189, 13005984751626401653, 13705655924917573610, 4478024771903160124, 7618357315214007762, 14996345354316050340, 14771871553020672540, 971709252776540184]], [[4937135398182580666, 17986945244951170333, 2487129235296867990, 15979140709268653499, 3897487206609969449, 13612396236908224299, 14468516094342360610, 12745677508632419842, 10722351005836221486, 8878346169744514889, 8591800726921335062, 5420904088285775448], [10767582494528772282, 2227088195370666643, 15575492087744866884, 10951495695107266886, 14247888370950604400, 3806160151024686226, 10395838898091828658, 8202965953051070313, 4773561486313910605, 2898338895764760252, 8657580944087919971, 1730581381441759195], [15404830355045490942, 9757848308635767896, 16246349574504327564, 17739508100331179607, 2100530845383463555, 8428544846722942307, 17989866497881777388, 6942307637742011228, 17493827487901511527, 8439453270689635073, 13612975878921785337, 12575750693983927323], [4868429759595039204, 9458613001765492637, 12611323946162655746, 1465467514154410111, 4266013948898456520, 1090946694088739453, 12184249385953309914, 7819660462871896169, 2147484190858091104, 2528553772172916335, 3907549439729959577, 10006010139408964974], [17092194474970504997, 2438434773120176760, 16471817668133176184, 9406858171444640329, 8617623030883894692, 14352914839413716820, 18111594029046466419, 3059692901310965726, 6988999698156956161, 18196999846180087935, 11031454060555981334, 12098654934755209856], [13358422592678516172, 14060976701541742497, 9530645587232103969, 10485803239668414700, 15399979418227289253, 16865322852400473166, 4050431578859868551, 14166923222197194496, 3594210172085806399, 4452223987235873474, 17140203612177915311, 11078522604030292625], [15953053449037059056, 8916245755856997925, 6297624478371715908, 2263430096116463669, 2919149374672530802, 15751948927366079758, 13282484625333560187, 125426629765319029, 439304205896839023, 6510861772002586587, 10964694982692016143, 8434681705651144383], [16526164959679711687, 17509808225570082079, 7447967806233747235, 17170547734925850781, 7533801603654485891, 295984251535772473, 15687530315636355127, 2262750977641985259, 14036595119423047173, 11938422380513567497, 16672912524512456002, 6835868929170420500]], [[1418231499479860459, 17299739933090247483, 11761359639032679886, 13193954573586890174, 14741936457481825534, 17539740878345144502, 6809353685781784679, 3595265297243068014, 6417607337382206828, 9038345237730696086, 17833797907851177262, 10814490609957220601], [14867941682067993507, 18291920244984832655, 14506471016171511737, 11785162471002032029, 1246589912383365960, 1734800640649306789, 15979235655921800699, 15068563494747665888, 13591900309620659137, 1649087538664967070, 9692115568991415063, 17794247677580784358], [8639192293326608549, 4066384536622807270, 6135199275461715886, 18040285057317667516, 3868647162552657969, 8719367486979086660, 5969047515714888644, 2289665069808727608, 9184933632913837923, 11005263514968372299, 2986644488544961059, 12642367899479169090], [1415266954123356504, 5196028033687313810, 13847123422449984196, 12224968642503558906, 7419710020465477027, 6956396696349324468, 11671949362833794642, 11309098093197709475, 10074954992359646374, 11540715179946764441, 1239970357406809, 3021313113679079260], [1244665840952148477, 12823941279147951699, 11009101821508435932, 10233134159772158641, 1858708212835509553, 5913496084653008678, 7211700937107827333, 8238805137398804919, 6166206377233460404, 1662315252276334894, 9446631311604712091, 7527973062289118028], [16473135077892871285, 9048419426550555028, 11955462843042512, 17320499548006488192, 7384030122020672818, 14392901402579125122, 4580400822933258404, 1794163683254998077, 13404233601032749201, 10863492292697479221, 6912208541464453954, 11339295332537132937], [10403906945843229530, 6991511138952997470, 4547192431388582371, 11530974162301645526, 14846281922116489869, 1074618295006158138, 2512384291041522278, 14624727640935460298, 7087102419361800121, 5213332677153874103, 5439356426758102758, 5495058245059055955], [12738504207408299722, 8610961843478257836, 16271812479500291954, 4449026618825469543, 9851321801061792596, 12310130416356494510, 1069178261966873710, 18136763645150820478, 15228984774564243060, 4187702055095081421, 3512526294966463979, 3708387356131937791]], [[13086459540053973335, 18134684027554908539, 18229220653074128752, 6365423563640195538, 8804421041919480649, 14802842342950369854, 16284400375459267631, 16671986587022769942, 5118996020611360153, 12611943924116427630, 17261066879283995729, 7857965876391942691], [15627593372429549226, 8917174667256336074, 4150276273688744768, 15833550595586125312, 1320646322444298996, 17282481370708914892, 11185470494971418827, 18287925568586968761, 12303914011563084861, 14246228603681223631, 17235767688634564597, 15159275233013854245], [3859129251912212910, 16322518938522746707, 5530324644412769609, 16964074166998444986, 9738048044386028331, 7535956126734155481, 6827462229788379852, 7365747889112163930, 17696255645632665445, 10838315022180100605, 7731885007855964578, 15270056568457763801], [18249820902549229618, 4326483773915176400, 9194921459450835524, 12799241044446552352, 11613709761695006467, 16243460015182809131, 10774093342577820910, 14043278033804694925, 8369231874308781866, 14986432051460837060, 13813685122364304024, 291605853114613555], [17885848282217034814, 7300106312099961342, 16737982599777708026, 17080809745183016909, 6769475720645550546, 16772197896038188985, 16217789387847341794, 9824280181818922272, 5827076905381557545, 12534291112560447071, 8942467283567090775, 12201203746721871873], [1125466440647417992, 7712933236355576583, 18364075661472179132, 274066230899992716, 9061515525896570011, 2703710648647612706, 17618457053814158159, 16552541536873208764, 2385704045369041405, 15243136248019111234, 11192633289839038508, 12096789468044662281], [833959530199534834, 1668086708037214448, 4130441827074545860, 16380729318987277832, 3027544804930607876, 13631086911213775952, 569418358163625667, 13425057391576525140, 12767031431193747865, 2075415642001073944, 386561514243071416, 17651570013726926542], [378995168330658849, 3807862492874115162, 243454551579527455, 7256538025218634640, 11966391224263016713, 13692700521359275861, 817904649501850456, 2598659928926340205, 2393205316270609249, 14124025013086241734, 9206301186656747335, 6077442763666685695]]]
#initialisation_zobrist()
echiquier_init = [1152921504606846976,9295429630892703744,2594073385365405696,4755801206503243776,71776119061217280,576460752303423488,16,129,36,66,65280,8] #positition initiales des pieces sur l'echiquier
transposition_table_positions = {} #stock evaluations des positions de profondeur 0, celles analysés suffisament loin
transposition_table_evaluations = {} #stock evaluations des positions de profondeur prf, celles tout juste evaluées
ouvertures = {11535791648361902632: 'e2e4', 4921370276097860652: 'g1f3', 16005836854738279446: 'g1f3', 9326316193898095309: 'd2d4', 1079385303291527066: 'd2d4', 12492157655642070144: 'd2d4', 17775614211299358778: 'e4d5', 13431755716002035610: 'e4e5', 6929298727715262559: 'd2d4', 16626695128573892177: 'd2d4', 5483524398049979922: 'd2d4', 8994247834783985259: 'f1b5', 18034048546586863717: 'd2d4', 12668518916066712982: 'b1c3', 2330782999207608513: 'b1c3', 14931595050893225083: 'b1c3', 11349758690411392060: 'b1c3', 10075021712631964872: 'd2d4', 14318812029394359347: 'd2d4', 11312342971509107778: 'f3d4', 1903246540482964044: 'f3d4', 12963087694145195986: 'g1f3', 13825442860084130813: 'b1c3', 12676593569744105240: 'f2f4', 18336634765298704067: 'b5a4', 6863103225492973345: 'e1g1', 12969842184624225332: 'g1f3', 11792283904355713824: 'e1g1', 13528892284962155321: 'd2d4', 5140991346815029048: 'd2d4', 8580368605231361958: 'f1e1', 10055315825466788775: 'f1e1', 6417130659020163531: 'f3d4', 11931730770409762250: 'f3d4', 17649021736469842001: 'b1c3', 14349115251812825571: 'c1e3', 16780951013540003845: 'd4b3', 17855130562154343701: 'c1g5', 163099214992679076: 'b1c3', 1041545760599827474: 'f3d4', 8248862342070881887: 'b1c3', 9563114840970571139: 'd4b5', 10008662386590600121: 'c1g5', 10200771208646865116: 'b5a3', 17181755218685127759: 'c3d5', 17105679591765654747: 'g5f6', 11777234103896673255: 'c2c3', 7706583925165832901: 'd1d2', 14172683193254752887: 'e1c1', 9235733950493148524: 'c2c4', 4624894663938490470: 'c1e3', 840556894866559500: 'b1c3', 2604225170213314200: 'f1e2', 276375376858845256: 'e1g1', 1602949283259295187: 'd4b5', 1759846215303414761: 'b1c3', 3144529889754247771: 'b5a3', 5206773935806033608: 'c3d5', 5292658761664568072: 'b1c3', 4444396163057463720: 'c1e3', 15523751610183981600: 'd1d2', 15597426216764713840: 'e1c1', 12739900384111481359: 'f3d4', 8762645829644144638: 'f1d3', 1849329772336890678: 'd4b3', 108232807110858925: 'e1g1', 15626751676475700764: 'b1c3', 6732509699654522198: 'g2g4', 13789359064995910604: 'h2h4', 3700041374846632559: 'h1g1', 15851156370948756312: 'd4b5', 15395684599686821218: 'c1f4', 14534589818851105070: 'f4g5', 8580378566936290368: 'a3c2', 5121721486881307834: 'e1g1', 11527772045313082895: 'f1e1', 6145146138342963214: 'a4b3', 2292550756294513570: 'c2c3', 14677866808103451653: 'h2h3', 2206867739281672076: 'b3c2', 236586092199534609: 'd2d4', 9760725454090514970: 'b1d2', 1554573357915831234: 'c3d4', 10185697891540166671: 'a4b3', 11258801822428555033: 'd4e5', 1392538488106354216: 'b1d2', 13014481673235638330: 'e1g1', 9371242994485547935: 'c2c3', 10539757914199798234: 'b5c6', 16342236544694441489: 'd4e5', 1678609994749595221: 'd1d8', 3228148002504889247: 'd4c6', 17113658799741387647: 'f3e5', 17247506459549331565: 'e5f3', 12767758858481403148: 'd2d4', 12226169947265602711: 'f1d3', 4618908528466063056: 'e1g1', 8954823979764329471: 'c2c4', 4289476519910209732: 'd3e2', 17245574439892011843: 'b1c3', 8452879681257724627: 'd1e2', 9586573652712994716: 'e2e4', 12474054469240717011: 'd2d4', 14776026716785102436: 'd4e5', 7624384042726913635: 'e5c6', 8296319024280364288: 'e4e5', 6584034022859375903: 'd2d4', 9476132011210123852: 'e4e5', 65219292960024400: 'a2a3', 16268486385198002093: 'b2c3', 2717550544782755390: 'd1g4', 7467691378324471613: 'f1d3', 10238702450285053306: 'g4h5', 11101113631135641871: 'e5f6', 14135649639012580907: 'c1g5', 11484493568836543051: 'g4h5', 18189161170985614302: 'h5d1', 2225746500165299489: 'c1d2', 14778563096115865407: 'd1g4', 4415301644247045574: 'e4e5', 18225667882799547629: 'f2f4', 8976241924021288937: 'g1f3', 16024897542636834196: 'c1e3', 3792317297359201820: 'd1d2', 10651930862919499904: 'a2a3', 817828236093346584: 'f3d4', 8891034494303399056: 'd1d2', 14519197008746387716: 'e1c1', 9648235357717226579: 'd2f2', 12524880096698693865: 'g1f3', 11926671201631187671: 'f1e2', 15120804233264466321: 'e1g1', 18373976681241905521: 'c1e3', 3154533404007651325: 'f3d4', 7570427407127281666: 'b1d2', 13805534085794702577: 'e1g1', 4442354895683905433: 'f1d3', 4177497987252146087: 'g1f3', 5638086849460997698: 'f1c4', 16224026885866149072: 'e1g1', 4424114929752811336: 'b1c3', 14819556638393930886: 'c1e3', 2840503811943743246: 'd1d2', 9230472654609242514: 'f2f3', 5203097002284170409: 'd2d4', 5195559691061950412: 'b1c3', 7930298240510965660: 'g1f3', 1268143390452033365: 'h2h3', 16145888253652054158: 'e4e5', 13870038070555947435: 'd2d4', 11679777248833028432: 'g1f3', 2726014541159503417: 'f1c4', 3424037796422279866: 'c1d2', 16373738759108839722: 'c3d5', 8487796190851704740: 'h2h3', 18225413932602688341: 'g2g4', 12007405144331450331: 'f3e5', 5687187629900338761: 'f1g2', 4306471230710267301: 'h2h3', 12890621573751413076: 'g2g4', 16765707560142466522: 'f3e5', 9184885211354695571: 'e5g6', 5967960559446550482: 'g1f3', 14728768282234068150: 'd2d4', 12541884026628762701: 'g1f3', 4329090560563530438: 'g2g3', 13876819241546293116: 'f1g2', 111144025615214890: 'g1f3', 13873099745783004528: 'c2c4', 8550808680626895513: 'b1c3', 9684615071551719767: 'c4c5', 7222210019004246310: 'f1e2', 8069101057300224443: 'e1g1', 16171353913028035820: 'e1g1', 8280951775092382600: 'f1c4', 11246064497138659572: 'c4b3', 458045666840627374: 'f3g5', 7365450180972312765: 'd1f3'}

hash_init = zobrist_hash(echiquier_init,tab_zobrist)
echiquier_generaux = echiquier_gen(echiquier_init)
echiquier_generaux.insert(2,hash_init)
for i in range(4):
    echiquier_generaux.insert(3,True)
echiquier_generaux.insert(7,[0,0])
position_init = echiquier_init + echiquier_generaux #position constituée des indices 0 à 11 des positions des 12 pieces respectivement (dame blanc,tour blanc,fou blanc,cavalier blanc,pion blanc,roi blanc,dame noir,tour noir,fou noir,cavalier noir,pions noir,roi noir), indice 12 la position blanc, indice 13 la position noir, indice 14 le hash de la position, indices 15 à 18 les droits (booleen) de rock (petit rock blanc,grand rock blanc,petit rock noir,grand rock noir), indice 19 un couple des droits de prise en passant [blanc,noir] et indice 20 la position totale (toujours appelée avec l'indice -1)
couleur_IA = 12
couleur_ADV = 13

#couleurs à modifier pour chaque parties : 12 = blanc, 13 = noir
prof_prise = 0
prof = 4 + prof_prise #profondeur d'analyse souhaitee au debut de la partie (ne peut jamais descendre en dessous de cette profondeur)
prf = prof #profondeur variable
tab_colonnes = [9259542123273814144,4629771061636907072,2314885530818453536,1157442765409226768,578721382704613384,289360691352306692,144680345676153346,72340172838076673] #binaire des differentes colonnes (pour evaluation)
valeurs = [900,500,330,320,100,20000,900,500,330,320,100,20000] #valeurs de base des differentes pieces dans l'ordre de leur index
tab_valeurs_ponderees = [[-20,-10,-10, -5, -5,-10,-10,-20,-10,  0,  5,  0,  0,  0,  0,-10,-10,  5,  5,  5,  5,  5,  0,-10,0,  0,  5,  5,  5,  5,  0, -5,-5,  0,  5,  5,  5,  5,  0, -5,-10,  0,  5,  5,  5,  5,  0,-10,-10,  0,  0,  0,  0,  0,  0,-10,-20,-10,-10, -5, -5,-10,-10,-20],
                         [0, 0, 0, 5, 5, 0, 0, 0,-5, 0, 0, 0, 0, 0, 0, -5,-5, 0, 0, 0, 0, 0, 0, -5,-5, 0, 0, 0, 0, 0, 0, -5,-5, 0, 0, 0, 0, 0, 0, -5,-5, 0, 0, 0, 0, 0, 0, -5,5, 10, 10, 10, 10, 10, 10, 5,0, 0, 0, 0, 0, 0, 0, 0],
                         [-20,-10,-10,-10,-10,-10,-10,-20,-10,  5,  0,  0,  0,  0,  5,-10,-10, 10, 10, 10, 10, 10, 10,-10,-10,  0, 10, 10, 10, 10,  0,-10,-10,  5,  5, 10, 10,  5,  5,-10,-10,  0,  5, 10, 10,  5,  0,-10,-10,  0,  0,  0,  0,  0,  0,-10,-20,-10,-10,-10,-10,-10,-10,-20],
                         [-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,  0,  5,  5,  0,-20,-40,-30,  5, 10, 15, 15, 10,  5,-30,-30,  0, 15, 20, 20, 15,  0,-30,-30,  5, 15, 20, 20, 15,  5,-30,-30,  0, 10, 15, 15, 10,  0,-30,-40,-20,  0,  0,  0,  0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50],
                         [ 0,  0,  0,  0,  0,  0,  0,  0,5, 10, 10,-20,-20, 10, 10,  5, 5, -5,-10,  0,  0,-10, -5,  5,0,  0,  0, 20, 20,  0,  0,  0,5,  5, 10, 25, 25, 10,  5,  5,10, 10, 20, 30, 30, 20, 10, 10,50, 50, 50, 50, 50, 50, 50, 50, 0,  0,  0,  0,  0,  0,  0,  0],
                         [20, 30, 10,  0,  0, 10, 30, 20,20, 20,  0,  0,  0,  0, 20, 20,-10,-20,-20,-20,-20,-20,-20,-10,-20,-30,-30,-40,-40,-30,-30,-20,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30],
                         [-20,-10,-10, -5, -5,-10,-10,-20,-10,  0,  0,  0,  0,  0,  0,-10,-10,  0,  5,  5,  5,  5,  0,-10,-5,  0,  5,  5,  5,  5,  0, -5,0,  0,  5,  5,  5,  5,  0, -5,-10,  5,  5,  5,  5,  5,  0,-10,-10,  0,  5,  0,  0,  0,  0,-10,-20,-10,-10, -5, -5,-10,-10,-20],
                         [0, 0, 0, 0, 0, 0, 0, 0,5, 10, 10, 10, 10, 10, 10, 5,-5, 0, 0, 0, 0, 0, 0, -5,-5, 0, 0, 0, 0, 0, 0, -5,-5, 0, 0, 0, 0, 0, 0, -5,-5, 0, 0, 0, 0, 0, 0, -5,-5, 0, 0, 0, 0, 0, 0, -5,0, 0, 0, 5, 5, 0, 0, 0],
                         [-20,-10,-10,-10,-10,-10,-10,-20,-10,  0,  0,  0,  0,  0,  0,-10,-10, 0, 5, 10, 10, 5, 0,-10,-10,  5, 5, 10, 10, 5,  5,-10,-10,  0,  10, 10, 10,  10,  0,-10,-10,  10,  10, 10, 10,  10,  10,-10,-10,  5,  0,  0,  0,  0,  5,-10,-20,-10,-10,-10,-10,-10,-10,-20],
                         [-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,  0,  0,  0,  0,-20,-40,-30,  0, 10, 15, 15, 10,  0,-30,-30,  5, 15, 20, 20, 15,  5,-30,-30,  0, 15, 20, 20, 15,  0,-30,-30,  5, 10, 15, 15, 10,  5,-30,-40,-20,  0,  5,  5,  0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50],
                         [ 0,  0,  0,  0,  0,  0,  0,  0,50, 50, 50,50,50, 50, 50,  50, 10, 10,20,  30,  30,20, 10,  10,5,  5,  10, 25, 25,  10,  5,  5,0,  0, 0, 20, 20, 0,  0,  0,5, -5, -10, 0, 0, -10, -5, 5,5, 10, 10, -20, -20, 10, 10, 5, 0,  0,  0,  0,  0,  0,  0,  0],
                         [-30, -40, -40,  -50,  -50, -40, -40, -30,-30, -40, -40,  -50,  -50, -40, -40, -30,-30, -40, -40,  -50,  -50, -40, -40, -30,-30, -40, -40,  -50,  -50, -40, -40, -30,-20,-30,-30,-40,-40,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,30,10,0,0,10,30,20]]
#tableau de ponderation des pieces suivant leur place sur l'echiquier

position = position_init
endgame = False
partie = []
MAX = 10000000000
MIN = -10000000000
game_id = input('Id of the Lichess game')

def main():
    global position
    global prf
    global prof_prise
    global endgame
    while True:
        partie.append(position)
        if position[14] in ouvertures:
            coup_lichess = ouvertures[position[14]]
            print('ouverture',coup_lichess)
            coup = [binaire_indice([int(coup_lichess[1])-1,ord(coup_lichess[0])-97]),binaire_indice([int(coup_lichess[3])-1,ord(coup_lichess[2])-97])]
            couleur_piece = piece_couleur_case(position, coup[0])
            position = creer_position_fils(position, coup, couleur_piece[1],[[int(coup_lichess[1])-1,ord(coup_lichess[0])-97], [int(coup_lichess[3])-1,ord(coup_lichess[2])-97]], couleur_IA)
        else :
            debut = time.time()
            L_minimax = minimax(position,0,'IA',MIN,MAX)
            fin = time.time()
            chrono = fin - debut
            print(prf,'/',round(chrono,2))
            if chrono < 6: #adapte la profondeur au temps de calcul
                prf +=1
                prof_prise += 1
            if chrono > 60 and prf!=prof:
                prf -= 1
                prof_prise -= 1
            coup = L_minimax[-1]
            if coup == MIN:
                client.bots.post_message(game_id, 'GG')
                client.bots.resign_game(game_id)
                break
            couleur_piece = piece_couleur_case(position,coup[0])
            position = creer_position_fils(position,coup,couleur_piece[1],[indices_binaire(coup[0]),indices_binaire(coup[1])],couleur_IA)
            partie.append(position)
            variante = []
            eval = L_minimax.pop(0)
            for elt in reversed(L_minimax):
                indices = [indices_binaire(elt[0]),indices_binaire(elt[1])]
                variante.append(chr(indices[0][1]+97)+str(indices[0][0] + 1)+chr(indices[1][1]+97)+str(indices[1][0] + 1))
            print(variante)
            print(eval)
            coup_lichess = variante[0]
        client.bots.make_move(game_id, coup_lichess)
        for event in client.bots.stream_game_state(game_id):
            try:
                if event['moves'][-5] == ' ':
                    coup_lichess_adv = event['moves'][-4:]
                else:
                    coup_lichess_adv = event['moves'][-5:-1]
                break
            except:
                coup_lichess_adv = ''
        try :
            indices_adv = [[int(coup_lichess_adv[1])-1,ord(coup_lichess_adv[0]) - 97],[int(coup_lichess_adv[3])-1,ord(coup_lichess_adv[2]) - 97]]
        except:
            return
        coup_adv = [binaire_indice(indices_adv[0]),binaire_indice(indices_adv[1])]
        couleur_piece_adv = piece_couleur_case(position, coup_adv[0])
        position = creer_position_fils(position,coup_adv,couleur_piece_adv[1],indices_adv,couleur_ADV)
        if position[0] == 0 and position[1] == 0 and position[6] == 0 and position[7] == 0:
            endgame = True
            print('endgame')
            tab_valeurs_ponderees[5] = [-50, -30, -30, -30, -30, -30, -30, -50, -30, -30, 0, 0, 0, 0, -30, -30, -30, -10, 20, 30, 30, 20, -10, -30, -30, -10, 30, 40, 40, 30, -10, -30, -30, -10, 30, 40, 40, 30, -10, -30, -30, -10, 20, 30, 30, 20, -10, -30, -30, -20, -10, 0, 0, -10, -20, -30, -50, -40, -30, -20, -20, -30, -40, -50]
            tab_valeurs_ponderees[11] = [-50, -40, -30, -20, -20, -30, -40, -50, -30, -20, -10, 0, 0, -10, -20, -30, -30, -10, 20, 30, 30, 20, -10, -30, -30, -10, 30, 40, 40, 30, -10, -30, -30, -10, 30, 40, 40, 30, -10, -30, -30, -10, 20, 30, 30, 20, -10, -30, -30, -30, 0, 0, 0, 0, -30, -30, -50, -30, -30, -30, -30, -30, -30, -50]
            tab_valeurs_ponderees[4] = [0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 10, -20, -20, 10, 10, 5, 5, -5, -10, 0, 0, -10, -5, 5, 40, 40, 40, 40, 40, 40, 40, 40, 80, 80, 80, 80, 80, 80, 80, 80, 120, 120, 120, 120, 120, 120, 120, 120, 200, 200, 200, 200, 200, 200, 200, 200, 0, 0, 0, 0, 0, 0, 0, 0]
            tab_valeurs_ponderees[10] = [0, 0, 0, 0, 0, 0, 0, 0, 200, 200, 200, 200, 200, 200, 200, 200, 120, 120, 120, 120, 120, 120, 120, 120, 80, 80, 80, 80, 80, 80, 80, 80, 40, 40, 40, 40, 40, 40, 40, 40, 5, -5, -10, 0, 0, -10, -5, 5, 5, 10, 10, -20, -20, 10, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0]

main()

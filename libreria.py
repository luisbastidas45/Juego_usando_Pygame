import pygame

def llenar_matriz(imagen, can_an, can_al, corte_an, corte_al):
    ls_img=[]

    for i in range(can_an): # 0-15
        fila2=[]
        for c in range(can_al): #0-14
            cuadro=imagen.subsurface(i*corte_an, c*corte_al, corte_an, corte_al)
            fila2.append(cuadro)
        ls_img.append(fila2)

    return ls_img

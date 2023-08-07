import pygame
import random
from libreria import llenar_matriz

#constantes
AZUL_CLARO=[76,160,233]
VERDE_CLARO=[80,240,107]
ancho = 600
alto = 480
verde_claro=[97,192,12,255]
blanco = [255,255,255]
negro = [0,0,0]
VERDE = [97,192,12,255]
rojo=[139,0,0]
amarillo=[236,230,50]
gris=[205,204,205,25]
verde_oscuro=[130,242,138]
azul=[48,187,246]

#CLASES

class Jugador(pygame.sprite.Sprite):
    def __init__(self,pos, matriz):
        pygame.sprite.Sprite.__init__(self)
        self.matriz=matriz
        self.accion=1
        self.col=0
        self.lim=[3,5,3]
        self.estado=0



        self.image = self.matriz[self.col][self.accion]
        self.rect = self.image.get_rect()

        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.velx=0
        self.vely=0
        self.salud=100
        #self.salto=pygame.mixer.Sound('salto.ogg')
        self.bloques=pygame.sprite.Group()
        self.puntos=0

    def update(self):
        #if self.velx != self.vely: #detener la animacion cuando no exista movimiento
        self.image= self.matriz[self.col][self.accion] #actualiza rel sprite

        if self.col < self.lim[self.accion]:
            self.col+=1
        else:
            self.col=0
            self.accion=1
        self.rect.x += self.velx

        ls_col=pygame.sprite.spritecollide(self,self.bloques,False)
        for p in ls_col:
            if self.velx >= 0:
                if self.rect.right > p.rect.left:
                    self.rect.right = p.rect.left

            else:
                if self.rect.left < p.rect.right:
                    self.rect.left = p.rect.right


        self.rect.y+= self.vely

        #=====
        ls_col=pygame.sprite.spritecollide(self,self.bloques,False)
        for p in ls_col:
            if self.vely > 0:
                if self.rect.bottom > p.rect.top:
                    self.rect.bottom = p.rect.top
                    #self.salto.play()
                    self.vely=0.1
            else:
                if self.rect.top < p.rect.bottom:

                    self.rect.bottom = p.rect.top
                    self.vely=1


        #====
        if self.vely != 0:
            self.vely += 0.51  ##rapidez de caida


        if self.rect.bottom > alto:
            self.rect.bottom = alto
            self.vely=0



class Bloque(pygame.sprite.Sprite): #esta es la plataforma

    def __init__(self, pos, dim, cl= verde_claro):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dim)
        self.image.fill(cl)
        self.rect = self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.velx=0

    def update(self):
        self.rect.x += self.velx


class Goma(pygame.sprite.Sprite):
    def __init__(self, pos,imagen_gen, cl=verde_oscuro):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen_gen

        self.rect = self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.velx=0


        self.disparar = False
        self.temp=100
        self.vida=20
        self.cantidad_generador=9
        self.pl=pygame.sprite.Group()

    def update(self):
        self.rect.x +=self.velx

        self.temp -=1
        if self.temp <= 0:
            self.disparar=True


class GomaFinal(pygame.sprite.Sprite):
    def __init__(self, pos,imagen_gen, cl=verde_oscuro):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen_gen

        self.rect = self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.velx=0


        self.disparar = False
        self.temp=100
        self.vida=20
        self.cantidad_generador=9
        self.pl=pygame.sprite.Group()

    def update(self):
        self.rect.x +=self.velx

        self.temp -=1
        if self.temp <= 0:
            self.disparar=True


class Bala(pygame.sprite.Sprite):

    def __init__(self,pos,imagen_enem,cl=blanco):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen_enem
        self.rect = self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.vely=1
        self.velx=0
        self.pl=pygame.sprite.Group()

    def update(self):
        self.rect.x -= self.velx

        self.rect.y+= self.vely

        #=====
        ls_col=pygame.sprite.spritecollide(self,self.pl,False)
        for p in ls_col:
            if self.vely > 0:
                if self.rect.bottom > p.rect.top:
                    self.rect.bottom = p.rect.top
                    self.vely=0
        if self.vely <= 0:
            self.vely=20



        #====
        if self.vely != 0:
            self.vely += 0.51  ##rapidez de caida



        if self.rect.bottom > alto:
            self.rect.bottom = alto
            self.vely=0


class Balajugador(pygame.sprite.Sprite):

    def __init__(self,pos,cl=blanco):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10,10])
        self.image.fill(cl)
        self.rect = self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.velx=0
    def update(self):
        self.rect.x += 10


class Modificador(pygame.sprite.Sprite):

    def __init__(self,pos,imagen_pre,cl=rojo):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen_pre
        self.rect = self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]-20
        self.vely=0
        self.velx=0

    def update(self):
        self.rect.y += self.vely
        if  self.rect.bottom > (alto - 10): #limite de pantalla
            self.rect.bottom = alto - 10
        self.rect.x += self.velx







if __name__ == '__main__':
    #inicializacion
    pygame.init()
    pantalla=pygame.display.set_mode([ancho,alto])

    #VARIABLES
    salto=pygame.mixer.Sound('salto.ogg')
    sonido3=pygame.mixer.Sound('sonido3.ogg')
    sonido2=pygame.mixer.Sound('sonido2.ogg')
    fuente_juego=pygame.font.Font(None,32)
    fuente=pygame.font.Font(r"C:\Users\Acer\Documents\UNIVERSIDAD\COMPUTACION GRAFICA\PROYECTO FINAL\8-BIT WONDER.TTF",26)
    fuente1=pygame.font.Font(r"C:\Users\Acer\Documents\UNIVERSIDAD\COMPUTACION GRAFICA\PROYECTO FINAL\8-BIT WONDER.TTF",15)

#====================================================================

    #ciclo de presentacion
    fin=False
    seguir=False

    while not fin and not seguir:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            if event.type == pygame.KEYDOWN:
               seguir=True

        sonidito=sonido2.play()
        
        fondo_presentacion=pygame.image.load('paper.png')
        texto=fuente.render('INICIO DE JUEGO', True, rojo)
        #texto3=fuente.render('JUEGO TERMINADO', True, rojo)
        #texto_final=fuente.render('JUEGO TERMINADO', True, rojo)
        texto1=fuente1.render('Presione cualquier tecla', True, blanco)
        pantalla.blit(fondo_presentacion,[0,0])
        pantalla.blit(texto, [160,50])
        pantalla.blit(texto1, [240,450])

        pygame.display.flip()

#=====================================================================

    #ciclo principal

    #grupos
    jugadores = pygame.sprite.Group()
    gomas = pygame.sprite.Group()
    Balas =pygame.sprite.Group()
    balas_g = pygame.sprite.Group()
    bloques = pygame.sprite.Group()
    balasjugador=pygame.sprite.Group()
    modificadores = pygame.sprite.Group()
    gomafinal = pygame.sprite.Group()


    #PROPIEDADES

    #propiedades del sprite principal
    imagen=pygame.image.load('calvo.png')
    info=imagen.get_rect()
    can_ancho=6
    can_alto=3
    cor_ancho=int(info[2])/can_ancho
    cor_alto=int(info[3])/can_alto
    matriz=llenar_matriz(imagen,can_ancho,can_alto,cor_ancho,cor_alto)


    #propiedades del fondo
    fondo=pygame.image.load('a1copia.png')
    info=fondo.get_rect()
    f_ancho=info[2]
    f_largo=info[3]
    print('propiedades fondo: ', info, f_ancho, f_largo )
    f_x=0
    f_vx=0
    f_limx=ancho-f_ancho
    lim_d= 350 #limite de pantalla para avance del fondo



    #j.vely= -4.5

    b=Bloque([0,280],[807,1])  #1
    bloques.add(b)

    b=Bloque([807,280],[130,1],gris) #2
    bloques.add(b)

    b=Bloque([935,280],[145,1])    #3
    bloques.add(b)

    b=Bloque([1127,247],[285,1])   #4
    bloques.add(b)

    b=Bloque([1128,329],[128,1])   #5
    bloques.add(b)

    b=Bloque([1258,312],[182,1])   #6
    bloques.add(b)

    b=Bloque([1439,297],[96,1])    #7
    bloques.add(b)

    b=Bloque([1535,312],[73,1])    #8
    bloques.add(b)

    b=Bloque([1608,312],[129,1],gris)  #9
    bloques.add(b)

    b=Bloque([1737,312],[366,1])   #10
    bloques.add(b)

    b=Bloque([2154,297],[146,1])   #11
    bloques.add(b)

    b=Bloque([2341,264],[127,1])   #12
    bloques.add(b)

    b=Bloque([2472,248],[64,1])    #13
    bloques.add(b)

    b=Bloque([2536,248],[127,1],gris)  #14
    bloques.add(b)

    b=Bloque([2662,248],[250,1])   #15
    bloques.add(b)

    b=Bloque([2911,265],[65,1])    #16
    bloques.add(b)

    b=Bloque([2946,296],[190,1])   #17
    bloques.add(b)

    b=Bloque([3138,265],[25,1])    #18
    bloques.add(b)

    b=Bloque([3169,234],[31,1])    #19
    bloques.add(b)

    b=Bloque([3207,297],[59,1])    #20
    bloques.add(b)

    b=Bloque([3233,329],[159,1])   #21
    bloques.add(b)

    b=Bloque([3394,361],[62,1])    #22
    bloques.add(b)

    b=Bloque([3425,393],[384,1])   #23
    bloques.add(b)

    b=Bloque([3810,361],[30,1])    #24
    bloques.add(b)

    b=Bloque([3841,328],[187,1])   #25
    bloques.add(b)

    b=Bloque([4069,298],[220,1])   #26
    bloques.add(b)

    b=Bloque([4290,328],[154,1])   #27
    bloques.add(b)

    b=Bloque([4486,297],[416,1])   #28
    bloques.add(b)


    b.velx=0

    #OBJETOS
    j=Jugador([0,240],matriz)
    j.bloques=bloques
    jugadores.add(j)

    imagen2= pygame.image.load('esp2.png')

    g=Goma([737,200],imagen2)
    gomas.add(g)

    g=Goma([1342,157],imagen2)
    gomas.add(g)

    g=Goma([1465,207],imagen2)
    gomas.add(g)

    g=Goma([2033,222],imagen2)
    gomas.add(g)

    g=Goma([2398,174],imagen2)
    gomas.add(g)

    g=Goma([2842,158],imagen2)
    gomas.add(g)

    g=Goma([3739,303],imagen2)
    gomas.add(g)

    g=Goma([4219,208],imagen2)
    gomas.add(g)

    g1=GomaFinal([4600,207],imagen2) #4600
    gomafinal.add(g1)

    j.vely= -4.5


    conf=False
    chao2=False
    sonidito=sonido2.stop()
    sonidito3=sonido3.play()

    reloj=pygame.time.Clock()
    fin_juego=False
    fin=False
    #ciclo principal
    while (not fin) and (not fin_juego):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            #if event.type == pygame.MOUSEBUTTONDOWN:
                #print(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    j.velx=5


                if event.key == pygame.K_LEFT:
                    j.velx=-5
                if event.key == pygame.K_SPACE:
                    
                    salto1=salto.play()
                    j.vely= -4.5
            if event.type == pygame.KEYUP:


                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT):
                    j.velx=0

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                if event.button == 1:

                    b=Balajugador(j.rect.midright,azul)
                    balasjugador.add(b)

        if j.rect.right > lim_d:
            j.rect.right = lim_d
            f_vx= -5


        else:
            f_vx=0
        for b in bloques:
            b.velx=f_vx
        for g in gomas:
            g.velx=f_vx
        for g1 in gomafinal:
            g1.velx=f_vx
        for m in modificadores:
            m.velx=f_vx
        for b_g in balas_g:
            b_g.velx=5





        for j1 in jugadores:
            ls_col=pygame.sprite.spritecollide(j1,modificadores,True)
            p= random.randrange(4)
            for n in ls_col:
                if p==2 or p==0:
                    j.puntos+=100
                if j.salud < 100:
                    print("valor p: ",p)
                    if p==1:
                        j.salud += 5
                        j.puntos+=50
                        print("vida normal")
                    if p==3:
                        v=100-j.salud
                        j.salud +=v
                        j.puntos+=50
                        print("vida completa")


       
        for g in gomas: #elima los elementos una vez salgan de la pantalla
            if g.rect.y < -10:
                '''Gomas.remove(g)'''
 
        ls_col=pygame.sprite.spritecollide(j,gomas,False)
        for g in ls_col:
            if j.salud > 0:
                j.salud -=5


        confirmacion=False
        for b in balasjugador:
            if g.vida == 0:
                confirmacion=True

            ls_imp=pygame.sprite.spritecollide(b,gomas,confirmacion) #eliminar la goma

            if len(ls_imp) > 0:
                balasjugador.remove(b)
                print("chao1")
                if g.vida > 0:
                    g.vida-=10



            if b.rect.y < -10:
                Balas.remove(b)

        ##========
        for b in balasjugador:
            if g1.vida == 0:
                confirmacion=True

            ls_imp=pygame.sprite.spritecollide(b,gomafinal,confirmacion) #eliminar la goma

            if len(ls_imp) > 0:
                balasjugador.remove(b)
                print("chao2")
                chao2=True
                fin_de_juego=True
                if g1.vida > 0:
                    g1.vida-=10


            if b.rect.y < -10:
                Balas.remove(b)



        
        ##=======
        imagen=pygame.image.load('hongo.png')

        for g in gomas:
            if g.disparar:
                #crear Bala
                #iniciar temporizador
                #disparar en falso
                b=Bala(g.rect.midleft,imagen)
                b.vely=1
                b.pl=bloques
                balas_g.add(b)
                g.temp=random.randrange(110)  #revisar estado de disparos generador 350
                g.disparar=False

        for g1 in gomafinal:
            if g1.disparar:
                #crear Bala
                #iniciar temporizador
                #disparar en falso
                b=Bala(g1.rect.midleft,imagen)
                b.vely=1
                b.pl=bloques
                balas_g.add(b)
                g1.temp=random.randrange(110)  #revisar estado de disparos generador 350
                g1.disparar=False

        for b in balas_g:
            ls_colj= pygame.sprite.spritecollide(b,jugadores,False)
            if len(ls_colj) > 0:
                if j.salud > 0:
                    j.salud-=5
                balas_g.remove(b)
            if b.rect.x < 0:
                balas_g.remove(b)
                print("borrar")
            if b.rect.y > alto-100:
                balas_g.remove(b)
                print("se cayo")
        for a in balasjugador:
            if a.rect.x >ancho:
                balasjugador.remove(a)
                print("eliminada")

        for j2 in jugadores:
            if j2.rect.y > alto-100:
                if j2.salud > 0:
                    j2.salud-=5
            if j2.salud == 0:

                fin_juego=True
                j2.estado=1

        imagen3=pygame.image.load('logo.png')

        for s in balasjugador:
            ls_colb= pygame.sprite.spritecollide(s,balas_g,True)
            for i in ls_colb:
                n=random.randrange(100)
                if n < 50:
                    m=Modificador(i.rect.center,imagen3)
                    modificadores.add(m)
                balasjugador.remove(s)

                print("blaseliminadas")


        '''for d1 in balas_g:
            resta=g.rect.x - d1.rect.x
            if resta > 50:
                balas_g.remove(d1)
                print("eliminada")'''

        if  conf==False and chao2==True:
            print("TERMINASTE")
            conf=True
            j.estado=2
            fin_juego=True




        jugadores.update()
        bloques.update()
        gomas.update()
        Balas.update()
        balas_g.update()
        balasjugador.update()
        modificadores.update()
        gomafinal.update()

        info="Salud: " + str(j.salud)
        texto=fuente.render(info,False,blanco)
        info3="Puntos: "+ str(j.puntos)
        texto3=fuente.render(info3,False,blanco)

        pantalla.fill(negro)
        pantalla.blit(fondo,[f_x,0])
        pantalla.blit(texto,[20,20])
        pantalla.blit(texto3,[20,45])


        jugadores.draw(pantalla)
        bloques.draw(pantalla)
        gomafinal.draw(pantalla)
        gomas.draw(pantalla)
        Balas.draw(pantalla)
        balas_g.draw(pantalla)
        balasjugador.draw(pantalla)
        modificadores.draw(pantalla)


        pygame.display.flip()
        reloj.tick(30)
        if f_x > f_limx:
            f_x+=f_vx

    
#===============================================
#CICLO DE DE GANAR

    fin=False
    seguir=False

    while (not fin) and (not seguir):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            if event.type == pygame.KEYDOWN:
                seguir=True

        
        
        pantalla.fill(negro)
        
        fondo_finalizacion=pygame.image.load('retro.jpg')

        pantalla.blit(fondo_finalizacion,[0,0])
        pantalla.blit(texto3, [200,100])


        if j.estado == 1:
            texto_perdedor=fuente.render('HAS PERDIDO', True, blanco)
            pantalla.blit(texto_perdedor, [170,150])


        if j.estado == 2:
           
            texto_final=fuente.render('HAS GANADO', True, blanco)
            pantalla.blit(texto_final, [170,50])


        
        
        pygame.display.flip()

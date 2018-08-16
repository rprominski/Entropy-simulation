from random import random, randint,uniform   
import time
import collections
import math
import matplotlib.pyplot as plt
import pygame

stanZPedami=False  #czy przy wyznaczaniu ilosc atomow w danym stanie uwzgledniac tez pedy 
pedyCalkowite=False  # czy pedy maja miec tylko wartosc calkowita
dynamicznyWykres=False # czy wykres entropii ma byc generowany na biezaco
animacja=True # czy wyswietlac animacje poruszajacych sie czastek
rozmiarOkna=30 # regulacja wielkosci okna animacji (w dlugosciach
rozmiarAtomu=4 # rozmiar atomu na symulacji (w pikselach)
opoznienie=0.07 # opoznienie przy wyswietlaniu animacji (w sekundach)
r=10 # parametr na podstawie ktorego wyznaczana jest ilosc czastek, maksymalny ped i rozmiar pojemnika
     # ilosc czastek bedzie rowna 2^r, dlatego zaleca sie wpisywac tu rozsadna liczbe

# STALE WYZNACZANE NA PODSTAWIE PARAMETRU r 
P=r+(1-r%2) # Maksymalny ped 
R=2*r+1 # Rozmiar pojemnika 
kwantCzasu=1.0/(2*P) # krok czasu po ktorym polozenie atomow jest uaktualniane
N=2**r # ilosc czastek 


atomy=[]
kolor=[]
osX=[]
osY=[]
stany=collections.Counter()

pygame.init()
window=pygame.display.set_mode((R*rozmiarOkna,R*rozmiarOkna))

class Atom:
    def __init__(self,pedX,pedY,polozenieX,polozenieY):
        self.pedX=pedX
        self.pedY=pedY
        self.polozenieX=polozenieX
        self.polozenieY=polozenieY

def silnia(n):
    if n<=1:
        return 1
    else:
        tmp=1
        for i in range(2,n+1):
            tmp*=i
    return tmp

def rysujWykres(x,y):
    plt.plot(x,y,'g-')
    plt.show()

def generujStanPoczatkowy():
    plt.ion()
    ilosc=0
    for i in range(0,R):
        for j in range(0,int(N/R)):
            if pedyCalkowite:
                atomy.append(Atom(randint(-P,P),randint(-P,P),0.0,i*1.0))
            else:
                atomy.append(Atom(uniform(-P,P),uniform(-P,P),0.0,i*1.0))
        ilosc+=N/R
    
    for i in range(int(ilosc),int(N)):
        if pedyCalkowite:
            atomy.append(Atom(randint(-P,P),randint(-P,P),0.0,(i-ilosc)*1.0))
        else:
            atomy.append(Atom(uniform(-P,P),uniform(-P,P),0.0,(i-ilosc)*1.0))
            
    for i in range(0,N):
        kolor.append((randint(0,255),randint(0,255),randint(0,255)))

def ruch(atom):
    if atom.polozenieX+atom.pedX*kwantCzasu<0:
        atom.polozenieX=-(atom.polozenieX+atom.pedX*kwantCzasu)
        atom.pedX*=-1
    elif atom.polozenieX+atom.pedX*kwantCzasu>=R:
        atom.polozenieX=2*R-(atom.polozenieX+atom.pedX*kwantCzasu)
        atom.pedX*=-1
    else:
        atom.polozenieX+=(atom.pedX*kwantCzasu)

    if atom.polozenieY+atom.pedY*kwantCzasu<0:
        atom.polozenieY=-(atom.polozenieY+atom.pedY*kwantCzasu)
        atom.pedY*=-1
    elif atom.polozenieY+atom.pedY*kwantCzasu>=R:
        atom.polozenieY=2*R-(atom.polozenieY+atom.pedY*kwantCzasu)
        atom.pedY*=-1
    else:
        atom.polozenieY+=(atom.pedY*kwantCzasu)
    
    if stanZPedami==True:
        pom= str(int(atom.pedX))+"#"+str(int(atom.pedY))+"#"+str(int(atom.polozenieX))+"#"+str(int(atom.polozenieY))  
    else:
        pom= str(int(atom.polozenieX))+"#"+str(int(atom.polozenieY)) 
    stany[pom]+=1

def obliczEntropie():
    wynik=0.0
    for i in range(1,N+1):
        wynik+=math.log(i)
    for i in stany:
        wynik-=math.log(silnia(stany[i]))
    return wynik

def symulacja():   
    if not dynamicznyWykres:
        maxTime=30

    generujStanPoczatkowy()
    czas=0
    i=0

    running=True
    for atom in atomy:
        ruch(atom)
        if animacja:
            pygame.draw.circle(window,kolor[i],(int(atom.polozenieX*rozmiarOkna),int(atom.polozenieY*rozmiarOkna)),rozmiarAtomu)
        i+=1

    pygame.display.flip()
    while running:
        i=0
        stany.clear()
        window.fill((0,0,0))
        for atom in atomy:
            ruch(atom)
            if animacja:
                pygame.draw.circle(window,kolor[i],(int(atom.polozenieX*rozmiarOkna),int(atom.polozenieY*rozmiarOkna)),rozmiarAtomu)
                i+=1
        if animacja:
            pygame.display.flip()
        time.sleep(opoznienie)
        osY.append(obliczEntropie())
        osX.append(czas)
        if animacja:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    running=False
                if event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running=False
        czas+=kwantCzasu
        
        maxTime-=kwantCzasu
        print (maxTime)
        if maxTime<=0:
            break

def main():
    symulacja()
    pygame.display.iconify()
    rysujWykres(osX,osY)
    plt.show()
    try:
        plt.pause(36000)
    except Exception as e:
        return 0
    return 0

if __name__== "__main__":
  main()
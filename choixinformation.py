from fltk import *

class Recherche:
    def __init__(self,ax,ay,bx,by,tag='',remplissage=''):
        self.ax=ax
        self.ay=ay
        self.bx=bx
        self.by=by
        self.tag=tag
        self.recherche=''
        self.remplissage=remplissage
        rectangle(self.ax,self.ay,self.bx,self.by,tag=self.tag,remplissage=self.remplissage)
##########
    def getCord(self):
        return list((self.ax,self.ay,self.bx,self.by))

    def getTag(self):
        return self.tag

    def getRecherche(self):
        return self.recherche

    def getTaillerecherche(self):
        return taille_texte(self.recherche)

    def getLongueurrectangle(self):
        return self.bx-self.ax

    def initRecherche(self,x):
        self.recherche=str(x)

    def setRecherche(self,x):
        self.recherche+=str(x)
        return self.recherche

    def setRemplissage(self,r=''):
        efface(self.tag)
        self.remplissage=r
        rectangle(self.ax,self.ay,self.bx,self.by,tag=self.tag,remplissage=self.remplissage)
############
    def setBarre(self):
        efface('recherche')
        texte(self.ax+10, self.ay,self.recherche,tag='recherche')
        mise_a_jour()

    def clique(self):
        souris=(abscisse_souris(),ordonnee_souris())
        return (self.getCord()[0]<souris[0]<self.getCord()[2] and self.getCord()[1]<souris[1]<self.getCord()[3])

    def tagsanscase(self):
        return (self.tag).lstrip('case')

class Bouton:
    def __init__(self,x,y,chaine,tag,couleur):
        self.taille_texte = taille_texte(chaine,taille=15)
        self.x=x
        self.y=y
        self.xb,self.yb=None,None
        self.chaine=str(chaine)
        self.tag=tag
        self.texte=texte(x,y,chaine,couleur=couleur ,tag=tag,taille=15)

    def getCord(self):
        return list((self.x,self.y+4,self.x+self.taille_texte[0], self.y+self.taille_texte[1]-4)) #((self.x,self.y,self.xb,self.yb)

    def getTag(self):
        return self.tag

    def getChaine(self):
        return self.chaine

    def getTailletexte(self):
        return self.taille_texte

    def setCord(self,ax,ay,bx,by):
        self.x,self.y,self.xb,self.yb = ax,ay,bx,by

    def setTailletexte(self,ax,bx):
        self.taille_texte=(self.taille_texte[0]+(bx-ax),self.taille_texte[1])

    def clique(self,souris):
        cord=self.getCord()
        return (self.getCord()[0]<souris[0]<self.getCord()[2] and self.getCord()[1]<souris[1]<self.getCord()[3])

    def efface(self):
        efface(self.tag)

    def tagsanscase(self):
        return self.tag.rstrip('case')


def affichebtn(listelien):
    lstbtn=[]
    c=0
    for i in listelien:
        lstbtn.append(Bouton(40,25*(c+1),str(i),'t'+str(c),"black"))
        c=c+1
    return lstbtn

def cliquebtn(lstbtn,tev,lstcase=None):
    ax,bx=0,0

    for i in range(len(lstbtn)):
        if lstcase is not None:
            lstbtn[i-1].setTailletexte(-ax,-bx)
            ax,ay,bx,by=lstcase[i].getCord()
            xa,ya,xb,yb=lstbtn[i].getCord()
            lstbtn[i].setTailletexte(ax,bx)
            lstbtn[i].setCord(ax,ay,xb,yb)

        if lstbtn[i].clique((abscisse_souris(),ordonnee_souris())) and tev=="ClicGauche":
            mise_a_jour()
            return lstbtn[i].getTag(), False, lstbtn[i].getChaine()

        if tev == 'Quitte':
            return None,None,None

    lstbtn[-1].setTailletexte(-ax,-bx)
    return None, True, None

def sport(carte):
    listesport=[]
    with open(carte,'r') as csv_file:

        lines = csv_file.readlines()
        for i in range(1,len(lines)): # coordonnées des villes
            row = lines[i].split(';')
            if row[4] not in listesport:
                listesport.append(row[4])
    return listesport

def information(carte):
    listinfo=[]
    with open(carte,'r') as csv_file:

        lines = csv_file.readlines()
        lines[0]=lines[0].replace('_',' ').rstrip('\n').split(';')
        del lines[0][2:5]
        for i in range(1,len(lines)): # coordonnées des villes i=i.lstrip('FF des')
            row = lines[i].rstrip('\n').split(';')
            del row[2:5]
            listinfo.append(row)
    return lines[0] , listinfo

def casecliqueedansliste(carte,casecliquee):
    with open(carte,'r') as csv_file:
        lines = csv_file.readlines()
        lines[0]=lines[0].rstrip('\n').split(';')
    casecliquee=casecliquee.replace(' ','_')
    
    for i in range (len(lines[0])):
        #print(lines[0][i])
        if casecliquee in lines[0][i]:
            return i

def case(liste):
    listecase=[]
    c=25
    for i in range (len(liste)):
        case = Recherche(10,(i+1)*c+2,35,(2+i)*c-2,f'case{i}')#str(i)
        listecase.append(case)
    return listecase


def recherche():
    b=Recherche(10,50,200,90)
    while True:

        ev = donne_ev()
        tev = type_ev(ev)

        if tev == 'Touche':
            if touche(ev)== 'Return':
                efface_tout()
                return b.getRecherche()

            if 'Return' not in b.getRecherche():
                if touche(ev)== 'BackSpace':
                    x=b.getRecherche()[:-1]
                    b.initRecherche(x)

                elif touche(ev)== 'space':
                    b.setRecherche(' ')

                elif touche(ev)== 'Shift_R' or touche(ev)== 'Shift_L' or touche(ev)== 'Caps_Lock' :
                    pass

                else:
                    b.setRecherche(touche(ev))
                    #print(touche(ev))
                b.setBarre()

            if b.getLongueurrectangle()-20 < b.getTaillerecherche()[0] :
                x=b.getRecherche()[1:]
                b.initRecherche(x)

        if tev == 'Quitte':
            break

        mise_a_jour()

def recommancerRecherche(listerecherche,message,carte):
    texte(10,10,message)
    reche=recherche()
    if reche is None :
        return reche
    listesport=sport(carte) #liste des sport
    for i in listesport:
        if reche in i:
            listerecherche.append(i)

    if listerecherche==[]:
        efface_tout()
        return recommancerRecherche([],'aucune fédération, recommancer la recherche',carte)
    elif len(listerecherche)>20:
        efface_tout()
        return recommancerRecherche([],'précisez la recherche',carte)
    else:
        return listerecherche

def page_recherche(carte):
    listerecherche=recommancerRecherche([],'Recherche',carte)
    if listerecherche is None :
        return listerecherche
    condition=True
    lstbtn = affichebtn(listerecherche)
    while condition:
        ev = donne_ev()
        tev = type_ev(ev)

        tag , condition , federation = cliquebtn(lstbtn,tev)
        if condition is None:
            return condition
        """
        Permet de surligner en bleu
        """
        for i in range(len(lstbtn)):
            c = lstbtn[i].getChaine()
            xa,ya,xb,yb=lstbtn[i].getCord()
            t = lstbtn[i].getTag()
            efface('t'+str(t))
            if lstbtn[i].clique((abscisse_souris(),ordonnee_souris())) :
                    efface('t'+str(t))
                    Bouton(40,ya-3,str(c),'t'+str(t),"blue")
                    mise_a_jour()
            else:
                efface('t'+str(t))
        mise_a_jour()
    return federation


def infoclique(carte):

    info , listinfo = information(carte)
    lstbtn=affichebtn(info)
    lstcase=case(info)
    condition,casecliquee=True,lstcase[0]

    while condition :

        ev = donne_ev()
        tev = type_ev(ev)

        infocliquee, condition ,y = cliquebtn(lstbtn,tev,lstcase)
        if condition is None:
            return condition

        if not condition :
            casecliquee.setRemplissage()
            casecliquee = lstcase[int(infocliquee[1:])]
            casecliquee.setRemplissage('black')
            condition=True
            chaine=y

        if tev == 'Touche':
            if touche(ev)== 'Return':
                condition=False

        mise_a_jour()

    infochoisie=casecliqueedansliste(carte,chaine)
    return infochoisie


def fermerfenetre(estNone):
    if estNone is None:
        condition=True

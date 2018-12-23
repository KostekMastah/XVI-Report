import os

PATH_DO_FOLDERU_RAPORTY="C:/Weryfikacje XVI/Raporty/Roboczy"
daty=['2018-01-01','2018-12-01']
ŚREDNIA='=ŚREDNIA.JEŻELI(B8:B52;"<>")'
średnia_abs='=(SUMA.JEŻELI(B8:B52;">=0")-SUMA.JEŻELI(B8:B52;"<0"))/LICZ.JEŻELI(B8:B52;"<>")'
SD='{=ODCH.STANDARDOWE.A(JEŻELI(B8:B52 <> "";B8:B52;""))}'
max_ABS = '{=MAX(MODUŁ.LICZBY(B8:B52))}'


def mixer_raportow(sciezka_docelowa,daty):
    os.chdir(sciezka_docelowa)

    for file in os.listdir(sciezka_docelowa):
        if not file.startswith('raport XVI E1 '):
            continue
        else:
            plik1 = open(file,'r')
            plik2 = open(file.replace('E1', 'E2'),'r')
            try:

                lines1 = plik1.readlines()
                lines2 = plik2.readlines()

                mix = lines1[1:] + lines2[1:]
                mix.sort()

            except FileNotFoundError as e:
                print(e)
            try:
                plik1.close()
            except UnboundLocalError as e:
                print(e)
            try:
                plik2.close()
            except UnboundLocalError as e:
                print(e)

            file_rep = file.replace('raport XVI E1 ', 'Zbiorczy raport ')

            plik_raport = open(file_rep, 'w')
            plik_raport.write('sep=~\n')
            plik_raport.write(file.replace('raport XVI E1 ', 'Raport '))
            plik_raport.write(
                'Nazwisko~Imie~ID pacjenta~PTV~data~Pierwszy check~LAT[cm]~LONG[cm]~VERT[cm]~Komentarz~Margines(+)~Margines(-)~Unieruchomienie~Lokalizacja~Intencja' + '\n')
            plik_raport.writelines(mix)
            plik_raport.close()
            przypisanie_pacjentom_unieruchomien(sciezka_docelowa,file_rep,daty)


def wpisanie_dat(daty):
    daty[0] = input("Wpisz datę początkowa okresu(RRRR-MM-DD):")
    daty[1] = input("   Wpisz datę koncowa okresu(RRRR-MM-DD):")
    return daty


def is_werdykt(tekst):
    if tekst.startswith('nie') or tekst.startswith('bnie'):
        return False
    else:
        return True


def is_data(data_z_pliku,daty):
    if daty[0] <= data_z_pliku <= daty[1]:
        return True
    else:
        return False


def przypisanie_pacjentom_unieruchomien(sciezka_docelowa,file, daty):

    PLIK_WERYFIKACYJNY='Lista 63Gy'

    os.chdir(sciezka_docelowa)
    plik_pac = open(PLIK_WERYFIKACYJNY+'.csv','r')
    plik_rap = open(file)
    plik_save = open('save '+PLIK_WERYFIKACYJNY+' '+daty[0]+' '+daty[1]+'.csv','w')

    lines_pac = plik_pac.readlines()
    lines_rap = plik_rap.readlines()
    lines_rap = lines_rap[2:]
    marg_tabl = []

    liczba_wierszy=30
    etykieta=4

    for i in range(etykieta):
        marg_tabl.append('\n')

    for i in range(liczba_wierszy):
        marg_tabl.append('\n'+str(i+1))


    for pole in lines_pac:
        tablica=pole.split(';')
        i=0
        tablica_pacjenta=[]
        for a in range(liczba_wierszy):
            tablica_pacjenta.append('~~~')

        if is_werdykt(tablica[3]):
            marg_tabl[0] = marg_tabl[0] + '~' + tablica[1] + '~~~'
            marg_tabl[1] = marg_tabl[1] + '~' + tablica[0] + '~~~'


            marg_tabl[etykieta-1] = marg_tabl[etykieta-1] + '~Data~Lateral~Long~Vertical'
            nazwisko=''

            for xvi in lines_rap:
                xvi_tab=xvi.split('~')
                if tablica[1]==xvi_tab[2] and is_data(xvi_tab[4], daty):
                    tablica_pacjenta[i]=(xvi_tab[4]+'~' +xvi_tab[6]+ '~' +xvi_tab[7]+ '~' +xvi_tab[8])
                    nazwisko=xvi_tab[0]+' '+xvi_tab[1]

                    i+=1
            marg_tabl[2] = marg_tabl[2] + '~' + nazwisko + '~'
            marg_tabl[2] = marg_tabl[2] + '~' + tablica[2] + '~'

            wiersz=etykieta
            for record in tablica_pacjenta:
                marg_tabl[wiersz]=marg_tabl[wiersz]+'~'+record
                wiersz+=1

    plik_save.write('sep=~\n')
    plik_save.writelines(marg_tabl)

    plik_save.close()
    plik_pac.close()
    plik_rap.close()


#instancje funkcji
wpisanie_dat(daty)
mixer_raportow(PATH_DO_FOLDERU_RAPORTY , daty)
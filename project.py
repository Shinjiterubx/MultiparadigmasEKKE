import random
import base64

# Szükséges fileok: project.py, .env
# Readme.md Tartalmazza a program leírását.


# A program kezdéséhez szükséges eljárás, amit a menuben hívunk meg.

def game_start():
    while True:
        print("\033[1m\033[95mAz alábbi parancsok közül választhat:")
        print("\033[92mSTART \033[96m- kezdés | \033[92mHIGHSCORE \033[96m- ranglista | \033[92mEXIT \033[96m- kilépés")
        temp = input()


        if temp == "START" or temp == "HIGHSCORE" or temp == "EXIT":
            print("\n\n")
            return temp
        else:
            print("\n\n")
            print("Adjon meg egy érvényes parancsot!")

# A menü része a programnak, az eljárás kiértékeli a megadott választ.
# a user paraméter az adott felhasználó neve amit a program indulásakor kérünk be.

def menu(user):
    while True:
        choice = game_start()
        if choice == "START":
            save_game(user, open_game())
            
        if choice == "EXIT":
            print("A játék őn számára véget ért!")
            break
        if choice == "HIGHSCORE":
            open_leaderboard(user)
            

#Highscore elmentése, ahol a key a felhasználó neve, a value pedig az elért eredmémnye (status)

def save_game(key, value):
    # A dct változóba beleírjuk az összes mentést a .env fileból.
    dct = read_all()


    try:
        if str(value) >= dct[key]:
            # Ha  a pontszám nagyobb mint az elmentett akkor
            # dct dictionarynek beállítjuk az adott user nevére az elmentett pontszámot.
            dct[key] = str(value)
            write_all(dct)
    except Exception as e:
        # Ha nem lenne ilyen nevű érték (Nem játszott még a user) akkor szintén
        # dct dictionarynek beállítjuk az adott user nevére az elmentett pontszámot.
        dct[key] = str(value)
        write_all(dct)
    
# A HIGHSCORE bemenetnél használt eljárás aminek paraméterként a usert kell megadni.

def open_leaderboard(username):
    # Változó amiben eltároljuk a .env file tartalmát
    saves = read_all()

    # Try catch-el van lekezelve a pontszám kiírása, amennyiben az adott névhez nem található pontszám úgy, hibát dob.
    # Ez a hiba van lekezelve egy print kiírásával.
    try:
        print(f"{username} Legnagyobb pontszáma: {saves[username]}")
    except Exception as e:
        print("Nincs még elért pontszámod!")

# A read_all és a write_all függvények az órán írtak, nem történt rajtuk módosítás.

# ------------------------------------------------------------------------------------

def read_all() -> dict:
    ret = {}
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            try:
                [key, value] = line.rstrip().split("=", 1)
            except (ValueError):
                continue
            ret[key] = base64.b64decode(value.encode("utf-8")).decode("utf-8")
    return ret


def write_all(d: dict) -> None:
    with open(".env", "w", encoding="utf-8") as f:
        for k, v in d.items():
            cv = base64.b64encode(v.encode("utf-8")).decode("utf-8")
            f.write(f"{k}={cv}\n")


# ----------------------------------------------------------------------------------

# A fő játék megnyitása, ami csak switch case lényegében.

def open_game():
    # A status váltózó felel a jelenlegi állás elmentése érdekében.
    status = 0
    game = True
    #Végtelen iklus amiből akkor fogunk kilépni amennyiben veszítünk a játék során.
    while game:
        # A Felhasználó által megadott választás bekérése és eltárolása ideiglenes változóba.
        print("Add meg a válaszodat (KO - PAPIR - OLLO):")
        temp = input()

        #Felhasználó válaszának validálása.
        if temp == "KO" or temp == "PAPIR" or temp == "OLLO":
            # Generálunk egy random számot, ami az ellenfél válaszát imitálja
            # 1 == KO 2 == PAPIR 3 == OLLO a bot szemszögéből.
            bot_choice = random.randrange(1,3,1)
            
            # A switch_case része a programnak.
            if temp == "KO":
                if bot_choice == 2:
                    print("Az ellenfél válasza: PAPÍR\n")
                    game = False
                    break
                elif bot_choice == 3:
                    print("Az ellenfél válasza: OLLÓ")
                    print("+1 pontot kaptál.\n")
                    status += 1
                else:
                    print("Az ellenfél válasza: KŐ")
                    print("Döntetlen, nem kaptál pontot!\n")

            elif temp == "PAPIR":
                if bot_choice == 1:
                    print("Az ellenfél válasza: KŐ")
                    print("+1 pontot kaptál.\n")
                    status += 1
                elif bot_choice == 2:
                    print("Az ellenfél válasza: PAPÍR")
                    print("Döntetlen, nem kaptál pontot!\n")
                else:
                    print("Az ellenfél válasza: OLLÓ\n")
                    break
            else:
                if bot_choice == 1:
                    print("Az ellenfél válasza: KŐ\n")
                    game = False
                    break
                elif bot_choice == 2:
                    print("Az ellenfél válasza: PAPÍR")
                    print("+1 pontot kaptál!\n")
                    status += 1
                else:
                    print("Az ellenfél válasza: OLLÓ")
                    print("Döntetlen, nem kaptál pontot!\n")
                    game = False
                    break
        else:
            print("Helyes parancsot adj meg!\n")
    
    #Visszaadjuk az elért eredményt.

    print("\033[93mVesztettél!")
    print(f"\033[95mElért pontszám: {status} \n\n")

    return status
        
# A fő program futtatása:

if __name__ == "__main__":
    # Induláskor két sortörés, hogy elkülönüljön az előzőtől
    print("\n\n")
    # Bekérjük a felhasználó nevét
    print("\033[1m\033[95mAdd meg a neved:")
    user = input()
    # Meghívjuk a menu metódust a felhasználónévvel (user)
    menu(user)

from pymongo import MongoClient

# MongoDB adatbázis kapcsolat létrehozása
client = MongoClient("mongodb://localhost:27017/")

# Adatbázis kiválasztása
db = client["ISKOLA"]


def main():
    # Diákok lekérdezése az adatbázisból
    diakok_collection = db["Diakok"]
    diakok = diakok_collection.find()

    for diak in diakok:
        fizika_jegyek = [jegy["erdemjegy"] for jegy in diak["erdemjegyek"] if jegy["tantargy"] == "Fizika"]

        if fizika_jegyek:
            print(f"{diak['nev']} Fizika érdemjegyei:", ", ".join(map(str, fizika_jegyek)))

            # Érdemjegyek átlagának kiszámítása
            if len(fizika_jegyek) > 0:
                atlag = sum(fizika_jegyek) / len(fizika_jegyek)
                print(f"{diak['nev']} jegyek átlaga: {atlag:.1f}")
                print("-------------------------")
            else:
                print(f"{diak['nev']} nincs érdemjegy az átlaghoz.")
        else:
            print(f"{diak['nev']} Fizika érdemjegyei nem találhatóak.")


if __name__ == "__main__":
    main()

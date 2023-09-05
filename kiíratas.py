from pymongo import MongoClient

# MongoDB adatbázis kapcsolat létrehozása
client = MongoClient("mongodb://localhost:27017/")

# Adatbázis kiválasztása
db = client["ISKOLA"]


def main():
    # Diákok lekérdezése az adatbázisból
    diakok_collection = db["Diakok"]
    diak = diakok_collection.find_one({"nev": "Nagy Béla"})

    if diak:
        fizika_jegyek = diakok_collection.aggregate([
            {"$match": {"_id": diak["_id"]}},
            {"$unwind": "$erdemjegyek"},
            {"$match": {"erdemjegyek.tantargy": "Fizika"}},
            {"$project": {"_id": 0, "erdemjegy": "$erdemjegyek.erdemjegy"}}
        ])

        fizika_jegyek = [jegy["erdemjegy"] for jegy in fizika_jegyek]

        if fizika_jegyek:
            print("Nagy Béla Fizika érdemjegyei:", ", ".join(map(str, fizika_jegyek)))

            # Érdemjegyek átlagának kiszámítása
            if len(fizika_jegyek) > 0:
                atlag = sum(fizika_jegyek) / len(fizika_jegyek)
                print(f"Jegyek átlaga: {atlag:.1f}")
            else:
                print("Nincs érdemjegy az átlaghoz.")
        else:
            print("Nagy Béla Fizika érdemjegyei nem találhatóak.")
    else:
        print("Nagy Béla nem található az adatbázisban.")


if __name__ == "__main__":
    main()

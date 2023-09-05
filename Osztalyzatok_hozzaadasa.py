'''
Írj Python programot, amely az előzőleg létrehozott ISKOLA adatbázis Diákjait osztályozza
 a gyűjteményben szereplő tantárgyakból. A diákot, a tantárgyat és az érdemjegyet össze kell
 kötni és elmenteni a MongoDB adatbázisba.
'''
from pymongo import MongoClient

# MongoDB adatbázis kapcsolat létrehozása
client = MongoClient("mongodb://localhost:27017/")

# Adatbázis kiválasztása
db = client["ISKOLA"]


def main():
    # Diákok lekérdezése az adatbázisból
    diakok_collection = db["Diakok"]
    diakok = list(diakok_collection.find())
    # Diákok sorszámozása
    print("Diákok:")
    for idx, diak in enumerate(diakok, start=1):
        print(f"{idx}. {diak['nev']}")

    valasztott_diak_idx = int(input("Válasszon egy diák sorszámot: ")) - 1
    valasztott_diak = diakok[valasztott_diak_idx]

    print(f"Osztályzatok rögzítése a(z) {valasztott_diak['nev']} diáknak:")

    # Tantárgyak lekérdezése az adatbázisból
    tantargyak_collection = db["Tantargyak"]
    tantargyak = list(tantargyak_collection.find())

    erdemjegyek = []
    for tantargy in tantargyak:
        erdemjegy = int(input(f"Adja meg a(z) {tantargy['nev']} tantárgyhoz tartozó érdemjegyet (1-5): "))
        while erdemjegy < 1 or erdemjegy > 5:
            erdemjegy = int(input("Hibás érdemjegy. Adjon meg egy érvényes érdemjegyet (1-5): "))
        erdemjegyek.append({"tantargy": tantargy['nev'], "erdemjegy": erdemjegy})

    # Érdemjegyek mentése az adatbázisba
    if "erdemjegyek" in valasztott_diak:
        #A $push operátorral adjuk hozzá az új érdemjegyeket a meglévő érdemjegyekhez.
        # A $each operátorral megadhatjuk egy tömbben az új érdemjegyeket, amelyeket hozzá szeretnénk adni.
        diakok_collection.update_one({"_id": valasztott_diak["_id"]},
                                     {"$push": {"erdemjegyek": {"$each": erdemjegyek}}})
    else:
        diakok_collection.update_one({"_id": valasztott_diak["_id"]}, {"$set": {"erdemjegyek": erdemjegyek}})
    print("---------Érdemjegyek-------")
    # Diákok és érdemjegyek kiíratása az adatbázisból
    diakok = list(diakok_collection.find())
    for diak in diakok:
        erdemjegy_text = ', '.join([f"{jegy['tantargy']}: {jegy['erdemjegy']}" for jegy in diak.get("erdemjegyek", [])])
        print(f"{diak['nev']}: {erdemjegy_text if erdemjegy_text else 'Nincs érdemjegy'}")


if __name__ == "__main__":
    main()

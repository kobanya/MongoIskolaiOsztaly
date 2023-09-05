from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ISKOLA"]

diakok_collection = db["Diakok"]
tantargyak_collection = db["Tantargyak"]
erdemjegyek_collection = db["Erdemjegyek"]

if "Diakok" in db.list_collection_names() and "Tantargyak" in db.list_collection_names():
    print("Az adatbázis már létezik!")
else:
    diakok_collection.insert_many([
        {"nev": "Kiss Brigitta"},
        {"nev": "Nagy Béla"},
        {"nev": "Ferenczi Szabolcs"},
        {"nev": "Klein Noel"},
        {"nev": "Podhorszky Szilvia"},
        {"nev": "Matus Zsolt"},
        {"nev": "Harmati Vivien"},
        {"nev": "Láng Tamás"}
    ])

    tantargyak_collection.insert_many([
        {"nev": "Matematika"},
        {"nev": "Irodalom"},
        {"nev": "Földrajz"},
        {"nev": "Fizika"},
        {"nev": "Informatika"}
    ])

    print("Az adatbázis és a collection-ök létrehozva.")

    for diak in diakok_collection.find():
        for tantargy in tantargyak_collection.find():
            erdemjegyek_collection.insert_one({
                "diak_id": diak["_id"],
                "tantargy_id": tantargy["_id"]

            })

    print("Érdemjegyek hozzáadva.")

# Kiíratás
print("Diákok")
print("-----------------------------")
for diak in diakok_collection.find():
    diak_nev = diak["nev"]

    print(f"{diak_nev:<30}")


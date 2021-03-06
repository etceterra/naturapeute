"""
Import with the following command:

python manage.py shell -c "from src import mongo2pg; mongo2pg.import_all()"

"""
from datetime import date

from pymongo import MongoClient
from django.db import IntegrityError
from django.db.models import Q

from naturapeute.models import Therapist, Practice, Symptom, Synonym, Office, Patient
from blog.models import Article

client = MongoClient()
db = client.terrapeute

airtable_registry = {}
id_registry = {}


def import_practices():
    try:
        Practice.objects.all().delete()
    except Exception as e:
        print(str(e))
    for therapy in db.therapies.find():
        practice = Practice.objects.create(
            name=therapy["name"], slug=therapy["slug"]
        )
        airtable_registry[therapy.get("airtableId") or str(therapy["_id"])] = practice
        id_registry[str(therapy["_id"])] = practice

    print("practices imported")


def import_synonyms():
    try:
        Synonym.objects.all().delete()
    except Exception as e:
        print(str(e))
    counter = 0
    for synonym in db.synonyms.find():
        synonym = Synonym.objects.create(
            name=synonym["name"], words=' '.join(synonym["words"])
        )
        counter += 1
    print(f"{counter} synonyms imported")


symptoms = {}


def import_symptoms():
    try:
        Symptom.objects.all().delete()
    except Exception as e:
        print("error:" + str(e))
    for symptom in db.symptoms.find():
        if len(symptom["synonyms"]) == 1:
            symptom["synonyms"] = " ".split(symptom["synonyms"][0])
        instance = Symptom.objects.create(
            name=symptom["name"],
            synonyms=[x.strip() for x in symptom["synonyms"]],
            keywords=symptom["keywords"],
        )
        id_registry[str(symptom["_id"])] = instance
        airtable_registry[symptom["airtableId"]] = instance
    for symptom in db.symptoms.find():
        if symptom.get("airtableParentId"):
            instance = airtable_registry[symptom["airtableId"]]
            instance.parent = airtable_registry[symptom["airtableParentId"]]
            instance.save()
    print("symptoms imported")


def import_therapists():
    try:
        Therapist.mixed.all().delete()
    except Exception as e:
        print("error:" + str(e))
    for t in db.therapists.find():
        therapist = Therapist(
            slug=t["slug"],
            firstname=t["firstname"],
            lastname=t["lastname"],
            email=t.get("email"),
            phone=t["phone"].replace(" ", ""),
            is_certified=bool(t.get("isCertified")),
            description=t.get("description"),
            price=t.get("price"),
            timetable=t.get("timetable"),
            languages=t["languages"],
            photo=t.get("photo"),
            socials=t.get("socials"),
            agreements=t["agreements"],
            payment_types=t["paymentTypes"],
            membership="member",
        )
        therapist.save()
        therapist.creation_date = t["creationDate"]

        [
            therapist.practices.add(id_registry[str(k)])
            for k in t["therapies"]
            if str(k) in id_registry
        ]
        [
            therapist.symptoms.add(id_registry[str(k)])
            for k in t["symptoms"]
            if str(k) in id_registry
        ]

        for o in t["offices"]:
            office = Office.objects.create(
                street=o.get("street"),
                zipcode=o.get("zipCode"),
                city=o.get("city"),
                country=o.get("country"),
                pictures=o.get("pictures"),
                latlng=o.get("location")["coordinates"],
                therapist=therapist,
            )

        therapist.save()


def import_therapists_pending():
    for t in db.therapistpendings.find():
        try:
            Therapist.members.get(slug=t["slug"])
        except Therapist.DoesNotExist:
            pass
        else:
            continue
        name = t["name"].split(" ")
        therapist = Therapist(
            slug=t["slug"],
            firstname=name[0],
            lastname=" ".join(name[1:]),
            email=t.get("email"),
            phone=t["phone"].replace(" ", ""),
            is_certified=bool(t.get("isCertified")),
            description=t.get("description"),
            price=t.get("price"),
            timetable=t.get("timetable"),
            languages=t["languages"],
            photo=t.get("photo"),
            socials=t.get("socials"),
            agreements=t["agreements"],
            payment_types=t["paymentTypes"],
            membership="invitee",
        )
        therapist.save()
        therapist.creation_date = t["creationDate"]

        [
            therapist.practices.add(id_registry[str(k)])
            for k in t["therapies"]
            if str(k) in id_registry
        ]

        for o in t["offices"]:
            office = Office.objects.create(
                street=o.get("street"),
                zipcode=o.get("zipCode"),
                city=o.get("city"),
                country=o.get("country"),
                pictures=o.get("pictures"),
                latlng=o.get("location")["coordinates"],
                therapist=therapist,
            )

        therapist.save()

    print("therapists imported")


def import_articles():
    Article.objects.all().delete()
    for article in db.articles.find():
        instance = Article(
            title=article["title"],
            slug=article["slug"],
            body=article["body"],
            image=article.get("image"),
        )
        instance.save()

        instance.creation_date = article["creationDate"]
        instance.save()

    print("articles imported")


def import_patients():
    Patient.objects.all().delete()
    for extra in db.therapistdatas.find():
        t = db.therapists.find_one({ "airtableId": extra["therapistAirtableId"] })
        if not t: continue
        print("therapist:", t["lastname"], t["firstname"])
        therapist = Therapist.mixed.get(lastname=t["lastname"], firstname=t["firstname"])

        data =  extra["data"]
        therapist.invoice_data = {
            "hourly_price": data["servicePrice"],
            "services": data["preferredServices"],
            "author": {
                "name": data["author"]["name"],
                "email": data["author"]["email"],
                "phone": data["author"]["phone"],
                "zipcode": data["author"]["ZIP"],
                "city": data["author"]["city"],
                "street": data["author"]["street"],
                "rcc": data["author"]["RCC"],
                "iban": data["author"]["IBAN"],
            },
            "therapist": {
                "firstname": data["therapist"]["firstName"],
                "lastname": data["therapist"]["lastName"],
                "street": data["therapist"]["street"],
                "zipcode": data["therapist"]["ZIP"],
                "city": data["therapist"]["city"],
                "phone": data["therapist"]["phone"],
                "rcc": data["therapist"]["RCC"],
            }
        }
        therapist.save()

        for patient in data["patients"]:
            gender = "man" if patient["gender"] == "male" else "woman"
            try:
                zipcode = int(patient["ZIP"])
            except:
                zipcode = None
            patient = Patient.objects.create(
                firstname=patient["firstName"],
                lastname=patient["lastName"],
                street=patient["street"],
                zipcode=zipcode,
                city=patient["city"],
                canton=patient["canton"],
                gender=gender,
                birthdate=date.fromtimestamp(patient["birthday"] / 1000),
                email=patient["email"],
            )
            therapist.patients.add(patient)


def import_all():
    # import_practices()
    # import_symptoms()
    # import_synonyms()
    # import_therapists()
    # import_therapists_pending()
    # import_patients()
    import_articles()

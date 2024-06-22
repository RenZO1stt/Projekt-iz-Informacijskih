from pony.orm import Database, Required, PrimaryKey

db = Database()

class Artikl(db.Entity):
    id = PrimaryKey(int, auto=True)
    vrsta = Required(str)
    materijal = Required(str)
    velicina = Required(str)
    boja = Required(str)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
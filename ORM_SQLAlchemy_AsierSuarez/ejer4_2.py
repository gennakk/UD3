def medalla():
    from sqlalchemy import create_engine
    from ejer4tablas import Olimpiada, Deportista, Evento, Participacion
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///database.db')

    Session = sessionmaker(bind=engine)
    session = Session()

    nom = input("Introduce el nombre de un deportista: ")
    nom = "%"+nom+"%"

    q = session.query(Deportista).filter(Deportista.nombre.like(nom))
    print("Elige al deportista por su id")
    for deportista in q:
        print("\t{0}: {1}".format(deportista.id_deportista,deportista.nombre))
    id_deportista = input("  > ")

    q = session.query(Participacion,Evento,Olimpiada).filter(
        Evento.id_evento==Participacion.id_evento,
        Olimpiada.id_olimpiada==Evento.id_olimpiada,
        Participacion.id_deportista==id_deportista
    )
    print("Elige un evento por su id")
    for pa,ev,ol in q:
        print("\t{0}: {1} ({2}, {3}), {4}".format(ev.id_evento,ev.nombre,ol.nombre,ol.ciudad,pa.medalla))
    id_evento = input("  > ")

    medalla = input("Introduce la nueva medalla (Gold,Silver,Bronze): ")
    if medalla!="Gold" and medalla!="Silver" and medalla!="Bronze":
        medalla = None

    session.query(Participacion).filter(Participacion.id_deportista==id_deportista,Participacion.id_evento==id_evento)\
        .update({Participacion.medalla:medalla}, synchronize_session = False)
    #q.medalla = medalla
    session.commit()

    session.close()
def delete():
    from sqlalchemy import create_engine
    from ejer4tablas import Olimpiada, Deporte, Deportista, Evento, Equipo, Participacion
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

    q = session.query(Participacion,Evento,Olimpiada,Deportista).filter(
        Evento.id_evento==Participacion.id_evento,
        Olimpiada.id_olimpiada==Evento.id_olimpiada,
        Deportista.id_deportista==Participacion.id_deportista,
        Participacion.id_deportista==id_deportista
    )
    resultados = q.count()
    if (resultados==1):
        for pa,ev,ol,de in q:
            print("{0} ({1}, {2}), {3}".format(ev.nombre,ol.nombre,ol.ciudad,pa.medalla))
            borrar = input("¿Desea borrar esta participación junto a su deportista? (s/N): ")
            if (borrar.lower()=="s"):
                session.delete(pa)
                session.delete(de)
                print("Deportista y participacion borradas")
            break
    else:
        print("Elige un evento por su id para borrarlo")
        for pa,ev,ol,de in q:
            print("\t{0}: {1} ({2}, {3}), {4}".format(pa.id_evento,ev.nombre,ol.nombre,ol.ciudad,pa.medalla))
        id_evento = input("  > ")

        q = session.query(Participacion).filter(
            Participacion.id_deportista==id_deportista,
            Participacion.id_evento==id_evento
        )
        for participacion in q:
            session.delete(participacion)

    session.commit()
    session.close()
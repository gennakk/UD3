def participantes():
    from sqlalchemy import create_engine
    from ejer4tablas import Olimpiada, Deporte, Deportista, Evento, Equipo, Participacion
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///database.db')

    Session = sessionmaker(bind=engine)
    session = Session()

    temporada = input("Indica la edición olímpica (S/W): ")
    while True:
        if temporada.lower()!="s" and temporada.lower()!="w":
            temporada = input("Por favor, indica la edición olímpica (S/W): ")
        else:
            if temporada.lower()=="s":
                temporada = "Summer"
            else:
                temporada = "Winter"
            break

    q = session.query(Olimpiada).filter(Olimpiada.temporada==temporada)
    print("Elige una edición olímpica introduciendo su numero")
    for olimpiada in q:
        print("\t{0}: {1}, {2}".format(olimpiada.id_olimpiada,olimpiada.nombre,olimpiada.ciudad))
    id_olimpiada = input("  > ")

    q = session.query(Deporte).filter(Evento.id_olimpiada==id_olimpiada,Evento.id_deporte==Deporte.id_deporte)
    print("Elige un deporte por su id")
    for deporte in q:
        print("\t{0}: {1}".format(deporte.id_deporte,deporte.nombre))
    id_deporte = input("  > ")

    q = session.query(Evento).filter(Evento.id_olimpiada==id_olimpiada,Evento.id_deporte==id_deporte)
    print("Selecciona un evento por su id")
    for evento in q:
        print("\t{0}: {1}".format(evento.id_evento,evento.nombre))
    id_evento = input("  > ")

    q = session.query(Olimpiada,Deporte,Evento,Deportista,Participacion,Equipo).filter(
        Olimpiada.id_olimpiada==Evento.id_olimpiada,
        Deporte.id_deporte==Evento.id_deporte,
        Equipo.id_equipo==Participacion.id_equipo,
        Deportista.id_deportista==Participacion.id_deportista,
        Evento.id_evento==Participacion.id_evento,
        Evento.id_evento==id_evento
    )
    i = True
    for ol,de,ev,da,pa,eq in q:
        if i:
            print("\n\033[1m{0}: {1} ({2}, {3})\033[0m".format(de.nombre,ev.nombre,ol.nombre,ol.ciudad))
            i = False
        print("\t{0}: {1}cm {2}kg, {3} años, {4} ({5})".format(da.nombre,da.peso,da.altura,pa.edad,eq.nombre,pa.medalla))

    session.close()
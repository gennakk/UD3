def add():
    from sqlalchemy import create_engine
    from ejer4tablas import Olimpiada, Deporte, Deportista, Evento, Equipo, Participacion
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///database.db')

    Session = sessionmaker(bind=engine)
    session = Session()

    nom = input("Introduce el nombre de un deportista: ")
    nompor = "%" + nom + "%"

    q = session.query(Deportista).filter(Deportista.nombre.like(nompor))
    resultados = q.count()
    if resultados==0:
        sexo = input("Indica el sexo (M/F): ")
        while True:
            sexo=sexo.upper()
            if sexo!="M" and sexo!="F":
                sexo = input("Por favor, indica el sexo (M/F): ")
            else:
                break

        peso = input("Pon su peso (solo numeros): ")
        altura = input("Pon su altura (solo numeros): ")

        deportista = Deportista(nombre=nom, sexo=sexo, peso=peso, altura=altura)
        session.add(deportista)
        session.commit()

        q = session.query(Deportista.id_deportista).filter(Deportista.nombre==nom)
        id_deportista = -1
        for deportista in q:
            id_deportista = deportista.id_deportista

    else:
        print("Elige al deportista por su id")
        for deportista in q:
            print("\t{0}: {1}".format(deportista.id_deportista, deportista.nombre))
        id_deportista = int(input("  > "))

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

    q = session.query(Olimpiada).filter(Olimpiada.temporada.like(temporada))
    print("Elige una edición olímpica introduciendo su numero")
    for olimpiada in q:
        print("\t{0}: {1}, {2}".format(olimpiada.id_olimpiada,olimpiada.nombre,olimpiada.ciudad))
    id_olimpiada = input("  > ")

    q = session.query(Deporte).filter(Evento.id_deporte==Deporte.id_deporte,Evento.id_olimpiada==id_olimpiada)
    print("Elige un deporte por su id")
    for deporte in q:
        print("\t{0}: {1}".format(deporte.id_deporte,deporte.nombre))
    id_deporte = input("  > ")

    q = session.query(Evento).filter(Evento.id_deporte==id_deporte,Evento.id_olimpiada==id_olimpiada)
    print("Selecciona un evento por su id")
    for evento in q:
        print("\t{0}: {1}".format(evento.id_evento,evento.nombre))
    id_evento = input("  > ")

    edad = input("Introduce su edad (solo numeros): ")

    #!!!!!!!!!!!!!!!!sql = "SELECT DISTINCT e.id_equipo, e.nombre FROM Equipo e"
    q = session.query(Equipo)
    print("Selecciona un equipo por su id")
    for equipo in q:
        print("\t{0}: {1}".format(equipo.id_equipo,equipo.nombre))
    id_equipo = input("  > ")

    medalla = input("Introduce la nueva medalla (Gold,Silver,Bronze): ")
    if medalla!="Gold" and medalla!="Silver" and medalla!="Bronze":
        medalla = None

    participacion = Participacion(
        id_deportista=id_deportista,
        id_evento=id_evento,
        id_equipo=id_equipo,
        edad=edad,
        medalla=medalla
    )
    session.add(participacion)
    session.commit()
    print("Participacion añadida con exito")

    session.close()
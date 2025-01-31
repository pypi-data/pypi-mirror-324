class Course:

    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link

    def __repr__(self):
        return f'\nCurso: {self.name}\nDurantion: {self.duration}\nLink: {self.link}\n'

courses = [
    Course("Introduccion al Linux", 25, "https://hack4u.io/cursos/introduccion-a-linux/"),
    Course("Personalización de Linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/"),
    Course("Introduccion al Hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/"),
    Course("Python Ofensivo", 35, "https://hack4u.io/cursos/python-ofensivo/")

]

def listar():
    for x in courses:
        print(x)

def buscar(name):
    for x in courses:
        if x.name == name:
            return x
    return "No hay ningun curso con ese nombre"


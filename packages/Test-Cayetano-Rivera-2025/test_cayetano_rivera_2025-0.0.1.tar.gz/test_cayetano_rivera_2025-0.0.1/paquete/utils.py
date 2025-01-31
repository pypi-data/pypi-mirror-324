from courses import courses

def duracion():
    return (sum(x.duration for x in courses))

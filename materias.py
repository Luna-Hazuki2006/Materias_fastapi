from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, field_validator
from datetime import datetime

class Nivel(BaseModel): 
    ID : str
    nombre : str
    descripcion : str | None = None

class Profesor(BaseModel): 
    CEDULA : str
    nombres : str
    apellidos : str
    nacimiento : datetime
    inicioLaboral : datetime
    telefono : str
    direccion : str
    nivel : Nivel
    años : int
    @field_validator('años')
    def cantidades(cls, años): 
        if años < 0: raise ValueError('La cantidad de años de trabajo no puede ser negativa')
        return años

class Materia(BaseModel): 
    ID : str
    nombre : str
    contenido : str
    nivel : Nivel
    costo : float
    profesores : list[Profesor] = []
    carga : int
    prerrequisitos : list = []

materias : list[Materia] = []
profesores : list[Profesor] = []
niveles : list[Nivel] = []

app = FastAPI()

@app.get('/profesores', status_code=status.HTTP_302_FOUND)
async def listar_profesores(): 
    return profesores

@app.post('/profesor', status_code=status.HTTP_201_CREATED)
async def agregar_profesor(profesor : Profesor):
    for este in profesores: 
        if este.CEDULA == profesor.CEDULA: 
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                detail={'mensaje': 'No puede existir un profesor con la misma cédula'}
            )
    profesores.append(profesor)
    return profesor

@app.get('/niveles', status_code=status.HTTP_302_FOUND)
async def listar_niveles(): 
    return niveles

@app.post('/nivel', status_code=status.HTTP_201_CREATED)
async def crear_nivel(nivel : Nivel): 
    for este in niveles: 
        if este.ID == nivel.ID: 
            print(niveles)
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                detail={'mensaje': 'No puede existir un nivel con la misma id'}
            )
    niveles.append(nivel)
    return nivel

@app.get('/materias', status_code=status.HTTP_302_FOUND)
async def listar_materias(): 
    return materias

@app.get('/materia/{id}', status_code=status.HTTP_302_FOUND)
async def obtener_materia(id : str): 
    for este in materias: 
        if este.ID == id: return este
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail={'mensaje': 'No se pudo encontrar una materia con esa id'}
    )

@app.post('/materia', status_code=status.HTTP_201_CREATED)
async def crear_materia(materia : Materia): 
    for este in materias: 
        if este.ID == materia.ID: 
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                detail={'mensaje': 'No puede existir una materia con la misma id'}
            )
    materias.append(materia)
    return materia

@app.put('/materia/{id}', status_code=status.HTTP_202_ACCEPTED)
async def modificar_materia(id : str, materia : Materia): 
    for i in range(len(materias)): 
        este = materias[i]
        if este.ID == id: 
            if id == materia.ID: 
                materias[i] = materia
                return materias[i]
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                detail={'mensaje': 'La id de la materia no es la misma a la del parámetro'}
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail={'mensaje': 'No existe una materia con esa id'}
    )

@app.delete('/materia/{id}', status_code=status.HTTP_202_ACCEPTED)
async def eliminar_materia(id): 
    for i in range(len(materias)): 
        if materias[i].ID == id: 
            este = materias[i]
            materias.remove(materias[i])
            return este
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail={'mensaje': 'No se pudo encontrar una materia con esa id'}
    )
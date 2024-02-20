"""from fastapi import FastAPI, HTTPException, Depends


from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

DATABASE_URL = "postgresql+psycopg2://user:password@postgres:5432/petroli_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Definición del modelo de datos
class Telemetry(Base):
    __tablename__ = "telemetry"
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer)
    pressure = Column(Float)
    temperature = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Creación de la tabla
Base.metadata.create_all(bind=engine)

# Modelo Pydantic para la recopilación de datos
class TelemetryCreate(BaseModel):
    asset_id: int
    pressure: float
    temperature: float

# Ruta para recopilar datos de telemetría
@app.post("/telemetry")
async def collect_telemetry(telemetry: TelemetryCreate, db: Session = Depends(get_db)):
    db_telemetry = Telemetry(**telemetry.dict())
    db.add(db_telemetry)
    db.commit()
    db.refresh(db_telemetry)
    return {"message": "Telemetry data collected successfully"}

# Ruta para obtener datos de telemetría
@app.get("/telemetry/{asset_id}")
async def get_telemetry(asset_id: int, db: Session = Depends(get_db)):
    telemetry_data = db.query(Telemetry).filter(Telemetry.asset_id == asset_id).all()
    return telemetry_data

"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from peewee import Model, MySQLDatabase, CharField, FloatField, DateTimeField
from datetime import datetime
from typing import List

# Configuración de la base de datos
database = MySQLDatabase('petroli_database', user='root', password='', host='localhost', port=3306)

# Definición de modelos
class SensorData(Model):
    sensor_id = CharField(max_length=50)
    pressure = FloatField()
    flow = FloatField()
    temperature = FloatField()
    storage_level = FloatField()
    timestamp = DateTimeField(default=datetime.now)

    class Meta:
        database = database

# Crear tablas
database.connect()
database.create_tables([SensorData])

# Inicializar la aplicación FastAPI
app = FastAPI()

# Definición de modelos Pydantic
class SensorDataCreate(BaseModel):
    sensor_id: str
    pressure: float
    flow: float
    temperature: float
    storage_level: float

class SensorDataResponse(SensorDataCreate):
    timestamp: datetime

@app.get('/')
async def index():
  return 'PETROLI API CC COPYRIGHT 2024 geneyesis'

# Rutas de la API
@app.post("/sensor-data/", response_model=SensorDataResponse)
async def create_sensor_data(data: SensorDataCreate):
    new_data = SensorData.create(**data.dict())
    return {**data.dict(), "timestamp": new_data.timestamp}

@app.get("/sensor-data/", response_model=List[SensorDataResponse])
async def read_sensor_data(start_date: datetime = Query(...), end_date: datetime = Query(...)):
    query = SensorData.select().where((SensorData.timestamp >= start_date) & (SensorData.timestamp <= end_date))
    data = [{"sensor_id": entry.sensor_id, "pressure": entry.pressure, "flow": entry.flow,
             "temperature": entry.temperature, "storage_level": entry.storage_level, "timestamp": entry.timestamp}
            for entry in query]
    return data





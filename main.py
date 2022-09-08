import asyncio
from contextlib import contextmanager

import typer
from kasa import Discover
from pydantic import BaseModel
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///D:/DevCode/PyKasa/sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def get_db():
    """Session Management for DB

    Yields:
        SQLAlchemy session: DB Session
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


class Device(Base):
    """Model Representation of Device

    Args:
        Base ( SQLAlchemy ): SQL Alchemy Base Model
    """

    __tablename__ = "device_list"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Integer, unique=True, index=True)
    ip = Column(String, unique=True)


class DeviceBase_Schm(BaseModel):
    """Validation for Records

    Args:
        BaseModel ( Pydantic Base Model): Pydantic Schema
    """

    name: str
    ip: str


class Device_Schm(DeviceBase_Schm):
    """Validation for Records

    Args:
        DeviceBase_Schm ( Pydantic Model): Pydantic Schema
    """

    id: int

    class Config:
        orm_mode = True


app = typer.Typer()

console = Console()

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def create_device_db(db: Session, device_create: DeviceBase_Schm):
    """Insert validated record into DB

    Args:
        db (Session): Session passed as contex
        device_create (DeviceBase_Schm): Pydantic validated record

    Returns:
        _type_: _description_
    """
    db_device = Device(name=device_create.name, ip=device_create.ip)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def list_all_devices(
    db: Session, skip: int = 0, limit: int = 100
) -> list[Device]:
    """Returns all device records in db

    Args:
        db (Session): Session Context Manager
        skip (int, optional): How many records to skip. Defaults to 0.
        limit (int, optional): Limit of Recoreds returned. Defaults to 100.

    Returns:
        List[SQLAlchemy Model]: Model Representation of all devices in db
    """
    return db.query(Device).offset(skip).limit(limit).all()


def get_device_ip(db: Session, id: int) -> Device:
    """Return IP of device from id

    Args:
        db (Session): DB session passed using context
        id (int): ID of object to get id of

    Returns:
        SQLAlchemy Model : SQLAlchemy Model Single Record
    """
    return db.query(Device).filter_by(id=id).first()


@app.command()
def create_new_device(name: str, ip_addr: str):
    """Creates a new device in the DB

    Args:
        name (str): Name to assing device
        ip_addr (str): IP address of device
    """
    data_packet = {"name": name, "ip": ip_addr}
    data_input = DeviceBase_Schm(**data_packet)
    with get_db() as db:
        create_device_db(db, data_input)


# TODO: write docstring
@app.command()
def get_all_devices():
    """Display a list of all devices to terminal"""
    with get_db() as db:
        devs = list_all_devices(db)
        table = Table("Name", "IP", "ID")
        for dev in devs:
            disp = Device_Schm.from_orm(dev)
            table.add_row(disp.name, str(disp.ip), str(disp.id))
        console.log("🚀 ~ file: main.py ~ line 176 ~ table", table)
        console.print(table)


@app.command()
def get_one_device(id: int):
    """Acquire a device on its id

    Args:
        id (int): id of device to get
    """
    with get_db() as db:
        dev = get_device_ip(db, id)
        disp = Device_Schm.from_orm(dev)
        console.log("🚀 ~ file: main.py ~ line 190 ~ disp", disp)


async def aturn_off(ip):
    dev = await Discover.discover_single(host=ip)
    await dev.update()
    await dev.turn_off()
    return dev


@app.command()
def turn_off_device(id: int):
    """Turn off a device based on its id

    Args:
        id (int): id of device to turn off
    """
    with get_db() as db:
        dev = get_device_ip(db, id)
        disp = Device_Schm.from_orm(dev)
    console.log(disp.ip)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Exec Command", total=None)
        res = asyncio.run(aturn_off(disp.ip))
        console.log("🚀 ~ file: main.py ~ line 198 ~ res", res)


async def aturn_on(ip):
    dev = await Discover.discover_single(host=ip)
    await dev.update()
    await dev.turn_on()
    return dev


@app.command()
def turn_on_device(id: int):
    """Turn on a device based on its id

    Args:
        id (int): id of device to turn off
    """
    with get_db() as db:
        dev = get_device_ip(db, id)
        disp = Device_Schm.from_orm(dev)
    console.log(disp.ip)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Exec Command", total=None)
        res = asyncio.run(aturn_on(disp.ip))
        console.log("🚀 ~ file: main.py ~ line 227 ~ res", res)


@app.command()
def version():
    """Get program version number"""
    print("1.0")


if __name__ == "__main__":
    app()

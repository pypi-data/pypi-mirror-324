from sqlalchemy import Column, Float, Integer, String, TIMESTAMP,DateTime, Text, ForeignKey, Boolean,Index
from sqlalchemy.orm import Mapped, mapped_column,DeclarativeBase,relationship
from pgvector.sqlalchemy import Vector


# Define the base class
class Base(DeclarativeBase):
    pass
    
# Define the models
# Flight Information Table
class FlightInfo(Base):
    __tablename__ = "flight_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(DateTime, nullable=False)
    start_time = Column(String, nullable=False)
    start_location = Column(String(255), nullable=False)
    end_date = Column(DateTime, nullable=False)
    end_time = Column(String, nullable=False)
    end_location = Column(String(255), nullable=False)
    fleet = Column(String(255), nullable=False)
    aircraft = Column(String(255), nullable=False)
    foqa_status = Column(String(255), nullable=False)
    departure = Column(String(255), nullable=False)
    departure_rwy = Column(String(255), nullable=False)
    dep_datetime = Column(DateTime, nullable=False)
    arrival = Column(String(255), nullable=False)
    arrival_rwy = Column(String(255), nullable=False)
    arr_datetime = Column(DateTime, nullable=False)
    foqa_comment = Column(String(255), nullable=True)
    flight_number = Column(String(255), nullable=True)
    metar_departure = Column(String(255), nullable=True)
    metar_arrival = Column(String(255), nullable=True)
    start_airport_name = Column(String(255), nullable=True)
    start_airport_country = Column(String(255), nullable=True)
    start_airport_latitude = Column(Float)
    start_airport_longitude = Column(Float)
    start_airport_elevation = Column(Integer)
    end_airport_name = Column(String(255), nullable=True)
    end_airport_country = Column(String(255), nullable=True)
    end_airport_latitude = Column(Float)
    end_airport_longitude = Column(Float)
    end_airport_elevation = Column(Integer)
    start_airport_iata_id = Column(String, nullable=True)
    start_airport_runways = Column(String, nullable=True)
    end_airport_iata_id = Column(String, nullable=True)
    end_airport_runways = Column(String, nullable=True)
    type = Column(String(255), nullable=True)
    flight_key = Column(String, unique=True, index=True)
    embedding_ada002: Mapped[Vector] = mapped_column(Vector(1536), nullable=True)  # ada-002
    embedding_nomic: Mapped[Vector] = mapped_column(Vector(768), nullable=True)  # nomic-embed-text

     # One-to-Many: One Flight can have many Events
    events: Mapped["EventData"] = relationship("EventData", back_populates="flight_info", cascade="all, delete-orphan")

    # One-to-One: One Flight can have one Risk Data
    risk_data: Mapped["RiskData"] = relationship("RiskData", back_populates="flight_info", uselist=False)

    def __repr__(self):
        return f"<FlightInfo(flight_number={self.flight_number}, start_location={self.start_location}, end_location={self.end_location})>"

    def to_dict(self, include_embedding: bool = False):
        model_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        if include_embedding:
            model_dict["embedding_ada002"] = model_dict.get("embedding_ada002", [])
            model_dict["embedding_nomic"] = model_dict.get("embedding_nomic", [])
            
        else:
            model_dict.pop("embedding_ada002", None)
            model_dict.pop("embedding_nomic", None)
        return model_dict

    def to_str_for_rag(self):
        return f"Flight Number: {self.flight_number} Start Location: {self.start_location} " \
               f"End Location: {self.end_location} Departure: {self.departure} Arrival: {self.arrival}"

    def to_str_for_embedding(self):
        return f"Flight Number: {self.flight_number} Start Location: {self.start_location} Fleet:{self.fleet} FOQA Status: {self.foqa_status} " \
               f"Type: {self.type} End Location: {self.end_location} Departure: {self.departure} Arrival: {self.arrival}"


# Event Data (TimescaleDB Hypertable)
class EventData(Base):
    __tablename__ = "event_data"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=False)
    event_id: Mapped[float] = mapped_column(Float, nullable=False)
    filtered: Mapped[String] = mapped_column(String(255), nullable=False)
    phase: Mapped[String] = mapped_column(String(255), nullable=False)
    reason: Mapped[String] = mapped_column(Text, nullable=False)
    reason_comment: Mapped[String] = mapped_column(Text, nullable=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    deviation_category: Mapped[String] = mapped_column(String(255), nullable=False)
    deviation: Mapped[String] = mapped_column(String(255), nullable=False)
    deviation_value: Mapped[float] = mapped_column(Float, nullable=False)
    name_value_pairs: Mapped[Text] = mapped_column(Text, nullable=False)
    invalidated_event: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    embedding_ada002: Mapped[Vector] = mapped_column(Vector(1536), nullable=True)  # ada-002
    embedding_nomic: Mapped[Vector] = mapped_column(Vector(768), nullable=True)

    # Foreign Key to FlightInfo using flight_id (correct reference)
    flight_id: Mapped[int] = mapped_column(ForeignKey("flight_info.id"))


    # Define the reverse relationship
    flight_info: Mapped["FlightInfo"] = relationship("FlightInfo", back_populates="events")

    @staticmethod
    def create_hypertable(engine):
        with engine.connect() as conn:
            conn.execute("SELECT create_hypertable('event_data', 'time');")

    def __repr__(self):
        return f"<EventData(event_id={self.event_id}, deviation={self.deviation}, level={self.level})>"

    def to_dict(self, include_embedding: bool = False):
        model_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        if include_embedding:
            model_dict["embedding_ada002"] = model_dict.get("embedding_ada002", [])
            model_dict["embedding_nomic"] = model_dict.get("embedding_nomic", [])
        else:
            model_dict.pop("embedding_ada002", None)
            model_dict.pop("embedding_nomic", None)
        return model_dict

    def to_str_for_rag(self):
        return f"Event ID: {self.event_id}, Deviation: {self.deviation}, Level: {self.level}"

# Risk Data Table
class RiskData(Base):
    __tablename__ = "risk_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    month_name = Column(String(255), nullable=False)
    end_month = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)
    severity = Column(Float, nullable=False)
    probability = Column(Float, nullable=False)
    risk_index = Column(Float, nullable=False)
    embedding_ada002: Mapped[Vector] = mapped_column(Vector(1536), nullable=True)  # ada-002
    embedding_nomic: Mapped[Vector] = mapped_column(Vector(768), nullable=True)   

    # One-to-One Foreign Key to FlightInfo
    flight_id: Mapped[int] = mapped_column(ForeignKey("flight_info.id"), unique=True)

    # Define the reverse relationship
    flight_info: Mapped["FlightInfo"] = relationship("FlightInfo", back_populates="risk_data")

    def __repr__(self):
        return f"<RiskData(month={self.month}, year={self.year}, severity={self.severity}, probability={self.probability})>"
    
    def to_dict(self, include_embedding: bool = False):
        model_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        if include_embedding:
            model_dict["embedding_ada002"] = model_dict.get("embedding_ada002", [])
            model_dict["embedding_nomic"] = model_dict.get("embedding_nomic", [])
        else:
            model_dict.pop("embedding_ada002", None)
            model_dict.pop("embedding_nomic", None)
        return model_dict

    def to_str_for_rag(self):
        return f"Month: {self.month_name}, Year: {self.year}, Severity: {self.severity}, Probability: {self.probability}"

    def to_str_for_embedding(self):
        return f"Severity: {self.severity}, Probability: {self.probability}, Risk Index: {self.risk_index}"

    # Define HNSW indexes for vector similarity search
index_ada002 = Index(
    "hnsw_index_for_innerproduct_flightinfo_embedding_ada002",
    FlightInfo.embedding_ada002,
    postgresql_using="hnsw",
    postgresql_with={"m": 16, "ef_construction": 64},
    postgresql_ops={"embedding_ada002": "vector_ip_ops"},
)

index_nomic = Index(
    "hnsw_index_for_innerproduct_flightinfo_embedding_nomic",
    FlightInfo.embedding_nomic,
    postgresql_using="hnsw",
    postgresql_with={"m": 16, "ef_construction": 64},
    postgresql_ops={"embedding_nomic": "vector_ip_ops"},
)

# Define HNSW indexes for vector similarity search on EventData and RiskData
index_eventdata_ada002 = Index(
    "hnsw_index_for_innerproduct_eventdata_embedding_ada002",
    EventData.embedding_ada002,
    postgresql_using="hnsw",
    postgresql_with={"m": 16, "ef_construction": 64},
    postgresql_ops={"embedding_ada002": "vector_ip_ops"},
)

index_eventdata_nomic = Index(
    "hnsw_index_for_innerproduct_eventdata_embedding_nomic",
    EventData.embedding_nomic,
    postgresql_using="hnsw",
    postgresql_with={"m": 16, "ef_construction": 64},
    postgresql_ops={"embedding_nomic": "vector_ip_ops"},
)

index_riskdata_ada002 = Index(
    "hnsw_index_for_innerproduct_riskdata_embedding_ada002",
    RiskData.embedding_ada002,
    postgresql_using="hnsw",
    postgresql_with={"m": 16, "ef_construction": 64},
    postgresql_ops={"embedding_ada002": "vector_ip_ops"},
)

index_riskdata_nomic = Index(
    "hnsw_index_for_innerproduct_riskdata_embedding_nomic",
    RiskData.embedding_nomic,
    postgresql_using="hnsw",
    postgresql_with={"m": 16, "ef_construction": 64},
    postgresql_ops={"embedding_nomic": "vector_ip_ops"},
)
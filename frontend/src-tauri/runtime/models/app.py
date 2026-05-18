from sqlalchemy import Column, Integer, String, Text, DateTime, func, Boolean
from models import Base

class InstalledApp(Base):
    __tablename__ = "installed_apps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    app_id = Column(String(128), nullable=False)
    display_name = Column(String(128), default="")
    installed_at = Column(DateTime, server_default=func.now())
    config_json = Column(Text, default="{}")

class AppDefinition(Base):
    __tablename__ = "app_definitions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id = Column(String(128), unique=True, nullable=False)
    name = Column(String(128), nullable=False)
    tagline = Column(String(256), default="")
    description = Column(Text, default="")
    icon = Column(String(32), default="🤖")
    category = Column(String(64), default="工具")
    color = Column(String(64), default="from-blue-500 to-indigo-600")
    author = Column(String(64), default="Aible OS")
    is_builtin = Column(Boolean, default=True)
    app_file = Column(String(256), default="")
    created_at = Column(DateTime, server_default=func.now())

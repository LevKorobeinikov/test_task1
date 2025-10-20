from app.core.db import Base


class BaseModel(Base):
    """
    Абстрактная базовая модель для моделей.
    """

    __abstract__ = True

    def __repr__(self):
        return f"{type(self).__name__}({self.id=}, "

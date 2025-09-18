from pydantic import BaseModel, Field

class Data(BaseModel):
    MessagesActualLength: int
    WarningsActualLength: int
    ErrorsActualLength: int

class Extra(BaseModel):
    OperationName: str
    backup_name: str = Field(alias='backup-name')

class DuplicatiBackupResult(BaseModel):
    Data: Data
    Extra: Extra
    Exception: str | None
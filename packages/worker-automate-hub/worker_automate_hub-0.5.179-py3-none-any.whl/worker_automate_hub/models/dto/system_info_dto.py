from pydantic import BaseModel


class SystemInfoDTO(BaseModel):
    uuidRobo: str
    maxCpu: str
    maxMem: str
    usoCpu: str
    usoMem: str
    espacoDisponivel: str

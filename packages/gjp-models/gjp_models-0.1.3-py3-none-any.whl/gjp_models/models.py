from datetime import datetime

from pydantic import BaseModel, constr


class SystemKwargs(BaseModel):
    class Config:
        extra = "allow"

class SystemConfig(BaseModel):
    ff: str
    box: str
    water: str
    system_kwargs: SystemKwargs

    class Config:
        extra = "allow"

class JobBase(BaseModel):
    pdb_id: constr(min_length=4, max_length=10)
    system_config: SystemConfig
    s3_links: str
    priority: int
    hotkeys: list[str]
    is_organic: bool
    active: bool
    update_interval: float
    max_time_no_improvement: float
    epsilon: int
    min_updates: int
    updated_at: datetime
    best_loss: float
    best_loss_at: datetime
    best_hotkey: str
    updated_count: int
    created_at: datetime
    best_cpt_links: list[str] | None = None


class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    job_id: str
    validator_hotkey: str

    class Config:
        from_attributes = True

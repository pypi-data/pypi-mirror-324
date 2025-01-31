from pydantic import BaseModel, Field
from typing import Optional, List
from .instance_state import InstanceState
import logging

logger = logging.getLogger(__name__)

class Requirements(BaseModel):
    gpu_name: Optional[str] = None
    price: Optional[float] = None  # Maximum acceptable price
    disk: Optional[float] = None  # Minimum disk space
    image: Optional[str] = None
    num_gpus: Optional[str] = None
    cpu_cores: Optional[str] = None
    ram: Optional[str] = None
    env: Optional[str] = None
    regions: Optional[List[str]] = None

    def matches(self, instance: InstanceState) -> bool:
        # Compare each field in the requirements with the instance
        if self.gpu_name and self.gpu_name.lower() != (instance.gpu_name or "").lower():
            logger.info(f"GPU name {self.gpu_name} does not match {instance.gpu_name}")
            return False
        if self.price and self.price < (instance.instance.totalHour or 0):
            logger.info(f"Price {self.price} is less than {instance.instance.totalHour}")
            return False
        if self.disk and self.disk > (instance.disk_space or 0):
            logger.info(f"Disk space {self.disk} is greater than {instance.disk_space}")
            return False
        if self.image and self.image.lower() != (instance.image_uuid or "").lower():
            logger.info(f"Image {self.image} does not match {instance.image_uuid}")
            return False
        if self.num_gpus and int(self.num_gpus) != (instance.num_gpus or 0):
            logger.info(f"Number of GPUs {self.num_gpus} is not {instance.num_gpus}")
            return False
        if self.cpu_cores and int(self.cpu_cores) > (instance.cpu_cores_effective or 0):
            logger.info(f"CPU cores {self.cpu_cores} is greater than {instance.cpu_cores_effective}")
            return False
        if self.ram and int(self.ram) > (instance.cpu_ram or 0):
            logger.info(f"RAM {self.ram} is greater than {instance.cpu_ram}")
            return False
        # if self.env and self.env not in [env[0] for env in (instance.extra_env or [])]:

        #     return False

        return True

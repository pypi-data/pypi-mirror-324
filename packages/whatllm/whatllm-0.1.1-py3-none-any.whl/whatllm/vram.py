import pyopencl as cl
from typing import Tuple
from whatllm import ERRORS

def get_machine_spec() -> Tuple[str, str, float]:
    """ Finds the most vram avaliable 
    Param:
        None
    Returns:
        list: a list containing host machine info
    """

    platforms = cl.get_platforms()
    gibi = 1073741824
    curr_vram = 0.0
    total_vram = 0.0
    plat_name = ''
    device_name = ''

    for platform in platforms:
        # opencl is for heterogenous computing 
        # Ex: Intel GPU will be on Intel platform, Nvidia on CUDA, AMD on Rocm
        devices = platform.get_devices(device_type=cl.device_type.GPU)
        for device in devices:
            # global_mem_size is in bytes
            try:
                curr_vram = round(device.global_mem_size / gibi, 2)
            except:
                raise ERRORS[2] # VRAM_ERROR
            
            if curr_vram > total_vram:
                total_vram = curr_vram
                plat_name = platform.name
                device_name = device.name

    if total_vram != 0.0:
        return [plat_name, device_name, total_vram]
    else:
        raise ERRORS[3] # HARDWARE_ERROR

"""Top-level package for what-llm-can-i-run."""

__app_name__ = "whatllm"
__version__ = "0.1.0"

(
    SUCCESS, # integer 0
    RAM_ERROR, # integer 1
    VRAM_ERROR, # so on
    HARDWARE_ERROR,
) = range(4) # error code

ERRORS = {
    RAM_ERROR: "Error Getting Physical Memory",
    VRAM_ERROR: "Error Getting GPU Memory",
    HARDWARE_ERROR: "Error Getting Hardware Specifcations.",
}

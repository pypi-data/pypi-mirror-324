from pencil_art import pencil_art

__all__ = ['pencil_art']

def __getattr__(name):
    if name == "__call__":
        return pencil_art
    raise AttributeError(f"Module '{__name__}' has no attribute '{name}'")

from .GeminiAPINode import NODE_CLASS_MAPPINGS as NODE_CLASS_MAPPINGS_G


# Combine the dictionaries
NODE_CLASS_MAPPINGS = {**NODE_CLASS_MAPPINGS_G}


__all__ = ['NODE_CLASS_MAPPINGS']
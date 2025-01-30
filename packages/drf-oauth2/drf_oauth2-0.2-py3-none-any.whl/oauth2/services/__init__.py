import importlib

# Faqat shu modullarni import qilish kerak
__all__ = ["google", "facebook", "github"]

# Modullarni avtomatik import qilish
for module_name in __all__:
    importlib.import_module(f"{__name__}.{module_name}")

import uvicorn
import fastapi
import PIL
import jinja2
import aiofiles

print(f"uvicorn={uvicorn.__version__}")
print(f"fastapi={fastapi.__version__}")
print(f"pillow={PIL.__version__}")
print(f"jinja2={jinja2.__version__}")
print(f"aiofiles={aiofiles.__version__}")
print("ALL_OK")
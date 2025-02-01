import os
import shutil

if not os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")):
    shutil.copyfile(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env.example"),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
    )
from decouple import config  # noqa F401

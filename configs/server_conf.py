import logging
from dash import Dash
# create a console and file logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(message)s")#"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# create a file handler
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
# create a stream handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
# call the ability to add external scripts
external_scripts = [
    # add the tailwind cdn url hosting the files with the utility classes
    {"src": "https://cdn.tailwindcss.com"}
]

app = Dash(
    __name__, external_scripts=external_scripts, suppress_callback_exceptions=True, assets_folder="../assets"
)

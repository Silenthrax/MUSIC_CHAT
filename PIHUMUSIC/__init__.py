from PIHUMUSIC.core.bot import PIHU
from PIHUMUSIC.core.dir import dirr
from PIHUMUSIC.core.git import git
from PIHUMUSIC.core.userbot import Userbot
from PIHUMUSIC.misc import dbb, heroku

from SafoneAPI import SafoneAPI
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = PIHU()
api = SafoneAPI()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

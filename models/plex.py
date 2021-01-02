from plexapi.myplex import MyPlexAccount
import plexapi
import json


class Plex:
    def __init__(self):
        f = open('config.json', 'r')
        self.config = json.load(f)
        try:
            self.account = MyPlexAccount(self.config.get(
                "PS_USERNAME"), self.config.get("PS_PASSWORD"))
        except plexapi.exceptions.Unauthorized:
            print('Email/Username/Password for Plex Account is incorrect!')
            exit()
        self.server = self.account.resource(
            self.config.get("SERVER_NAME")).connect()

    def sections(self):
        section = self.server.library.section('My Music')
        artist = section.get('Various Artists')
        tracks = artist.tracks()
        for track in tracks:
            url = track.getStreamURL()
            print(url)

    async def searchServer(self, query):
        results = self.server.search(query, mediatype='track')
        tracks = [track for track in results if isinstance(
            track, plexapi.audio.Track)]
        return tracks

    async def searchLibrary(self, section, title):
        res = self.server.library.search(title=title)
        return res


if __name__ == "__main__":
    plex = Plex()
    plex.sections()

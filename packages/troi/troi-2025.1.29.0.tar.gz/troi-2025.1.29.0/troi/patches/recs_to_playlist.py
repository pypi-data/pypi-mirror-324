from troi import Element, Recording, Playlist, PipelineError
import troi.listenbrainz.recs
import troi.playlist
import troi.filters
import troi.sorts
import troi.musicbrainz.recording_lookup
import troi.musicbrainz.mbid_mapping
from troi.patch import Patch


class RecsPlaylistMakerElement(Element):
    '''
        This element takes in Recordings and spits out a Playlist, which generating a custom name and desc
        for the playlist from the recording data
    '''

    def __init__(self, name, desc, patch_slug=None, user_name=None, max_num_recordings=None, type=None):
        super().__init__()
        self.name = name
        self.desc = desc
        self.patch_slug = patch_slug
        self.user_name = user_name
        self.max_num_recordings = max_num_recordings
        self.type = type

    @staticmethod
    def inputs():
        return [Recording]

    @staticmethod
    def outputs():
        return [Playlist]

    def read(self, inputs):
        try:
            model_id = inputs[0][0].listenbrainz["model_id"]
            model_url = inputs[0][0].listenbrainz["model_url"]
            self.name = "Top 100 %s recommendations from model %s" % (self.type, model_id)
            self.desc = """Top 100 %s recommendations generated by model <a href="%s">%s</a>""" % (self.type, model_url, model_id)
        except IndexError:
            pass

        if self.max_num_recordings is not None:
            return [Playlist(name=self.name,
                    description=self.desc,
                    recordings=inputs[0][:self.max_num_recordings],
                    patch_slug=self.patch_slug,
                    user_name=self.user_name)]
        else:
            return [Playlist(name=self.name,
                    description=self.desc,
                    recordings=inputs[0],
                    patch_slug=self.patch_slug,
                    user_name=self.user_name)]


class RecommendationsToPlaylistPatch(Patch):
    """
        See below for description
    """

    def __init__(self, args):
        super().__init__(args)

    @staticmethod
    def inputs():
        """
        Save the current recommended tracks for a given user and type (top or similar).

        \b
        USER_NAME: is a MusicBrainz user name that has an account on ListenBrainz.
        TYPE: is The type of daily jam. Must be 'top' or 'similar' or 'raw'.
        """
        return [
            {"type": "argument", "args": ["user_name"]},
            {"type": "argument", "args": ["type"]}
        ]

    @staticmethod
    def outputs():
        return [Recording]

    @staticmethod
    def slug():
        return "recs-to-playlist"

    @staticmethod
    def description():
        return "Save the current recommended tracks for a given user and type (top, similar or raw)."

    def create(self, inputs):
        user_name = inputs['user_name']
        type = inputs['type']

        if type not in ("top", "similar", "raw"):
            raise PipelineError("type must be either 'top' or 'similar' or 'raw'")

        recs = troi.listenbrainz.recs.UserRecordingRecommendationsElement(user_name=user_name,
                                                                          artist_type=type,
                                                                          count=100)
        if type == "top":
            playlist_type = "top artists"
        elif type == "similar":
            playlist_type = "similar artists"
        else:
            playlist_type = "raw"
        pl_maker = RecsPlaylistMakerElement(name="[unknown]",
                                            desc="[unknown]",
                                            patch_slug="saved-recs",
                                            user_name=user_name,
                                            type=playlist_type)
        pl_maker.set_sources(recs)

        return pl_maker

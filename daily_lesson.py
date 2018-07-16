import requests

import settings

DAILY_LESSON_ENDPOINT = settings.ARCHIVE_BACKEND_URL + "/latestLesson"
CONTENT_UNIT_ENDPOINT = settings.ARCHIVE_BACKEND_URL + "/content_units"


class DailyLesson:
    def __init__(self, logger, date, lang):
        self.date = date
        self.lang = lang
        self.logger = logger

        logger.info("Fetching lesson from {}".format(self.date))

        res = requests.get(DAILY_LESSON_ENDPOINT, params=dict(language=self.lang)).json()
        self._daily_lesson_parts = [lesson for lesson in res['content_units'] if lesson['film_date'] == self.date]
        logger.debug("Today's daily lessons fetched: {}".format(self._daily_lesson_parts))

    def get_parts_with_files(self):
        langs = ['ru', 'he']
        for part in self._daily_lesson_parts:
            res = requests.get("/".join([CONTENT_UNIT_ENDPOINT, part['id']]), params=dict(language=self.lang)).json()
            # filter by file type and video quality
            filtered_files = [file for file in res['files'] if file['type'] == 'audio' or file['video_size'] == 'nHD']
            #  Fetching only hebrew and russian media files
            for lang in langs:
                # building valid urls to media files
                files = ["/".join([settings.CDN_URL, file['id'] + '.' + file['name'].split('.')[-1]])
                         for file in filtered_files if file['language'] == lang]
                # fetching media files per language
                files_audio = [file for file in files if file.split('.')[-1] == 'mp3']
                files_video = [file for file in files if file.split('.')[-1] == 'mp4']
                # final
                part['files_{}'.format(lang)] = {'audio': "".join(files_audio), 'video': "".join(files_video)}
        return self._daily_lesson_parts

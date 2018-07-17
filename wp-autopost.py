#!/usr/bin/env python3.6
"""
    WordPress auto-post script, using JWT auth and wp-rest api
"""
import datetime
import random
import sys

from jinja2 import Template

import settings
import daily_lesson
import wp_rest_api
from logger import Logger

logger = None

HTML = """
                <p><span style="text-decoration: underline;"><strong>{{ title }}</strong></span></p>
                <table border="0">
                <tbody>
                <tr>
                <td>
                <span class="podPress_content"> \
                    <img src="https://www.laitman.ru/wp-content/plugins/podpress/images/video_mp4_icon.png" \
                        border="0" align="top" class="podPress_imgicon" \
                        alt="icon for podpress">&nbsp;<strong>Видео (рус.)</strong>: \
                    <a rel="nofollow" href="{{ lesson_rus_video }}">\
                    <span id="podPressPlayerSpace_{{ index + 1 }}_PlayLink">Открыть</span></a>    |\
                    <a href="{{ lesson_rus_video }}" rel="nofollow">Скачать</a><br>\
                    <span class="podPressPlayerSpace" id="podPressPlayerSpace_{{ index + 1 }}"\
                        style="display: block;z-index: 1;">&nbsp;</span>\
                </span>
                </td>
                <td>&nbsp;</td>
                <td>
                <span class="podPress_content">\
                    <img src="https://www.laitman.ru/wp-content/plugins/podpress/images/audio_mp3_icon.png" \
                        border="0" align="top" class="podPress_imgicon" \
                        alt="icon for podpress">&nbsp;<strong>Аудио (рус.)</strong>: \
                        <a rel="nofollow" href="{{ lesson_rus_audio }}">\
                        <span id="podPressPlayerSpace_{{ index + 2 }}_PlayLink">Открыть</span></a>    |\
                        <a href="{{ lesson_rus_audio }}" rel="nofollow">Скачать</a><br>\
                <span class="podPressPlayerSpace" id="podPressPlayerSpace_{{ index + 2 }}" \
                    style="display: block;z-index: 1;">&nbsp;</span>\
                </span>
                </td>
                </tr>
                <tr>
                <td>
                <span class="podPress_content">\
                    <img src="https://www.laitman.ru/wp-content/plugins/podpress/images/video_mp4_icon.png" \
                        border="0" align="top" class="podPress_imgicon" \
                        alt="icon for podpress">&nbsp;<strong>Видео (ивр.)</strong>: \
                        <a rel="nofollow" href="{{ lesson_heb_video }}">\
                        <span id="podPressPlayerSpace_{{ index + 3 }}_PlayLink">Открыть</span></a>    |\
                        <a href="{{ lesson_heb_video }}" rel="nofollow">Скачать</a><br>\
                <span class="podPressPlayerSpace" id="podPressPlayerSpace_{{ index + 3 }}" \
                    style="display: block;z-index: 1;">&nbsp;</span>\
                </span>
                </td>
                <td>&nbsp;</td>
                <td>
                <span class="podPress_content">\
                    <img src="https://www.laitman.ru/wp-content/plugins/podpress/images/audio_mp3_icon.png" \
                        border="0" align="top" class="podPress_imgicon" \
                        alt="icon for podpress">&nbsp;<strong>Аудио (ивр.)</strong>: \
                        <a rel="nofollow" href="{{ lesson_heb_audio }}">\
                        <span id="podPressPlayerSpace_{{ index + 4 }}_PlayLink">Открыть</span></a>    |\
                        <a href="{{ lesson_heb_audio }}" rel="nofollow">Скачать</a><br>\
                <span class="podPressPlayerSpace" id="podPressPlayerSpace_{{ index + 4 }}" \
                    style="display: block;z-index: 1;">&nbsp;</span>\
                </span>
                </td>
                </tr>
                </tbody>
                </table>
"""


def lessons_data_to_html(parts):
    lesson_html = ""
    for index, part in enumerate(parts):
        base = random.randint(10000, 100000)
        template = Template(HTML, trim_blocks=True, lstrip_blocks=True)
        outp = template.render(index=base + index,
                               title=part['name'],
                               lesson_rus_video=part['files_ru']['video'],
                               lesson_rus_audio=part['files_ru']['audio'],
                               lesson_heb_video=part['files_he']['video'],
                               lesson_heb_audio=part['files_he']['audio'])
        lesson_html += outp
    with open('outp.html', 'w') as f:
        f.write(lesson_html)
    return lesson_html


def main():
    global logger
    logger = Logger().logger

    logger.info("Fetching Lesson parts...")
    today = datetime.date.today().strftime('%Y-%m-%d')
    lesson_from_today = daily_lesson.DailyLesson(logger, today, lang='ru')
    parts = lesson_from_today.get_parts_with_files()
    logger.info("Lesson parts with files: {}".format(parts))
    logger.info("Processing Lesson parts to HTML...")
    post_content = lessons_data_to_html(parts)

    logger.info("WP Autopost Loaded")
    wp_rest = wp_rest_api.WpRESTApi(logger,
                                    settings.LAITMAN_RU_URL,
                                    settings.LAITMAN_RU_USERNAME,
                                    settings.LAITMAN_RU_PASSWORD)
    wp_rest.validate_token()
    today = datetime.datetime.now().strftime('%d.%m.%y')
    wp_rest.create_post(title=f"Утренний урок {today}", content=post_content, status="publish")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(e)
        sys.exit(1)

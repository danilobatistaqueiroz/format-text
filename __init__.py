import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5 import QtWidgets
from PyQt5 import QtCore

import os
import urllib
import logging

from anki.hooks import addHook, wrap
from aqt.editor import Editor
from typing import List, Callable
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

from anki.utils import json

config = mw.addonManager.getConfig(__name__)

ADDON_PATH = os.path.dirname(__file__)

ICON_SOFTEN_PATH = os.path.join(ADDON_PATH, "icons", "soften.ico")
SOFTEN_TOOLTIP = "soften text"

ICON_CONTRAST_PATH = os.path.join(ADDON_PATH, "icons", "contrast.png")
CONTRAST_TOOLTIP = "contrast text"

ICON_EMPHASIZE_PATH = os.path.join(ADDON_PATH, "icons", "emphasize.png")
EMPHASIZE_TOOLTIP = "emphasize text"

def contrast_text(txt):
    contrast_format = config[ 'contrast-format' ]
    return contrast_format.replace('$txt',txt)

def soften_text(txt):
    soften_format = config[ 'soften-format' ]
    return soften_format.replace('$txt',txt)

def emphasize_text(txt):
    emphasize_format = config[ 'emphasize-format' ]
    return emphasize_format.replace('$txt',txt)

def soften(editor: Editor) -> None:
    text = editor.web.selectedText()
    text = soften_text(text)
    text = f"""setFormat('inserthtml', {json.dumps(text)});"""
    editor.web.eval(text)

def emphasize(editor: Editor) -> None:
    text = editor.web.selectedText()
    text = emphasize_text(text)
    text = f"""setFormat('inserthtml', {json.dumps(text)});"""
    editor.web.eval(text)

def contrast(editor: Editor) -> None:
    text = editor.web.selectedText()
    text = contrast_text(text)
    text = f"""setFormat('inserthtml', {json.dumps(text)});"""
    editor.web.eval(text)

def add_buttons(buttons: List[str], editor: Editor) -> List[str]:
    if config['soften'] == 'enabled':
        soften_button = editor.addButton(
            icon=ICON_SOFTEN_PATH,
            cmd="soften_text",
            func=lambda editor: soften(editor),
            tip=SOFTEN_TOOLTIP+' '+config['soften-shortcut'],
            keys=config['soften-shortcut']
        )
        buttons.append(soften_button)
    if config['contrast'] == 'enabled':
        contrast_button = editor.addButton(
            icon=ICON_CONTRAST_PATH,
            cmd="contrast_text",
            func=lambda editor: contrast(editor),
            tip=CONTRAST_TOOLTIP+' '+config['contrast-shortcut'],
            keys=config['contrast-shortcut']
        )
        buttons.append(contrast_button)
    if config['emphasize'] == 'enabled':
        emphasize_button = editor.addButton(
            icon=ICON_EMPHASIZE_PATH,
            cmd="emphasize_text",
            func=lambda editor: emphasize(editor),
            tip=EMPHASIZE_TOOLTIP+' '+config['emphasize-shortcut'],
            keys=config['emphasize-shortcut']
        )
        buttons.append(emphasize_button)
    return buttons

addHook("setupEditorButtons", add_buttons)

<h1 align="center">jdProcessFileWatcher</h1>

<h3 align="center">Effortlessly monitor and display real-time file access for any process</h3>

<p align="center">
    <img alt="jdProcessFileWatcher" src="screenshots/MainWindow.png"/>
</p>

With jdProcessFileWatcher, you can monitor all the files accessed by a process. It allows you to start any program and observe in real-time which files it accesses through an easy-to-use GUI. Additionally, you have the option to connect to an already running process.

## Translate
You can help translating jdProcessFileWatcher on [Codeberg Translate](https://translate.codeberg.org/projects/jdProcessFileWatcher)

![Translation status](https://translate.codeberg.org/widget/jdProcessFileWatcher/jdProcessFileWatcher/multi-auto.svg)

## Develop
jdProcessFileWatcher is written in Python and uses PyQt6 as GUI toolkit. You should have some experience in both.
You can run `jdProcessFileWatcher.py`to start jdProcessFileWatcher from source and test your local changes.
It ships with a few scripts in the tools directory that you need to develop.

#### CompileUI.py
This is the most important script. It will take all `.ui` files in `jdProcessFileWatcher/ui` and compiles it to a Python class
and stores it in `jdProcessFileWatcher/ui_compiled`. Without running this script first, you can't start jdProcessFileWatcher.
You need to rerun it every time you changed or added a `.ui` file.

#### BuildTranslations.py
This script takes all `.ts` files and compiles it to `.qm` files.
The `.ts` files are containing the translation source and are being used during the translation process.
The `.qm` contains the compiled translation and are being used by the Program.
You need to compile a `.ts` file to a `.qm` file to see the translations in the Program.

#### UpdateTranslations.py
This regenerates the `.ts` files. You need to run it, when you changed something in the source code.
The `.ts` files are contains the line in the source, where the string to translate appears,
so make sure you run it even when you don't changed a translatable string, so the location is correct.

####  UpdateUnixDataTranslations.py
This regenerates the translation files in `deploy/translations`. these files contains the translations for the Desktop Entry and the AppStream File.
It uses gettext, as it is hard to translate this using Qt.
These files just exists to integrate the translation with Weblate, because Weblate can't translate the Desktop Entry and the AppStream file.
Make sure you run this when you edited one of these files.
You need to have gettext installed to use it.

#### UpdateTranslators.py
This uses git to get a list of all Translators and writes it to `jdProcessFileWatcher/data/translators.json`.
This is used to display the translators in the About Dialog.
You need git to run this script.

#### WriteChangelogHtml.py
This read the Changelog from `deploy/page.codeberg.JakobDev.jdProcessFileWatcher.metainfo.xml`, converts it to HTML and writes it to `jdProcessFileWatcher/data/changelog.html`.
This is used to display the Changelog in the About Dialog.
You need [appstream-python](https://pypi.org/project/appstream-python) to be installed to use this script.

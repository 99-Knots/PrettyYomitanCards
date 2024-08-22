import sys, re
import zipfile, os
import sqlite3, json

TEMP_DIR = 'temp_dir'
NOTE_NAME = 'PrettyYomitan'
CARD_TYPE = 'Recognition'


def setStyle(note, file_path):
    with open(file_path, encoding='utf-8') as file:
        css_file = file.read()
    note['css'] = css_file

def setTemplate(note, card_name, file_path, key):
    with open(file_path, encoding='utf-8') as file:
        file_content = file.read()
    template = next((item for item in note['tmpls'] if item['name'] == card_name), None)
    if template:
        template[key] = file_content

def setFrontTemplate(note, template_name, file):
    setTemplate(note, template_name, file, 'qfmt')

def setBackTemplate(note, template_name, file):
    setTemplate(note, template_name, file, 'afmt')


def createAnkiPkg(source_dir, old_pkg):
    with zipfile.ZipFile('tempDeck.apkg', 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for folder_name, subfolders, filenames in os.walk(source_dir):
            for filename in filenames:
                file_path = os.path.join(folder_name, filename)
                zip_ref.write(file_path, filename)
    os.replace('tempDeck.apkg', old_pkg)


def extractOldDeck(filename):
    with zipfile.ZipFile(filename, 'r') as old_deck:
        old_deck.extractall(TEMP_DIR)


def editDB(source, front_file=None, back_file=None, style_file=None):
    if not(front_file is None and back_file is None and style_file is None):
        try:
            conn = sqlite3.connect(source)
            cursor = conn.cursor()

            cursor.execute('SELECT id, models FROM col')
            mod_id, models = cursor.fetchall()[0]
            models = json.loads(models)
            notetype = next((models[k] for k in models.keys() if models[k]['name'] == NOTE_NAME), None)

            if front_file is not None:
                setFrontTemplate(notetype, CARD_TYPE, front_file)
            if back_file is not None:
                setBackTemplate(notetype, CARD_TYPE, back_file)
            if style_file is not None:
                setStyle(notetype, style_file)

            new_models = json.dumps(models)
            cursor.execute((f'UPDATE col SET models = ? WHERE id = ?'), (new_models, mod_id))

            conn.commit()

        except sqlite3.Error as e:
            print(f'Database error: {e}')
            conn.rollback()
            sys.exit(1)

        finally:
            conn.close()


def updateDemoDeck():
    source = os.path.join(TEMP_DIR, 'collection.anki21')
    deck_name = 'PrettyYomitanCardsDemo.apkg'
    front = 'frontTemplate.html'
    back = 'backTemplate.html'
    styling = 'style.css'
        
    extractOldDeck(deck_name)
    editDB(source, front, back, styling)
    createAnkiPkg(TEMP_DIR, deck_name)
    print('updated the .apkg with new template files')


def replacePermalink(start_marker, end_marker, content, prefix):
    def replace(match):
        f = match.group(2)
        with open(f) as file:
            line_count = len(file.readlines())
        start_m = start_marker.format(file=' ' + f)
        return f'{start_m}\n{prefix}{f}#L1-L{line_count}\n{end_marker}'
    
    start_m = start_marker.format(file=r'\s*(.*?)\s*')
    pattern = f'({start_m})(.*?)({end_marker})'

    return(re.sub(pattern, replace, content, flags=re.DOTALL))


def processReadme(readme, repo, hash_long):
    with open(readme, 'r') as file:
        content = file.read()
    start_marker = '<!--insert-start:{file}-->'
    end_marker = '<!--insert-end-->'
    with open(readme, 'w') as file:
        file.write(replacePermalink(start_marker, end_marker, content, prefix='https://github.com/' + repo + '/blob/' + hash_long + '/'))
    print('inserted new permalinks')

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python update_files.py <user/repository> <hash long> <readme path>')
        sys.exit(1)

    user_repo = sys.argv[1].strip()
    hash_long = sys.argv[2].strip()
    readme_path = sys.argv[3].strip()

    if not user_repo or not hash_long or not readme_path:
        print('Error: One or more required arguments are empty.')
        sys.exit(1)

    processReadme(readme_path, user_repo, hash_long)
    updateDemoDeck()

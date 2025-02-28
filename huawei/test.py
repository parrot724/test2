import json

className = 'j84-MyClass'
with open('tmp/classes/j84-MyClass.json', 'r', encoding='utf-8') as f:
    s = f.read()

classPages = json.loads(s)
with open('tmp/classes/%s.txt' % className, 'w', encoding="utf-8") as f:
    for pagex, page in enumerate(classPages['pages']):
        if len(page['pageNotes']) is not 0:
            f.write(str(pagex + 1))
        for notex, note in enumerate(page['pageNotes']):
            f.write('-%s:%s:(%s, %s, %s, %s)' % (notex + 1, note['noteContent'], note['x'], note['y'], note['width'], note['height']))
        f.write('\n')

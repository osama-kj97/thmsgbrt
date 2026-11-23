"""Inline wireframes/screens.json into the hub template -> hub/index.html"""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((root/'wireframes/screens.json').read_text())
tpl = (root/'hub/hub.template.html').read_text()
out = tpl.replace('__SCREENS__', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
(root/'hub/index.html').write_text(out)
print('wrote', len(out), 'bytes')

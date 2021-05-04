import os
import re

import latextools
import svgutils

print("** Step 1/2 - hugo build **")
os.system("hugo")

print("\n** Step 2/2 - tex2svg **")
for root, _, files in os.walk("./docs", topdown=False):
   for filename in files:
       if filename.endswith(".html"):
            path = os.path.join(root, filename)
            with open(path, 'r') as f:
                content = f.read()
                for match in re.findall("\$.*\$", content):
                    latex = latextools.render_snippet(
                        match, commands=[latextools.cmd.all_math])
                    svg = svgutils.transform.fromstring(latex.as_svg().content)
                    w, h = svg.get_size()
                    scale = 1.1
                    svg.set_size((f'{float(w[:-2])*scale}pt', f'{float(h[:-2])*scale}pt'))
                    content = content.replace(match, svg.to_str().decode('ascii'))
                with open(path, 'w') as f:
                    f.write(content)

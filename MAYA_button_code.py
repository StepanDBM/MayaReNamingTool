import sys
from pathlib import Path

repo = Path(
    r"E:\Work\3D\my_3D\KANEDA\Projects\Scripting\MayaReNamingTool\renamer"
)

if str(repo) not in sys.path:
    sys.path.insert(0, str(repo))

import bootstrap

bootstrap.run()
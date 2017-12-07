from django.apps import AppConfig

import os
folderName = os.path.dirname(os.path.abspath(__file__)).split('/')[-1]
className = folderName[0].upper()+folderName[1:]

classdef = "class %sConfig(AppConfig):\n    name = '%s'"%(className,folderName)

exec(classdef)

#print(classdef)


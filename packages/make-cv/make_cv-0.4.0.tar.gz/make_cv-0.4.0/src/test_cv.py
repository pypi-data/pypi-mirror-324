#!/Users/bhelenbr/.venv/bin/python3.12
# -*- coding: utf-8 -*-
import re
import sys
from make_cv.make_cv import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
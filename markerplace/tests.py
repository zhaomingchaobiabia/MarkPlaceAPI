from django.test import TestCase

# Create your tests here.

import time
print(time.strftime('%Y-%m-%d %H:%M:%S'))


import os

print(os.environ['FNAC_KEY'])
print(os.environ['PARTNER_ID'])
# -*- coding: utf-8 -*-

import re
import string


# Expresión regular que comprueba que la cadena es un número.
regex = re.compile(r'[0-9]+')
text1 = '01234'

if regex.search(text1):
   print('Entra porque text1 coincide con la expresión regular.')

if regex.match(text1):
     print('Entra porque text1 coincide con la expresión regular.')

text2 = 'test 01234'
if regex.search(text2):
   print('Entra porque parte de text2 coincide con la expresión regular.')

if regex.match(text2):
   pass  # No entrará
else:
  print('No entra porque text2 no coincide con la expresión regular.')
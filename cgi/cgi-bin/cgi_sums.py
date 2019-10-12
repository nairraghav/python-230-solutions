#!/usr/bin/env python
import cgi
import cgitb

cgitb.enable()


form = cgi.FieldStorage()
operands = form.getlist("operand")
total = 0

try:
    total = sum(map(int, operands))
    body = f'Total: {total}'
except ValueError:
    body = 'Invalid Parameter Found: Please Only Use Integers'

print("Content-type: text/plain")
print()
print(body)

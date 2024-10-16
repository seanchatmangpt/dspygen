```python

class MathWeb:

...

from sympy import isprime

@app.route('/prime/<int:n>')

def nth_prime(n):

count = 0

num = 1

while count < n:

num += 1

if isprime(num):

count += 1

return str(num)

```
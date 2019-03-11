# reflectedParamterRecon
A tool for :
1. Grab a (not necessarily complete) list of URL for a domain. (This part is based on the work of [si9int](https://github.com/si9int/cc.py))
2. Test for parameters with value reflected in response

# Usage
python3 detect.py `domain` | grep reflected

# Todo
1. Mulitithreading
2. Probe for more XSS payload

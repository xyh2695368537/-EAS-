price = '你好'
g = {}
g['__builtins__'] = None
price = eval(price,g)
if isinstance(price,(int,float)):
    print(type(price))
    print(price)
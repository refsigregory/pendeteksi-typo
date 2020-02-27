import cgi

stringvar = 'Hello variable'
intvar = 30
html_content = f'''<html>
<head><title>My first Python CGI app</title></head>
<body>
<p>Hello, 'world'!</p>
<p>This is a stringvar = {stringvar} </p>
<p>This is intvar = {intvar} </p>
</body>
</html>'''

print ('Content-type: text/html\n\n')
print (html_content)
import run as r

print('Welcome to my KJV interpreter!')
ans = 'n'
print('Please paste the path of the file.')
path = input('>> ')
text = ''
while ans != 'y':
    try:
        with open(path, 'r') as f:
            text = f.read()
            print('Your file:\n')
            print(text, '\n\n----------------------------\n')
            print('Is this correct? (y/n)')
            ans = input('>> ')
            if ans == 'n':
                print('Please paste the path of the file.')
                path = input('>> ')
                ans = 'n'
    except:
        print('No file. Please try again.')
        path = input('>> ')
        ans = 'n'

text = text.split('\n')

r.run(text)
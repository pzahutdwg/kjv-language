def error(line=None, wholeLine=None, type=None, term=None):
    if type == 'declaration':
        pass
    elif type == 'unexpected':
        print(f'And it came to pass that the term, even {term}, was found in the midst of the code—known to the learned, yet out of season and without cause.')
    elif type == 'badComma':
        print(f'At line {line}, a comma did appear, yet it belonged not; for another parameter was looked for, and the comma was found wanting.')
    elif type == 'badClose':
        print(f'And behold, a function closure was found on line {line}, upon the selfsame line as other code. This thing was not expected, neither was it fitting; for such union is unseemly in the eyes of the compiler, and the law of clarity was broken')
    elif line:
        print(f'Lo, at line {line}, there arose an error, sudden and without warning.')
    
    if wholeLine:
        print(' '.join(wholeLine))
    else:
        print('We have searched the lines and beheld them with care, but the source remaineth in darkness.')
    if term:
        print(term)
    print('And thus, the interpreter hath spoken. Let not this error be taken lightly, for it is a sign of deeper troubles within the code.')
    print('If thou seeketh understanding of the syntax, turn thee unto the "Syntax" section in the book of README.md; there shalt thou find wisdom, and the way shall be made plain before thee.')
    # exit(1)
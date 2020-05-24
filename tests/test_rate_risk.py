from * import rate_risk

def test_rate_link():
    print('Testing rate_link')
    print('Score\tExpected\tLink')
    tests = [
        (0.0, 'https://www.google.com/'),
        (0.5, 'http://edimfulbu.tk/'),
        (0.5, 'https://dziennikmiasto.098.pl'),
        (1.0, 'https://transpor.cl/driveone/OneDrive')
    ]
    for expected, link in tests:
        rating = rate_link(link)
        print(f'{rating}\t{expected}\t{link}')

test_rate_link()
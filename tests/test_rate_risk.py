from rate_risk import rate_link, rate_email

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

def test_rate_email():
    print('Testing rate_email')

test_rate_link()
test_rate_email()
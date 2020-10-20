import os.path, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from app.api.utils.rate_risk import rate_link, rate_email, custom_rate_link

def test_rate_link():
    print('Testing rate_link')
    print('Score\tExpected\tLink')
    tests = [
        (0.0, 'https://www.google.com/'),
        (0.5, 'http://hamt.jp/program/wp-content/themes/twentyfourteen/home/latampass/cadastro/?cli=Cliente&amp;/7veVm4c71c/kgkrHOKUo5.php')
        (0.5, 'http://edimfulbu.tk/'),
        (0.5, 'https://dziennikmiasto.098.pl'),
        (1.0, 'https://transpor.cl/driveone/OneDrive')
    ]
    for expected, link in tests:
        (rating, reasons) = rate_link(link)
        print(f'{expected}\t{rating}\t{", ".join(reasons)}\t{link}')

def test_rate_email():
    print('Testing rate_email')
    print('NOT IMPLEMENTED')

def test_custom_rate_link():
    print('Testing custom_rate_link')
    print('Score\tExpected\tReasons\tLink')
    tests = [
        (0.0, 'https://www.google.com/'),
        (0.0, 'https://stackoverflow.com/questions/51451464/get-request-response-text-prints-invalid-characters'),
        (0.0, 'https://lchs-cybersecurity.github.io/'),
        (0.5, 'http://hamt.jp/program/wp-content/themes/twentyfourteen/home/latampass/cadastro/?cli=Cliente&amp;/7veVm4c71c/kgkrHOKUo5.php'),
        (0.5, 'http://edimfulbu.tk/'),
        (0.5, 'https://dziennikmiasto.098.pl'),
    ]
    for expected, link in tests:
        (rating, reasons) = custom_rate_link(link)
        print(f'{expected}\t{rating}\t{", ".join(reasons)}\t{link}')


# test_rate_link()
# test_rate_email()
test_custom_rate_link()
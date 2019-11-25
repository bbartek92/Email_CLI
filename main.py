import argparse
import sys
import logic

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f'error: {message}\n')
        self.print_help()
        sys.exit(2)

my_parser = MyParser(prog='Email CLI',
                     description='This app enables you to see received'
                                 ' emails list, write new email, '
                                 'respond to email or set up automatic'
                                 'response. The app connects to Gmail.')

my_parser.add_argument('-read', action='store_true',
                       help='This option will list the email which you '
                            'received')

my_parser.add_argument('-write', action='store_true',
                       help='This option will enable you to write new email')

my_parser.add_argument('-auto', action='store_true',
                       help='This option will set automatic reply for all '
                            'your incoming emails.')

args = my_parser.parse_args()
if args.read:
    mail = logic.MailBox()
    mail.read()
if args.write:
    mail = logic.MailBox()
    mail.write()
if args.auto:
    mail = logic.MailBox()
    mail.auto()
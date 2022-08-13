
from sites import NeoBux
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('--starting', default=0)
args = parser.parse_args()


if __name__ == '__main__':
	with open('data/gmail acc.bak', 'r') as f:
		content = f.read()
	email_list = content.split()
	email_list = [email.split(":") for email in email_list][args.starting:]
	for i, email in enumerate(email_list):
		neobux = NeoBux()
		username = email[0].split('@')[0]
		password = email[1]
		backup_email = email[2]
		neobux.start_process(username, password)
		neobux.quit()

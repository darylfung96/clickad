
from sites import NeoBux
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('--starting', default=0, type=int)
args = parser.parse_args()


if __name__ == '__main__':
	with open('data/neobux.txt', 'r') as f:
		content = f.read()

	with open('ports.txt', 'r') as ports_f:
		ports = ports_f.read()
		ports = ports.split("\n")

	email_list = content.split()
	email_list = [email.split(":") for email in email_list][args.starting:]
	for i, email in enumerate(email_list):
		# neobux = NeoBux(proxy_link=ports[i])
		neobux = NeoBux()
		username = email[0].split('@')[0]
		password = email[1]
		backup_email = email[2]
		neobux.start_process(username, password)
		neobux.quit()

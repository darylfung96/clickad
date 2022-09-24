
from sites import NeoBux
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('--starting', default=0, type=int)
parser.add_argument('--port-start', default=0, type=int)
args = parser.parse_args()


if __name__ == '__main__':
	with open('data/25.txt', 'r') as f:
		content = f.read()

	with open('ports.txt', 'r') as ports_f:
		ports = ports_f.read()
		ports = ports.split("\n")[args.port_start:]

	email_list = content.split()
	email_list = [email.split(":") for email in email_list][args.starting:]
	for i, email in enumerate(email_list):
		username = email[0].split('@')[0]
		password = email[1]
		# backup_email = email[2]

		# neobux = NeoBux(username, proxy_link=ports[i])
		neobux = NeoBux(username)

		try:
			neobux.start_process(username, password)
			neobux.quit()
		except IndexError as e:
			print(username, ' ', 'port: ', ports[i])
			print(e)
			print('===============')
			neobux.quit()


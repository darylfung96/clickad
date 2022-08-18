from argparse import ArgumentParser

from sites import NeoBux

parser = ArgumentParser()
parser.add_argument('--starting', default=0, type=int)
parser.add_argument('--port-start', default=4, type=int)
args = parser.parse_args()


def remove_registered_account(content):
	content = content.split()[1:]
	content = '\n'.join(content)
	with open('data/neobux_register.txt', 'w') as f:
		f.write(content)
	return content

if __name__ == '__main__':
	with open('data/neobux_register.txt', 'r') as f:
		content = f.read()
	email_list = content.split()
	email_list = [email.split(":") for email in email_list]
	with open('ports.txt', 'r') as ports_f:
		ports = ports_f.read()
		ports = ports.split("\n")[args.port_start:]

	for i, email in enumerate(email_list):
		username = email[0].split('@')[0]
		password = email[1]
		backup_email = email[2]
		neobux = NeoBux(username, proxy_link=ports[i])
		neobux.register(username, password, email[0], backup_email)
		neobux.quit()

		content = remove_registered_account(content)


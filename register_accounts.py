
from sites import NeoBux

if __name__ == '__main__':
	with open('data/gmail acc.txt', 'r') as f:
		content = f.read()
	email_list = content.split()
	email_list = [email.split(":") for email in email_list]
	for email in email_list:
		neobux = NeoBux()
		username = email[0].split('@')[0]
		password = email[1]
		backup_email = email[2]
		neobux.register(username, password, email[0], backup_email)
		neobux.quit()

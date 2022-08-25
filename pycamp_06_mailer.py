import click
import yaml
import imaplib
from email import message_from_bytes
from email.header import decode_header

class MailBox:
    def __init__(self, host: str, port_imap: int, login: str, password: str, workdir: str):
        self.login = login
        self.password = password
        self.workdir = workdir
        self.server = imaplib.IMAP4_SSL(host, port_imap)

    def __enter__(self):
        """ Funkcja odpowiedzialna za logowanie do skrzynki pocztowej """
        self.server.login(self.login, self.password)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.server.close()
        self.server.logout()

    def get_count(self):
        """ Funkcja zliczajaca ilosc wiadomosci w danym folderze """
        self.server.select(self.workdir)
        _, messages = self.server.search(None, 'ALL')
        return sum(1 for num in messages[0].split())

    def show_new_mails(self):
        messages_dir = {}
        self.server.select(self.workdir)
        _, message_ids = self.server.search(None, 'ALL')
        for message_id in message_ids[0].split():
            _, msg = self.server.fetch(message_id, '(RFC822)')
            message = message_from_bytes(msg[0][1])

            subject, _ = decode_header(message['Subject'])[0]
            if not isinstance(subject, str):
                subject = subject.decode('utf-8')

            sender = message['From']

            content = message.get_payload(decode=True)
            
            for part in message.walk():
                if part.get_filename() is not None:
                    messages_dir[message_id.decode("utf-8")] = [sender, subject, content, part.get_filename()]
                else:
                    messages_dir[message_id.decode("utf-8")] = [sender, subject, content, 'brak załącznika']

        print(messages_dir)

def load_config():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config


@click.group
@click.option('-w', '--workdir', default='Inbox', help='wybierz katalog (domyślnie: Inbox)')
def main(workdir):
    config = load_config()
    with MailBox(config['host'], config['port_imap'], config['login'], config['password'], workdir) as mail_box:
        print(mail_box.get_count())
        mail_box.show_new_mails()


@main.command(help='lista wiadomości')
def mails():
    pass


@main.command(help='wyszykiwanie')
@click.option('-m', '--search_module', type=click.Choice(['sender', 'header',  'content'], case_sensitive=False), required=True, help='search place')
@click.option('-p', '--search_pattern', required=True, help='search-pattern')
def search(search_module, search_pattern):
    pass


main.add_command(mails)
main.add_command(search)


if __name__ == '__main__':
    main()

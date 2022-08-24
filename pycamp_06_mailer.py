import click
import yaml
import imaplib

class MailBox:
    def __init__(self, host: str, port_imap: int, username: str, password: str, workdir: str):
        self.username = username
        self.password = password
        self.workdir, = workdir
        self.server = imaplib.IMAP4_SSL(host, port_imap)

    def login(self):
        """ Funkcja odpowiedzialna za logowanie do skrzynki pocztowej """
        self.server.ehlo()
        self.server.login(self.username, self.password)

    def get_count(self):
        """ Funkcja zliczajaca ilosc wiadomosci w danym folderze """
        self.server.select(self.workdir)
        _, data = self.server.search(None, 'ALL')
        return sum(1 for num in data[0].split())

    def mails_list(self):
        pass


    def __exit__(self):
        self.server.close()
        self.server.logout()


def load_config():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
        print(config)

@click.group
@click.option('-w', '--workdir', default='Inbox')
def main(workdir):
    load_config()
    print(workdir)


@main.command()
@click.argument('-l', is_flag=True)
def mails():
    print('lista emajlów')


@main.command()
@click.option('-m', '--search_module', type=click.Choice(['sender', 'header',  'content'], case_sensitive=False), required=True)
@click.option('-p', '--search_pattern', required=True)
def search():
    pass


main.add_command(mails)
main.add_command(search)


if __name__ == '__main__':
    main()

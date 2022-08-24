import click
import yaml
import imaplib


class MailBox:
    def __init__(self, host: str, port_imap: int, login: str, password: str, workdir: str):
        self.login = login
        self.password = password
        self.workdir = workdir
        self.server = imaplib.IMAP4_SSL(host, port_imap)

    def loginsex(self):
        """ Funkcja odpowiedzialna za logowanie do skrzynki pocztowej """
        # self.server.ehlo()
        self.server.login(self.login, self.password)

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
    return config


@click.group
@click.option('-w', '--workdir', default='Inbox', help='wybierz katalog (domyślnie: Inbox)')
def main(workdir):
    config = load_config()
    mail_box = MailBox(host=config['host'], port_imap=config['port_imap'], login=config['login'], password=config['password'], workdir=workdir)
    mail_box.loginsex()
    print(mail_box.get_count())


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

import click
import yaml
import imaplib


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
        _, data = self.server.search(None, 'ALL')
        return sum(1 for num in data[0].split())

    def show_mails(self):
        self.server.select(self.workdir)
        status, data = self.server.search(None, 'ALL')
        return status, data


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
        print(mail_box.show_mails())


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

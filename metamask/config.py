argentidentifikator = 'idpnpmjcpildphhndcbjcolbnkfekjoo'  # введите идентификатор расширения

password = 'PRO100ART' # введите пароль для всех кошельков argent

with open('mnemonic.txt','r') as f:
    seeds = [row.strip() for row in f]

with open('adspowerids.txt','r') as f:
    ids = [row.strip() for row in f]
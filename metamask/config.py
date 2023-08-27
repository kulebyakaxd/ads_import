mmidentifikator = ''  # введите идентификатор расширения

password = '' # введите пароль для всех кошельков argent

with open('mnemonic.txt','r') as f:
    seeds = [row.strip() for row in f]

with open('adspowerids.txt','r') as f:
    ids = [row.strip() for row in f]
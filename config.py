#!/bin/python3
# MySQL Configurations

host = "localhost"
database = "emailscraper"
myuser = "root"
mypass = "root"

# Badwords

badwords = ['sentry', 'deliveroo', '.png', '.webp', '.jpg', 'x22', 'u003', '.gif', 'trustpilot']
badwords.extend(['.js', '.heic',  '.jpeg', 'godaddy', 'name', 'example.com', 'domain.com'])
badwords.extend(['email', 'username', 'opencart', 'zipify', '.global', 'EXCLUDING',])
badwords.extend(['Q@3SU.DP', 'm@X.W', 'IS@k.v', 'lite.lt', 'template', 'checkout', 'widgets'])
badwords.extend(['example', 'company.com', 'i@+.M', 'Im@K.Z', 'O@i.a', 'q@A.q', 'w@Z.H,', 'Wz6@V.n'])
badwords.extend(['Z@U.D', 'G@EIr.u', 'Z@U.D', 'Wz6@V.n', 'w@Z.H', 'V@b.T', 'q@A.q', 'O@i.a', 'Im@K.Z'])
#badwords.extend([''])

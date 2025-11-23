pip freeze > requirements.txt

docker-compose up -d
ssh -R 80:localhost:8443 nokey@localhost.run
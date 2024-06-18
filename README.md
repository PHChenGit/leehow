這個 project 取名 leehow 有兩個意思
取中文諧音 你好，就像在對 leetcode 說你好
how 這個字有點怎麼做的意思在，就像我們在解題的時候 常常在寫怎麼寫

# Launch services
```
docker compose up -d
```

# Create db tables
## Enter db
```
mariadb -u leehao -pleehao leehao
```

## Show all databases
```
SHOW DATABASES;
```

## Create tables
```
USE leehao;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Check table created successfully
```
SHOW TABLES;
```
## Go to leehow app docker container and launch app
```
docker compose exec -it leehao sh
python main.py
```


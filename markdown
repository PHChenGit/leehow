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



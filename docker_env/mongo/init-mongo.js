db = db.getSiblingDB('normal'); // 切换到要创建的数据库

db.createUser({
    user: 'normal',
    pwd: '123456',
    roles: ["readWrite", "dbAdmin"]
});
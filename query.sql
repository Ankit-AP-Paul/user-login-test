create table users (
    username varchar(255),
    role varchar(255) default "user",
    mail_id varchar(255) primary key,
    password_ varchar(255),
    age int,
    weight double,
    height double,
    created_at timestamp default current_timestamp
);
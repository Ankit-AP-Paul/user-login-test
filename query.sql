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

create table smear_detail (
    id int auto_increment primary key,
    image longblob,
    result varchar(255),
    user_id varchar(255),
    status_ varchar(255),
    created_at timestamp default current_timestamp,
    foreign key (user_id) references users(mail_id)
);
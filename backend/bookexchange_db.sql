create table users {
    user_id serial primary key,
    username varchar(255),
    birthday date,
    email varchar(255) unique not null,
    avatar_url varchar(255),
    password_hash varchar(255) not null
};

create table books {
    book_id serial primary key,
    title varchar(255),
    author varchar(255),
    genre varchar(255),
    descr varchar(300)
};

create table locations {
    loc_id serial primary key,
    country varchar(255),
    city varchar(255),
    street varchar(255),
    house varchar(255),
    descr varchar(255),
};

create table bookings {
    bk_id serial primary key,
    user_id integer references users(user_id),
    book_id integer references books(book_id),
    loc_id integer references locations(loc_id),
    time_created timestamp not null default current_timestamp,
    time_due timestamp,
    time_closed timestamp,
    stat varchar(255) not null default 'pending',
    constraint stock_id
        foreign key (book_id, loc_id)
        references stock(book_id, loc_id)
};

create table stock {
    book_id integer not null references books(book_id),
    loc_id integer not null references locations(loc_id),
    available integer default 0 check (available >= 0),
    reserved integer default 0 check (reserved >= 0),
    constraint stock_id primary key (book_id, loc_id)
};

create table users {
    user_id serial primary key,
    username varchar(100),
    birthday date,
    email varchar(100) unique not null,
    avatar varchar(100),
    pass varchar(100) not null
};

create table books {
    book_id integer primary key,
    title varchar(100),
    author varchar(100),
    genre varchar(100),
    descr varchar(300)
};

create table locations {
    loc_id serial primary key,
    country varchar(100),
    city varchar(100),
    street varchar(100),
    house varchar(100),
    descr varchar(300),
};

create table bookings {
    bk_id integer,
    user_id integer references users(user_id),
    book_id integer references books(book_id),
    loc_id integer references locations(loc_id),
    time_created timestamp not null default current_timestamp,
    time_due timestamp,
    time_closed timestamp,
    stat varchar(100) not null default 'pending',
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

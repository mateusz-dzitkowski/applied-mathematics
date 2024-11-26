-- migrate:up
create table user_ (
    handle varchar primary key,
    created_at timestamp with time zone not null default now(),

    name varchar not null,
    description varchar,
    following int not null,
    followers int not null
);

-- replies are also tweets
create table tweet (
    id bigint primary key,
    created_at timestamp with time zone not null default now(),

    tweeted_at timestamp with time zone not null,
    text varchar not null,
    replies int not null,
    retweets int not null,
    likes int not null,
    views int not null,

    user_handle varchar not null,
    parent_id int,

    constraint fk_user foreign key (user_handle) references user_(handle),
    constraint fk_self foreign key (parent_id) references tweet(id)
);


-- migrate:down
drop table tweet;
drop table user_;

-- name: CreateUser :exec
insert into user_ (handle, name, description, following, followers)
values ($1, $2, $3, $4, $5);

-- name: DoesUserExist :one
select exists(select 1 from user_ where handle=$1);

-- name: CreateTweet :exec
insert into tweet (id, tweeted_at, text, replies, retweets, likes, views, user_handle, parent_id)
values ($1, $2, $3, $4, $5, $6, $7, $8, $9);

-- name: DoesTweetExist :one
select exists(select 1 from tweet where id=$1);

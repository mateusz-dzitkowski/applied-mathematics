create table mati_test_raw as
select * from read_csv_auto('tweets-data/*.csv', ignore_errors = true);

create table mati_test as
with deduped as (
    select
        *,
        row_number() over (partition by full_text) as rn
    from mati_test_raw
)
select * exclude (rn)
from deduped
where rn=1;

create table output as
select
    conversation_id_str,
    strptime(created_at, '%a %b %d %H:%M:%S %z %Y') as created_at,
    favorite_count,
    full_text,
    id_str,
    image_url,
    in_reply_to_screen_name,
    lang,
    location,
    quote_count,
    reply_count,
    retweet_count,
    tweet_url,
    user_id_str,
    username,
from mati_test;

copy output to 'twitter_test.csv';

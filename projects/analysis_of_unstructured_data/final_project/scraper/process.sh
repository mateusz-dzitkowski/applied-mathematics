find tweets-data -size 1 -print -delete  # remove all files with just a newline in them
duckdb -c ".read process.sql"  # dedup the data, transform the created_at column to be usable, save to twitter_test.csv

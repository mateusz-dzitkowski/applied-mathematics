source .env
parallel -j 3 npx tweet-harvest@latest --token "$ACCESS_TOKEN" --search-keyword {} --limit 1000 :::: args

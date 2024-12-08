source .env
parallel -j 3 npx tweet-harvest@latest --token "$TOKEN" --search-keyword {} --limit 20 :::: args

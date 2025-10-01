#!/bin/bash
# Update API key index to 10 in .env
sed -i '' 's/LIGHTER_API_KEY_INDEX=0/LIGHTER_API_KEY_INDEX=10/g' .env
echo "Updated LIGHTER_API_KEY_INDEX to 10"

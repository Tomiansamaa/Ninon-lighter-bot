#!/bin/bash
# Update API key index in .env
sed -i '' 's/LIGHTER_API_KEY_INDEX=2/LIGHTER_API_KEY_INDEX=0/g' .env
echo "Updated LIGHTER_API_KEY_INDEX to 0"

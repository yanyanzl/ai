# ai
first ai project
### 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

curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $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" \
  -d '{
     "model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": "Say this is a test!"}],
     "temperature": 0.7
   }'
# ner модель для определения сущностей в тексте

## how to run locally

```
git clone https://github.com/dottokyo/nerx5_search.git
```
```
pip install -r requirements.txt
```
```
cd nerx5_search
gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app --bind "0.0.0.0:8080"
```
"-w 2" - number of raised workers

"-bind x" - binding address

### пример запроса
```
curl -X POST https://nerx5search-production.up.railway.app/api/predict \
     -H "Content-Type: application/json" \
     -d '{"input": "молоко"}'
```
### пример респонса
```
[{"start_index":0,"end_index":6,"entity":"B-TYPE"}]%    
```
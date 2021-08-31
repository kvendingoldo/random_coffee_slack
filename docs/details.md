# for local development

```
export $(cat .env | egrep -v "(^#.*|^$)" | xargs)
```

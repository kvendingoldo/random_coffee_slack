## Useful commands for local development

### export all .env variables as environment variables
```
export $(cat .env | egrep -v "(^#.*|^$)" | xargs)
```

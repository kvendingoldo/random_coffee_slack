## Useful commands for local development

### export all .env variables as environment variables
```
export $(cat .env | egrep -v "(^#.*|^$)" | xargs)
```

### show meets on this week in human-readable format

```sql
SELECT u1.username, u2.username, meet.season, meet.completed FROM meet
    JOIN user u1 on meet.uid1 = u1.id
    JOIN user u2 on meet.uid2 = u2.id
    WHERE meet.season = '<SEASON>';
```

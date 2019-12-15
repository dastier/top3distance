# Top3distance
The top3distance app can do the following:
 - store users location (latitude, longitude)
 - populate a database with generated random user locations (5 different nationalities, 1000 users for each)
 - has a [query](query_distance.sql) to show top 3 the most distant users for each nationality

## How to run this app

1. install Docker and Docker Compose
2. run the following commands:

```sql
  $ git clone https://github.com/dastier/top3distance.git
  $ cd top3distance/
  $ docker-compose up --build
```

### Query to get top 3 the most distant users for each nationality

```sql
WITH all_distances AS
  (SELECT DISTINCT ON (distance) nationality,
                      id AS user_id_1,
                      secondid AS user_id_2,
                      distance AS "distance (в метрах)"
   FROM
     (SELECT name,
             nationality,
             nat_points.id,
             (point(u.longitude, u.latitude)<@>point(nat_points.longitude, nat_points.latitude)) * 1609.344 AS distance,
             u.id AS secondid
      FROM users u,
           LATERAL
        (SELECT id,
                latitude,
                longitude
         FROM users
         WHERE nationality = u.nationality) AS nat_points
      WHERE u.id <> nat_points.id
        AND nationality = u.nationality
      ORDER BY distance DESC) AS g1
   ORDER BY distance DESC)
  (SELECT *
   FROM all_distances
   WHERE nationality = 'Belarusian'
   ORDER BY "distance (в метрах)" DESC FETCH FIRST 3 ROWS ONLY)
UNION
  (SELECT *
   FROM all_distances
   WHERE nationality = 'Polish'
   ORDER BY "distance (в метрах)" DESC FETCH FIRST 3 ROWS ONLY)
UNION
  (SELECT *
   FROM all_distances
   WHERE nationality = 'Lithuanian'
   ORDER BY "distance (в метрах)" DESC FETCH FIRST 3 ROWS ONLY)
UNION
  (SELECT *
   FROM all_distances
   WHERE nationality = 'Latvian'
   ORDER BY "distance (в метрах)" DESC FETCH FIRST 3 ROWS ONLY)
UNION
  (SELECT *
   FROM all_distances
   WHERE nationality = 'Ukrainian'
   ORDER BY "distance (в метрах)" DESC FETCH FIRST 3 ROWS ONLY)
ORDER BY "distance (в метрах)" DESC,
         nationality ASC;
```

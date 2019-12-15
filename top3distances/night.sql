WITH cte_table_name AS
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
   FROM cte_table_name
   WHERE nationality = 'Belarusian'
   ORDER BY "distance (в метрах)" DESC FETCH FIRST 3 ROWS ONLY)
UNION
  (SELECT *
   FROM cte_table_name
   WHERE nationality = 'Polish'
   ORDER BY "distance (в метрах)" DESC FETCH FIRST 3 ROWS ONLY)
UNION
  (SELECT *
   FROM cte_table_name
   WHERE nationality = 'Lithuanian'
   ORDER BY "distance (в метрах)" DESC FETCH FIRST 3 ROWS ONLY)
UNION
  (SELECT *
   FROM cte_table_name
   WHERE nationality = 'Latvian'
   ORDER BY "distance (в метрах)" DESC FETCH FIRST 3 ROWS ONLY)
UNION
  (SELECT *
   FROM cte_table_name
   WHERE nationality = 'Ukrainian'
   ORDER BY "distance (в метрах)" DESC FETCH FIRST 3 ROWS ONLY)
ORDER BY "distance (в метрах)" DESC,
         nationality ASC;
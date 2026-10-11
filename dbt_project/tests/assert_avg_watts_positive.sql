
SELECT *
FROM {{ ref('mart_server_efficiency') }}
WHERE avg_watts_100 <= 0
   OR avg_watts_100 IS NULL

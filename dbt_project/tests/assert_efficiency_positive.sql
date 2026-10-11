
SELECT *
FROM {{ ref('mart_server_efficiency') }}
WHERE ssj_ops_per_watt <= 0
   OR ssj_ops_per_watt IS NULL

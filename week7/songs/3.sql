SELECT name FROM songs
GROUP BY duration_ms
ORDER BY COUNT(duration_ms) DESC
LIMIT 5;

// Jockey performance with earnings by meeting

//
MATCH (:Jockey)-[ride:RODE]->(:Horse)
  WHERE ride.placing IS NOT NULL
WITH DISTINCT ride.raceDate AS raceDate
  ORDER BY raceDate DESC
  LIMIT 25

MATCH (j:Jockey)-[ride:RODE]->(:Horse)
  WHERE ride.raceDate = raceDate
  AND ride.placing > 0
WITH j.nameEn AS jockey,
     ride.raceDate AS raceDate,
     ride.raceNum AS raceNum,
     ride.placing AS placing

MATCH (p:Pool)
  WHERE p.raceDate = raceDate
  AND p.raceNum = raceNum
  AND p.winOdds IS NOT NULL
WITH jockey, raceDate, raceNum, placing,
     CASE
       WHEN placing = 1 THEN p.winOdds[0]
       WHEN placing = 2 THEN p.placeOdds[1]
       WHEN placing = 3 THEN p.placeOdds[2]
       WHEN placing = 4 THEN 1
       ELSE 0
       END AS earning

//
WITH jockey, raceDate,
     collect(placing) AS placings,
     round(sum(earning), 1, 'HALF_UP') AS earnings

WITH jockey, raceDate, earnings,
     size(placings) AS rides,
     size([p IN placings WHERE p = 1]) AS wins,
     size([p IN placings WHERE p = 2]) AS seconds,
     size([p IN placings WHERE p = 3]) AS thirds,
     size([p IN placings WHERE p = 4]) AS fourths

WITH raceDate,
     toInteger(sum(earnings)) AS dayEarns,
     collect({
       jockey:   jockey,
       earnings: earnings,
       rides:    rides,
       wins:     wins,
       seconds:  seconds,
       thirds:   thirds,
       fourths:  fourths
     }) AS data

//
MATCH (r:Race)
  WHERE r.date = raceDate
  AND r.dayOrdinal = 1
WITH raceDate, dayEarns, data,
     r.venue AS venue

MATCH (r:Race)
  WHERE r.date = raceDate
WITH raceDate, venue, dayEarns, data,
     size(collect(r)) AS races

RETURN
  toString(raceDate) AS raceDate,
  venue, races, dayEarns, data
;

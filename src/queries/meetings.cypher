// Person performance with earnings by meeting
// Replace 'RODE' with 'TRAINED' for trainers

MATCH (p)-[rel:RODE]->(:Horse)
  WHERE rel.placing IS NOT NULL
WITH DISTINCT rel.raceDate AS raceDate
  ORDER BY raceDate DESC
  LIMIT 10

MATCH (p)-[rel:RODE]->(:Horse)
  WHERE rel.raceDate = raceDate
  AND rel.placing > 0
WITH p.nameEnAbbr AS person,
     rel.raceDate AS raceDate,
     rel.raceNum AS raceNum,
     rel.placing AS placing

MATCH (p:Pool)
  WHERE p.raceDate = raceDate
  AND p.raceNum = raceNum
  AND p.winOdds IS NOT NULL
WITH person, raceDate, raceNum, placing,
     CASE
       WHEN placing = 1 THEN p.winOdds[0]
       WHEN placing = 2 THEN p.placeOdds[1]
       WHEN placing = 3 THEN p.placeOdds[2]
     //         WHEN placing = 4 THEN 1
       ELSE 0
       END AS earning

//
WITH person, raceDate,
     collect(placing) AS placings,
     round(sum(earning), 1, 'HALF_UP') AS earnings

WITH person, raceDate, earnings,
     size(placings) AS engagements,
     size([p IN placings WHERE p = 1]) AS wins,
     size([p IN placings WHERE p = 2]) AS seconds,
     size([p IN placings WHERE p = 3]) AS thirds,
     size([p IN placings WHERE p = 4]) AS fourths

WITH raceDate,
     toInteger(sum(earnings)) AS turnover,
     collect({
       person:      person,
       earnings:    earnings,
       engagements: engagements,
       wins:        wins,
       seconds:     seconds,
       thirds:      thirds,
       fourths:     fourths
     }) AS data

// gather basic race day info
MATCH (r:Race)
  WHERE r.date = raceDate
  AND r.dayOrdinal = 1
WITH raceDate, turnover, data,
     r.venue AS venue

MATCH (r:Race)
  WHERE r.date = raceDate
WITH raceDate, venue, turnover, data,
     size(collect(r)) AS races

RETURN
  toString(raceDate) AS meeting,
  venue, races, turnover, data
;
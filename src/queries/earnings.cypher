// Person earnings during a specified period
// Replace 'RODE' with 'TRAINED' for trainers
// Input: startDate, endDate

// find out the earning for each person each race
MATCH (p)-[rel:RODE]->(:Horse)
  WHERE rel.raceDate >= $startDate
  AND rel.raceDate <= $endDate
WITH p.nameEnAbbr AS person,
     rel.raceDate AS raceDate,
     rel.raceNum AS raceNum,
     rel.placing AS placing,
     rel.winOdds AS winOdds

MATCH (p:Pool)
  WHERE p.raceDate = raceDate
  AND p.raceNum = raceNum
  AND p.winOdds IS NOT NULL
  AND p.placeOdds IS NOT NULL
WITH person, raceDate, raceNum, placing,
     CASE
       WHEN placing = 1 THEN p.winOdds[0]
       WHEN placing = 2 THEN p.placeOdds[1]
       WHEN placing = 3 AND size(p.placeOdds) > 2 THEN p.placeOdds[2]
       WHEN placing = 3 OR placing = 4 THEN winOdds / 10
       ELSE 0
       END AS earning

// group each person's earning by race meeting
WITH person, raceDate,
     sum(earning) AS dayEarning

WITH person,
     sum(dayEarning) AS totalEarns,
     collect(dayEarning) AS dayEarnings

WITH person, totalEarns,
     size(dayEarnings) AS engageDays,
     size([e IN dayEarnings WHERE e > 0]) AS earnDays,
     size([e IN dayEarnings WHERE e > 0 AND e < 7]) AS poor,
     size([e IN dayEarnings WHERE e >= 7 AND e < 12]) AS normal,
     size([e IN dayEarnings WHERE e >= 12]) AS rich

// only return the 'regular' people who ran top 4 at least once
  WHERE engageDays > 1
  AND earnDays > 0

WITH person, engageDays, earnDays,
     round(totalEarns, 1, 'HALF_UP') AS totalEarns,
     round(totalEarns / earnDays, 1, 'HALF_UP') AS earnDayAvg,
     round(totalEarns / engageDays, 1, 'HALF_UP') AS engageDayAvg,
     round(1.0 * poor / earnDays, 2) AS poor,
     round(1.0 * normal / earnDays, 2) AS normal,
     round(1.0 * rich / earnDays, 2) AS rich

RETURN
  person, engageDays, earnDays, totalEarns,
  earnDayAvg, engageDayAvg,
  round((earnDayAvg + engageDayAvg) / 2, 1, 'HALF_UP') AS AvgAvg,
  poor, normal, rich
  ORDER BY
  totalEarns DESC,
  earnDayAvg DESC
;
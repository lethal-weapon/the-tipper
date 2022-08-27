// Person earnings during a specified period note that
// this period should contain at least 3 race meetings
// Replace 'RODE' with 'TRAINED' for trainers
// Input: startDate, endDate

// find out the earning for each person each race
MATCH (p)-[rel:RODE]->(:Horse)
  WHERE rel.raceDate >= $startDate
  AND rel.raceDate <= $endDate
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
     //       WHEN placing = 4 THEN 1
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

// this condition is used for excluding special persons
// who only engage for a few days during a long period of time
  WHERE engageDays >= 3

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
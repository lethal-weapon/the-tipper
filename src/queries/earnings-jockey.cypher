// Jockey Earnings during a specified period, note that
// this period should contain at least 3 race meetings
// Input: startMeeting, endMeeting

// find out the earning for each jockey each race
MATCH (j:Jockey)-[ride:RODE]->(:Horse)
  WHERE ride.raceDate >= $startMeeting
  AND ride.raceDate <= $endMeeting
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
       ELSE 0
       END AS earning

// group each jockey's earning by race meeting
WITH jockey, raceDate,
     sum(earning) AS dayEarning

WITH jockey,
     sum(dayEarning) AS totalEarns,
     collect(dayEarning) AS dayEarnings

WITH jockey, totalEarns,
     size(dayEarnings) AS rideDays,
     size([e IN dayEarnings WHERE e > 0]) AS earnDays,
     size([e IN dayEarnings WHERE e > 0 AND e <= 7]) AS poor,
     size([e IN dayEarnings WHERE e > 7 AND e <= 12]) AS regular,
     size([e IN dayEarnings WHERE e > 12]) AS rich

// this condition is used for excluding special jockeys
// who only rode for a few days during a long period of time
  WHERE rideDays >= 3

WITH jockey, rideDays, earnDays,
     round(totalEarns, 1, 'HALF_UP') AS totalEarns,
     round(totalEarns / earnDays, 1, 'HALF_UP') AS earnDayAvg,
     round(totalEarns / rideDays, 1, 'HALF_UP') AS rideDayAvg,
     round(1.0 * poor / earnDays, 2) AS poor,
     round(1.0 * regular / earnDays, 2) AS regular,
     round(1.0 * rich / earnDays, 2) AS rich

RETURN jockey, rideDays, earnDays,
       totalEarns, earnDayAvg, rideDayAvg,
       round((earnDayAvg + rideDayAvg) / 2, 1, 'HALF_UP') AS realAvg,
       poor, regular, rich
  ORDER BY
  totalEarns DESC,
  earnDayAvg DESC
;
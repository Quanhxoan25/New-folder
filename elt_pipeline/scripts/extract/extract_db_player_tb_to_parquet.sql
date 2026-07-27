SELECT
    p.personID,
    p.countryID,
    p.schoolID,
    p.draftYear,
    p.draftRound,
    p.draftNumber,
    p.firstName,
    p.lastName,
    p.birthDate,
    p.heightInches,
    p.bodyWeightLbs, 
    p.jersey, 
    p.guard,
    p.forward,
    p.center,
    p.dleagueFlag,
    p.nbaFlag,
    p.gamesPlayedFlag,
    p.fromYear,
    p.toYear,
    c.country,
    s.school
from players p 
left join country c on p.countryid =c.countryid 
left join school s on p.schoolid = s.schoolid
where p.updated_at >= CURRENT_DATE 
    AND p.updated_at < CURRENT_DATE + INTERVAL '1 day';
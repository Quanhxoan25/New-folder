SELECT 
    tl.team_leagueid,
    tl.teamid,
    tl.leagueid,
    tl.cityid,
    tl.teamname,
    tl.teamabbrev,
    tl.seasonfounded,
    tl.seasonactivetill,
    c.city,
    l.league
from team_league tl 
left join city c on tl.cityid  = c.cityid
left join league l on tl.leagueid = l.leagueid
where tl.updated_at >= CURRENT_DATE 
    AND tl.updated_at < CURRENT_DATE + INTERVAL '1 day';

create table if not exists country (
  countryID SERIAL primary key,
  country varchar(100) unique not null,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

create table if not exists school (
  schoolID SERIAL primary key,
  school varchar(100) unique not null,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

create table if not exists players (
  personID int primary key not null,
  countryID int not null,
  schoolID int not null,
  draftYear int not null,
  draftRound int not null,
  draftNumber int not null,
  firstName varchar(50) not null,
  lastName varchar(50) not null,
  birthDate date not null,
  heightInches int not null,
  bodyWeightLbs int not null, 
  jersey varchar(20) not null, 
  guard int not null,
  forward int not null,
  center int not null,
  dleagueFlag int not null,
  nbaFlag int not null,
  gamesPlayedFlag int not null,
  fromYear int not null,
  toYear int,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT fk_player_country
        FOREIGN KEY(countryID)
        REFERENCES country(countryID),
  CONSTRAINT fk_player_school
        FOREIGN KEY(schoolID)
        REFERENCES school(schoolID),
  unique (firstName, lastName, birthDate)
);

create table if not exists Team (
  teamID int primary key not null,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

create table if not exists city (
  cityID serial primary key,
  city varchar(50) unique not null,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

create table if not exists league(
  leagueID serial primary key,
  league varchar(100) unique not null,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

create table if not exists team_league (
  team_leagueID serial primary key,
  teamID int not null, 
  leagueID int not null,
  cityID int not null,
  teamName VARCHAR(100) not null,
  teamabbrev VARCHAR(10) not null,
  seasonFounded int not null,
  seasonActiveTill int not null,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT fk_team
        FOREIGN KEY(teamID)
        REFERENCES team(teamID),
	CONSTRAINT fk_league
	    FOREIGN KEY(leagueID)
	    REFERENCES league(leagueID),
	    constraint fk_city
	    	foreign key (cityID)
	    	references city(cityID),
    UNIQUE(teamID, cityID, seasonFounded)
);

create index idx_players_countryID on players(countryID);
create index idx_players_schoolID on players(schoolID);
CREATE INDEX idx_players_created_at ON players(created_at);
CREATE INDEX idx_players_updated_at ON players(updated_at);

create index idx_team_league_leagueID on team_league(leagueID);
create index idx_team_league_cityID on team_league(cityID);
CREATE INDEX idx_teams_created_at ON team_league(created_at);
CREATE INDEX idx_teams_updated_at ON team_league(created_at);

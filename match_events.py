"""
Hardcoded Premier League matches (2025/26, matchday 38, 24 May 2026).
Goals, substitutions, and match metadata — no external API required.
"""

HARDCODED_MATCH_DATA: dict[int, dict] = {
    538160: {
        "utcDate": "2026-05-24T15:00:00Z",
        "homeTeam": {
            "id": 64,
            "name": "Liverpool FC",
            "shortName": "Liverpool",
        },
        "awayTeam": {
            "id": 402,
            "name": "Brentford FC",
            "shortName": "Brentford",
        },
        "score": {"fullTime": {"home": 1, "away": 1}},
        "goals": [
            {"minute": 58, "team": "home", "home": 1, "away": 0},
            {"minute": 64, "team": "away", "home": 1, "away": 1},
        ],
        "substitutions": [
            {
                "minute": 60,
                "team": "away",
                "playerOut": "Jordan Henderson",
                "playerIn": "Aaron Hickey",
            },
            {
                "minute": 73,
                "team": "home",
                "playerOut": "Rio Ngumoha",
                "playerIn": "Florian Wirtz",
            },
            {
                "minute": 74,
                "team": "home",
                "playerOut": "Mohamed Salah",
                "playerIn": "Jeremie Frimpong",
            },
            {
                "minute": 83,
                "team": "home",
                "playerOut": "Andrew Robertson",
                "playerIn": "Milos Kerkez",
            },
            {
                "minute": 83,
                "team": "home",
                "playerOut": "Ryan Gravenberch",
                "playerIn": "Trey Nyoni",
            },
            {
                "minute": 83,
                "team": "away",
                "playerOut": "Mathias Jensen",
                "playerIn": "Mikkel Damsgaard",
            },
            {
                "minute": 89,
                "team": "home",
                "playerOut": "Ibrahima Konaté",
                "playerIn": "Joseph Gomez",
            },
            {
                "minute": 89,
                "team": "away",
                "playerOut": "Vitaly Janelt",
                "playerIn": "Reiss Nelson",
            },
        ],
    },
    538157: {
        "utcDate": "2026-05-24T15:00:00Z",
        "homeTeam": {
            "id": 354,
            "name": "Crystal Palace FC",
            "shortName": "Crystal Palace",
        },
        "awayTeam": {
            "id": 57,
            "name": "Arsenal FC",
            "shortName": "Arsenal",
        },
        "score": {"fullTime": {"home": 1, "away": 2}},
        "goals": [
            {"minute": 42, "team": "away", "home": 0, "away": 1},
            {"minute": 48, "team": "away", "home": 0, "away": 2},
            {"minute": 89, "team": "home", "home": 1, "away": 2},
        ],
        "substitutions": [
            {
                "minute": 45,
                "team": "home",
                "playerOut": "Daniel Muñoz",
                "playerIn": "Tyrick Mitchell",
            },
            {
                "minute": 45,
                "team": "home",
                "playerOut": "Daichi Kamada",
                "playerIn": "Yeremy Pino",
            },
            {
                "minute": 45,
                "team": "home",
                "playerOut": "Ismaila Sarr",
                "playerIn": "Adam Wharton",
            },
            {
                "minute": 45,
                "team": "away",
                "playerOut": "Riccardo Calafiori",
                "playerIn": "Gabriel",
            },
            {
                "minute": 45,
                "team": "away",
                "playerOut": "Christian Nørgaard",
                "playerIn": "Kai Havertz",
            },
            {
                "minute": 62,
                "team": "home",
                "playerOut": "Adam Wharton",
                "playerIn": "Evann Guessand",
            },
            {
                "minute": 62,
                "team": "away",
                "playerOut": "Max Dowman",
                "playerIn": "Mikel Merino",
            },
            {
                "minute": 75,
                "team": "away",
                "playerOut": "Gabriel Jesus",
                "playerIn": "Eberechi Eze",
            },
            {
                "minute": 77,
                "team": "home",
                "playerOut": "Jørgen Strand Larsen",
                "playerIn": "Jean-Philippe Mateta",
            },
            {
                "minute": 83,
                "team": "away",
                "playerOut": "Noni Madueke",
                "playerIn": "Viktor Gyökeres",
            },
        ],
    },
    538161: {
        "utcDate": "2026-05-24T15:00:00Z",
        "homeTeam": {
            "id": 65,
            "name": "Manchester City FC",
            "shortName": "Man City",
        },
        "awayTeam": {
            "id": 58,
            "name": "Aston Villa FC",
            "shortName": "Aston Villa",
        },
        "score": {"fullTime": {"home": 1, "away": 2}},
        "goals": [
            {"minute": 23, "team": "home", "home": 1, "away": 0},
            {"minute": 47, "team": "away", "home": 1, "away": 1},
            {"minute": 61, "team": "away", "home": 1, "away": 2},
        ],
        "substitutions": [
            {
                "minute": 45,
                "team": "away",
                "playerOut": "Andrés García",
                "playerIn": "Matty Cash",
            },
            {
                "minute": 58,
                "team": "home",
                "playerOut": "Antoine Semenyo",
                "playerIn": "Rayan Cherki",
            },
            {
                "minute": 59,
                "team": "home",
                "playerOut": "Bernardo Silva",
                "playerIn": "Mateo Kovačić",
            },
            {
                "minute": 73,
                "team": "away",
                "playerOut": "Victor Lindelöf",
                "playerIn": "Pau Torres",
            },
            {
                "minute": 73,
                "team": "away",
                "playerOut": "Ian Maatsen",
                "playerIn": "Amadou Onana",
            },
            {
                "minute": 73,
                "team": "away",
                "playerOut": "Lamare Bogarde",
                "playerIn": "Youri Tielemans",
            },
            {
                "minute": 77,
                "team": "home",
                "playerOut": "John Stones",
                "playerIn": "Jérémy Doku",
            },
            {
                "minute": 77,
                "team": "home",
                "playerOut": "Nathan Aké",
                "playerIn": "Rayan Aït-Nouri",
            },
            {
                "minute": 78,
                "team": "home",
                "playerOut": "Savinho",
                "playerIn": "Josko Gvardiol",
            },
            {
                "minute": 86,
                "team": "away",
                "playerOut": "Ross Barkley",
                "playerIn": "John McGinn",
            },
        ],
    },
    538159: {
        "utcDate": "2026-05-24T15:00:00Z",
        "homeTeam": {
            "id": 63,
            "name": "Fulham FC",
            "shortName": "Fulham",
        },
        "awayTeam": {
            "id": 67,
            "name": "Newcastle United FC",
            "shortName": "Newcastle",
        },
        "score": {"fullTime": {"home": 2, "away": 0}},
        "goals": [
            {"minute": 20, "team": "home", "home": 1, "away": 0},
            {"minute": 80, "team": "home", "home": 2, "away": 0},
        ],
        "substitutions": [
            {
                "minute": 45,
                "team": "away",
                "playerOut": "Jacob Murphy",
                "playerIn": "Harvey Barnes",
            },
            {
                "minute": 60,
                "team": "home",
                "playerOut": "Kevin Santos Lopes de Macedo",
                "playerIn": "Tom Cairney",
            },
            {
                "minute": 66,
                "team": "away",
                "playerOut": "Jacob Ramsey",
                "playerIn": "Anthony Elanga",
            },
            {
                "minute": 66,
                "team": "away",
                "playerOut": "William Osula",
                "playerIn": "Yoane Wissa",
            },
            {
                "minute": 72,
                "team": "home",
                "playerOut": "Ollie Bobb",
                "playerIn": "Raúl Jiménez",
            },
            {
                "minute": 72,
                "team": "home",
                "playerOut": "Emile Smith Rowe",
                "playerIn": "Harry Wilson",
            },
            {
                "minute": 72,
                "team": "home",
                "playerOut": "Rodrigo Muniz",
                "playerIn": "Joshua King",
            },
            {
                "minute": 77,
                "team": "away",
                "playerOut": "Nick Woltemade",
                "playerIn": "Stanley Neave",
            },
            {
                "minute": 86,
                "team": "home",
                "playerOut": "Ibrahima Diop",
                "playerIn": "Jorge Cuenca",
            },
            {
                "minute": 84,
                "team": "away",
                "playerOut": "Dan Burn",
                "playerIn": "Jacob Murphy",
            },
        ],
    },
    538156: {
        "utcDate": "2026-05-24T15:00:00Z",
        "homeTeam": {
            "id": 397,
            "name": "Brighton & Hove Albion FC",
            "shortName": "Brighton",
        },
        "awayTeam": {
            "id": 66,
            "name": "Manchester United FC",
            "shortName": "Man United",
        },
        "score": {"fullTime": {"home": 0, "away": 3}},
        "goals": [
            {"minute": 33, "team": "away", "home": 0, "away": 1},
            {"minute": 44, "team": "away", "home": 0, "away": 2},
            {"minute": 48, "team": "away", "home": 0, "away": 3},
        ],
        "substitutions": [
            {
                "minute": 45,
                "team": "home",
                "playerOut": "Maxim De Cuyper",
                "playerIn": "Yankuba Minteh",
            },
            {
                "minute": 59,
                "team": "home",
                "playerOut": "James Milner",
                "playerIn": "Solly March",
            },
            {
                "minute": 59,
                "team": "home",
                "playerOut": "Diego Gómez",
                "playerIn": "Carlos Baleba",
            },
            {
                "minute": 59,
                "team": "home",
                "playerOut": "Danny Welbeck",
                "playerIn": "Charalampos Kostoulas",
            },
            {
                "minute": 62,
                "team": "away",
                "playerOut": "Patrick Dorgu",
                "playerIn": "Sam Lacey",
            },
            {
                "minute": 74,
                "team": "home",
                "playerOut": "Jack Hinshelwood",
                "playerIn": "Georginio Rutter",
            },
            {
                "minute": 74,
                "team": "away",
                "playerOut": "Noussair Mazraoui",
                "playerIn": "Leny Yoro",
            },
            {
                "minute": 74,
                "team": "away",
                "playerOut": "Mason Mount",
                "playerIn": "Joshua Zirkzee",
            },
            {
                "minute": 74,
                "team": "away",
                "playerOut": "Bryan Mbeumo",
                "playerIn": "Tyler Fletcher",
            },
            {
                "minute": 82,
                "team": "away",
                "playerOut": "Luke Shaw",
                "playerIn": "Tyrell Malacia",
            },
        ],
    },
}


def _team_for_side(match_data: dict, side: str) -> dict:
    return match_data["homeTeam"] if side == "home" else match_data["awayTeam"]


def _score_at_minute(goals: list[dict], minute: int) -> str:
    home, away = 0, 0
    for goal in sorted(goals, key=lambda g: g["minute"]):
        if goal["minute"] > minute:
            break
        home, away = goal["home"], goal["away"]
    return f"{home}-{away}"


def build_match(match_id: int) -> dict:
    """Build a full match object with normalized goals and substitutions."""
    raw = HARDCODED_MATCH_DATA[match_id]
    home_team = raw["homeTeam"]
    away_team = raw["awayTeam"]
    goal_rows = sorted(raw["goals"], key=lambda g: g["minute"])

    goals = [
        {
            "minute": g["minute"],
            "team": _team_for_side(raw, g["team"]),
            "score": {"home": g["home"], "away": g["away"]},
        }
        for g in goal_rows
    ]

    substitutions = []
    for s in raw["substitutions"]:
        substitutions.append(
            {
                "minute": s["minute"],
                "team": _team_for_side(raw, s["team"]),
                "playerOut": {"name": s["playerOut"]},
                "playerIn": {"name": s["playerIn"]},
                "scoreline": _score_at_minute(goal_rows, s["minute"]),
            }
        )

    return {
        "id": match_id,
        "utcDate": raw["utcDate"],
        "homeTeam": home_team,
        "awayTeam": away_team,
        "score": raw["score"],
        "goals": goals,
        "substitutions": substitutions,
    }


def match_label(match: dict) -> str:
    home = match["homeTeam"]["shortName"]
    away = match["awayTeam"]["shortName"]
    ft = match["score"]["fullTime"]
    date = match["utcDate"][:10]
    return f"{home} {ft['home']}–{ft['away']} {away} ({date})"


def list_matches() -> list[dict]:
    """Return all hardcoded matches, most recent first."""
    return list(ALL_MATCHES)


def get_match(match_id: int) -> dict:
    """Return a single match by ID (from local data only)."""
    return MATCH_BY_ID[match_id]


# Pre-built at import — no network, no API calls
ALL_MATCHES: list[dict] = sorted(
    (build_match(match_id) for match_id in HARDCODED_MATCH_DATA),
    key=lambda m: m["utcDate"],
    reverse=True,
)
MATCH_BY_ID: dict[int, dict] = {m["id"]: m for m in ALL_MATCHES}

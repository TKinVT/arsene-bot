import datetime

from arsenal import arsenal_api

COMPETITION_DICT = {
    'Premier League': 'PL',
    'League Cup': 'LC',
    'FA Cup': 'FA',
    'Club Friendlies': 'Fr',
    'Friendlies Clubs': 'Fr'
}


def parser(text):
    text = text.lower()

    options = {
        '': get_info,
        'fixtures': get_fixtures,
        'results': get_results,
        'scores': get_results,
        'squad': get_squad,
        'table': get_table,
        'team': get_squad
    }

    if text in options:
        return options[text]()
    else:
        return help_info


help_info = """
    *Ask Arsene about :arsenal:*
    `/ars` to get basic info: Next match, last result
    To see the upcoming fixtures, type `/ars fixtures`
    For the latest scores: `/ars results`
    """


def get_info():
    results = arsenal_api.results()[:3]
    results_text = f"Recent results:\n"
    for result in results:
        results_text = results_text + format_result(result) + "\n"

    fixtures = arsenal_api.fixtures()[:3]
    fixtures_text = f"Upcoming fixtures:\n"
    for fixture in fixtures:
        fixtures_text = fixtures_text + format_fixture(fixture) + "\n"

    text = f"*:arsenal: Info*\n\n```" \
           f"{results_text}\n" \
           f"{fixtures_text}\n" \
           f"{get_short_table()}```"
    return text


def get_fixtures():
    fixtures = arsenal_api.fixtures()
    update = arsenal_api.meta_info()['matches_last_update']
    text = f"*:arsenal: Fixtures:* \n_Updated: {update}_\n```"
    for fixture in fixtures:
        text = text + format_fixture(fixture) + "\n"
    text = text + '```'
    return text


def format_fixture(fixture):
    date = datetime.datetime.strptime(fixture['date_time'], '%a, %d %b %Y %H:%M:%S %Z')
    time_diff = arsenal_api.meta_info()['time_diff']
    date += datetime.timedelta(hours=time_diff)
    day = datetime.datetime.strftime(date, '%b %d')
    time = datetime.datetime.strftime(date, '%H:%M')
    home = fixture['home']
    away = fixture['away']
    competition = COMPETITION_DICT[fixture['competition']]

    r = f"{day} @ {time} | {home} vs {away} | {competition}"
    r = r.replace("Arsenal", "ARSENAL")

    return r


def get_results():
    results = arsenal_api.results()
    update = arsenal_api.meta_info()['matches_last_update']
    text = f"*:arsenal: Results:* \n_Updated: {update}_\n```"
    for result in results:
        text = text + format_result(result) + "\n"
    text = text + '```'
    return text


def format_result(result):
    date = datetime.datetime.strptime(result['date_time'], '%a, %d %b %Y %H:%M:%S %Z')
    date = datetime.datetime.strftime(date, '%b %d')
    home = result['home']
    home_score = result['home_goals']
    away = result['away']
    away_score = result['away_goals']
    competition = COMPETITION_DICT[result['competition']]
    status = result['status']

    if status == 'PST':
        r = f"{date} | {home} -PPD- {away} | {competition}"
    else:
        r = f"{date} | {home} {home_score} - {away_score} {away} | {competition}"

    r = r.replace('Arsenal', 'ARSENAL')

    return r


def get_table():
    table = arsenal_api.table()
    update = arsenal_api.meta_info()['table_last_update']
    text = f"*Premier League Table*\n_Updated: {update}_\n```                       " \
           "  | Pl |  W |  D |  L |  GF |  GA |  GD | Pts\n"
    for team in table:
        if team['team'] == 'Arsenal':
            text = text + "->" + format_table_entry(team)
        else:
            text = text + "  " + format_table_entry(team)
        if team['rank'] == 4 or team['rank'] == 17:
            text = text + f"  {'-'*66}\n"
    text = text + "```"

    return text


def get_short_table():
    teams = arsenal_api.table()

    for team in teams:
        if team['team'] == 'Arsenal':
            arsenal_rank = team['rank']

    starting_index = 0
    ending_index = arsenal_rank + 3

    if arsenal_rank > 4:
        starting_index = arsenal_rank - 4

    table = teams[starting_index:ending_index]

    text = "PL Table:\n                       " \
           "| Pl |  W |  D |  L |  GF |  GA |  GD | Pts\n"
    for team in table:
        text = text + format_table_entry(team)

    return text


def format_table_entry(entry):
    rank = str(entry['rank']).rjust(2)
    team = entry['team'].ljust(17)
    played = str(entry['played']).rjust(2)
    wins = str(entry['wins']).rjust(2)
    draws = str(entry['draws']).rjust(2)
    losses = str(entry['losses']).rjust(2)
    goals_for = str(entry['goals_for']).rjust(3)
    goals_against = str(entry['goals_against']).rjust(3)
    goal_difference = str(entry['goal_difference']).rjust(3)
    points = str(entry['points']).rjust(3)

    e = f"{rank} | {team} | {played} | {wins} | {draws} | {losses} | {goals_for} | {goals_against} | " \
        f"{goal_difference} | {points}\n"

    return e


def get_squad():
    squad = arsenal_api.squad()
    squad = [p for p in squad if 'number' in p]
    longest = arsenal_api.meta_info()['longest_name'] + 1

    text = f"*:arsenal: Squad*:\n```" \
           f"{' ' * (longest + 7)} Overall {' ' * 17} League\n" \
           f" # | {'Name'.ljust(longest)} | Apps | Gls | Ast | Rate | Apps | Gls | Ast | Rate\n"

    for player in squad:
        text += f"{str(player['number']).rjust(2)} | {player['name'].ljust(longest)} | " \
                f"{str(player['apps']).center(4)} | {str(player['goals']).center(3)} | {str(player['assists']).center(3)} | " \
                f"{str('%.2f' % player['rating']).center(4)} | {str(player['pl_apps']).center(4)} | " \
                f"{str(player['pl_goals']).center(3)} | {str(player['pl_assists']).center(3)} | " \
                f"{str('%.2f' % player['pl_rating']).center(4)}\n"

    text += '```'

    return text


if __name__ == '__main__':
    req = get_info()
    print(req)

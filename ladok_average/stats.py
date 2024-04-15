from sty import fg, bg

from ladok_average.termtable import TerminalTable

def __grade_from_course(course):
    grade = course['grade']
    match grade:
        case 'G':
            return 3
        case 'U':
            return 0
        case _ if grade.isdigit():
            return int(grade)
        case _:
            raise ValueError

def __scope_from_course(course):
    scope = course['scope']
    scope = scope[:len(scope) - 2] # remove "hp"

    return float(scope)

def __weight_from_course(course):
    return __scope_from_course(course) * __grade_from_course(course)

def __calculate_average(weight, scope):
    return round(weight / scope, 5)

def __get_average(courses, total_scope):
    total_weight = sum(list(map(lambda course : __weight_from_course(course), courses)))
    average = __calculate_average(total_weight, total_scope)

    return [
        {'statistic': 'Average grade',
        'value': str(average)}
    ]

def __year_from_course(course):
    return int(course['date'].split('-')[0])

def __get_averages_by_year(courses):
    year_scopes = {}
    year_weights = {}

    for course in courses:
        year = __year_from_course(course)
        year_scopes[year] = year_scopes.get(year, 0) + __scope_from_course(course)
        year_weights[year] = year_weights.get(year, 0) + __weight_from_course(course)

    averages = []
    for year in sorted(year_scopes.keys()):
        average = __calculate_average(year_weights[year], year_scopes[year])
        averages += [{'statistic': f'Average grade {year}',
                     'value': str(average)}]

    return averages

def get_stats(courses, verbose, ignore_average, by_year):
    stats = []
    total_scope = sum(list(map(lambda course : __scope_from_course(course), courses)))

    if not ignore_average and not by_year:
        stats += __get_average(courses, total_scope)
    
    if not ignore_average and by_year:
        stats += __get_averages_by_year(courses)

    if verbose:
        stats += [{
            'statistic': 'Number of courses',
            'value': str(len(courses)),
        }, {
            'statistic': 'Total scope',
            'value': str(total_scope) + 'hp',
        }]

    return stats

def create_stats_table():
    return TerminalTable(
        name='stats',
        header=['Statistic', 'Value'],
        alignments=['left', 'center'],
        sort_by=None,
        header_colors=(bg.blue, fg.white),
        even_colors=(bg.da_grey, fg.white),
        odd_colors=(bg.grey, fg.black),
    )

import json
import requests
import datetime
import MySQLdb
from argparse import ArgumentParser
from emails import send_email

import seta


def get_raw_data(start_date, end_date):
    if not end_date:
        end_date = datetime.datetime.now()

    if not start_date:
        start_date = end_date - datetime.timedelta(days=180)

    url = "http://alertmanager.allizom.org/data/seta/?startDate=%s&endDate=%s" % (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

    response = requests.get(url, headers={'accept-encoding': 'json'}, verify=True)
    data = json.loads(response.content)
    return data['failures']


def communicate(failures, to_remove, total_detected, testmode, date):

    active_jobs = seta.get_distinct_tuples()
    format_in_table(active_jobs, to_remove)
    percent_detected = ((len(total_detected) / (len(failures)*1.0)) * 100)
    print "We will detect %.2f%% (%s) of the %s failures" % (percent_detected, len(total_detected), len(failures))

    if testmode:
        return

    insert_in_database(to_remove, date)

    if date is None:
        date = datetime.date.today()
    change = print_diff("%s" % (date - datetime.timedelta(days=1)).strftime('%Y-%m-%d'), '%s' % date.strftime('%Y-%m-%d'))
    try:
        total_changes = len(change)
    except TypeError:
        total_changes = 0

    if total_changes == 0:
        send_email(len(failures), len(to_remove), date, "no changes from previous day", admin=True, results=False)
    else:
        send_email(len(failures), len(to_remove), date, str(total_changes) + " changes from previous day", change, admin=True, results=True)


def format_in_table(active_jobs, master):
    results = {}
    sum_removed = 0
    sum_remaining = 0

    tbplnames = {'mochitest-1': {'group': 'M', 'code': '1'},
                 'mochitest-2': {'group': 'M', 'code': '2'},
                 'mochitest-3': {'group': 'M', 'code': '3'},
                 'mochitest-4': {'group': 'M', 'code': '4'},
                 'mochitest-5': {'group': 'M', 'code': '5'},
                 'mochitest-6': {'group': 'M', 'code': '6'},
                 'mochitest-7': {'group': 'M', 'code': '7'},
                 'mochitest-8': {'group': 'M', 'code': '8'},
                 'mochitest-9': {'group': 'M', 'code': '9'},
                 'mochitest-10': {'group': 'M', 'code': '10'},
                 'mochitest-11': {'group': 'M', 'code': '11'},
                 'mochitest-12': {'group': 'M', 'code': '12'},
                 'mochitest-13': {'group': 'M', 'code': '13'},
                 'mochitest-14': {'group': 'M', 'code': '14'},
                 'mochitest-15': {'group': 'M', 'code': '15'},
                 'mochitest-16': {'group': 'M', 'code': '16'},
                 'mochitest-other': {'group': 'M', 'code': 'Oth'},
                 'mochitest-browser-chrome-1': {'group': 'M', 'code': 'bc1'},
                 'mochitest-browser-chrome-2': {'group': 'M', 'code': 'bc2'},
                 'mochitest-browser-chrome-3': {'group': 'M', 'code': 'bc3'},
                 'mochitest-devtools-chrome-1': {'group': 'M', 'code': 'dt1'},
                 'mochitest-devtools-chrome-2': {'group': 'M', 'code': 'dt2'},
                 'mochitest-devtools-chrome-3': {'group': 'M', 'code': 'dt3'},
                 'mochitest-devtools-chrome-4': {'group': 'M', 'code': 'dt4'},
                 'mochitest-devtools-chrome-5': {'group': 'M', 'code': 'dt5'},
                 'mochitest-devtools-chrome-6': {'group': 'M', 'code': 'dt6'},
                 'mochitest-devtools-chrome-7': {'group': 'M', 'code': 'dt7'},
                 'mochitest-devtools-chrome-8': {'group': 'M', 'code': 'dt8'},
                 'mochitest-devtools-chrome': {'group': 'M', 'code': 'dt'},
                 'mochitest-gl': {'group': 'M', 'code': 'gl'},
                 'mochitest-gl-1': {'group': 'M', 'code': 'gl1'},
                 'mochitest-gl-2': {'group': 'M', 'code': 'gl2'},
                 'mochitest-gl-3': {'group': 'M', 'code': 'gl3'},
                 'mochitest-gl-4': {'group': 'M', 'code': 'gl4'},
                 'mochitest-gl-5': {'group': 'M', 'code': 'gl5'},
                 'mochitest-e10s-1': {'group': 'M-e10s', 'code': '1'},
                 'mochitest-e10s-2': {'group': 'M-e10s', 'code': '2'},
                 'mochitest-e10s-3': {'group': 'M-e10s', 'code': '3'},
                 'mochitest-e10s-4': {'group': 'M-e10s', 'code': '4'},
                 'mochitest-e10s-5': {'group': 'M-e10s', 'code': '5'},
                 'mochitest-e10s-browser-chrome-1': {'group': 'M-e10s', 'code': 'bc1'},
                 'mochitest-e10s-browser-chrome-2': {'group': 'M-e10s', 'code': 'bc2'},
                 'mochitest-e10s-browser-chrome-3': {'group': 'M-e10s', 'code': 'bc3'},
                 'mochitest-e10s-devtools-chrome': {'group': 'M-e10s', 'code': 'dt'},
                 'mochitest-push': {'group': 'M', 'code': 'p'},
                 'xpcshell': {'group': '', 'code': 'X'},
                 'xpcshell-1': {'group': '', 'code': 'X1'},
                 'xpcshell-2': {'group': '', 'code': 'X2'},
                 'xpcshell-3': {'group': '', 'code': 'X3'},
                 'xpcshell-4': {'group': '', 'code': 'X4'},
                 'xpcshell-5': {'group': '', 'code': 'X5'},
                 'crashtest': {'group': 'R', 'code': 'C'},
                 'crashtest-1': {'group': 'R', 'code': 'C1'},
                 'crashtest-2': {'group': 'R', 'code': 'C2'},
                 'crashtest-3': {'group': 'R', 'code': 'C3'},
                 'crashtest-4': {'group': 'R', 'code': 'C4'},
                 'jsreftest': {'group': 'R', 'code': 'J'},
                 'jsreftest-1': {'group': 'R', 'code': 'J1'},
                 'jsreftest-2': {'group': 'R', 'code': 'J2'},
                 'jsreftest-3': {'group': 'R', 'code': 'J3'},
                 'jsreftest-4': {'group': 'R', 'code': 'J4'},
                 'jsreftest-5': {'group': 'R', 'code': 'J5'},
                 'jsreftest-6': {'group': 'R', 'code': 'J6'},
                 'jsreftest-7': {'group': 'R', 'code': 'J7'},
                 'jsreftest-8': {'group': 'R', 'code': 'J8'},
                 'plain-reftest-1': {'group': 'R', 'code': 'R1'},
                 'plain-reftest-2': {'group': 'R', 'code': 'R2'},
                 'plain-reftest-3': {'group': 'R', 'code': 'R3'},
                 'plain-reftest-4': {'group': 'R', 'code': 'R4'},
                 'plain-reftest-5': {'group': 'R', 'code': 'R5'},
                 'plain-reftest-6': {'group': 'R', 'code': 'R6'},
                 'plain-reftest-7': {'group': 'R', 'code': 'R7'},
                 'plain-reftest-8': {'group': 'R', 'code': 'R8'},
                 'plain-reftest-9': {'group': 'R', 'code': 'R9'},
                 'plain-reftest-10': {'group': 'R', 'code': 'R10'},
                 'plain-reftest-11': {'group': 'R', 'code': 'R11'},
                 'plain-reftest-12': {'group': 'R', 'code': 'R12'},
                 'plain-reftest-13': {'group': 'R', 'code': 'R13'},
                 'plain-reftest-14': {'group': 'R', 'code': 'R14'},
                 'plain-reftest-15': {'group': 'R', 'code': 'R15'},
                 'plain-reftest-16': {'group': 'R', 'code': 'R16'},
                 'plain-reftest-17': {'group': 'R', 'code': 'R17'},
                 'plain-reftest-18': {'group': 'R', 'code': 'R18'},
                 'plain-reftest-19': {'group': 'R', 'code': 'R19'},
                 'plain-reftest-20': {'group': 'R', 'code': 'R20'},
                 'reftest-1': {'group': 'R', 'code': 'R1'},
                 'reftest-2': {'group': 'R', 'code': 'R2'},
                 'reftest-3': {'group': 'R', 'code': 'R3'},
                 'reftest-4': {'group': 'R', 'code': 'R4'},
                 'reftest-e10s': {'group': 'R-e10s', 'code': 'R'},
                 'reftest-e10s-1': {'group': 'R-e10s', 'code': 'R1'},
                 'reftest-e10s-2': {'group': 'R-e10s', 'code': 'R2'},
                 'crashtest-e10s': {'group': 'R-e10s', 'code': 'C'},
                 'jittest': {'group': '', 'code': 'Jit'},
                 'jittest-2': {'group': '', 'code': 'Jit2'},
                 'jittest-1': {'group': '', 'code': 'Jit1'},
                 'marionette': {'group': '', 'code': 'Mn'},
                 'marionette-e10s': {'group': '', 'code': 'Mn-e10s'},
                 'cppunit': {'group': '', 'code': 'Cpp'},
                 'reftest-no-accel': {'group': '', 'code': 'Cpp'},
                 'web-platform-tests-1': {'group': 'W', 'code': '1'},
                 'web-platform-tests-2': {'group': 'W', 'code': '2'},
                 'web-platform-tests-3': {'group': 'W', 'code': '3'},
                 'web-platform-tests-4': {'group': 'W', 'code': '4'},
                 'web-platform-tests-reftests': {'group': 'W', 'code': 'R'},
                 'mochitest-jetpack': {'group': '', 'code': 'JP'},
                 'luciddream': {'group': '', 'code': 'Ld'},
                 'robocop-1': {'group': 'RC', 'code': '1'},
                 'robocop-2': {'group': 'RC', 'code': '2'},
                 'robocop-3': {'group': 'RC', 'code': '3'},
                 'robocop-4': {'group': 'RC', 'code': '4'},
                 'robocop-5': {'group': 'RC', 'code': '5'},
                 'robocop-6': {'group': 'RC', 'code': '6'},
                 'robocop-7': {'group': 'RC', 'code': '7'},
                 'robocop-8': {'group': 'RC', 'code': '8'},
                 'reftest': {'group': 'R', 'code': 'R'},
                 'androidx86-set-4': {'group': 'S', 'code': '4'}}

    for jobtype in active_jobs:
        key = "%s_%s" % (jobtype[0], jobtype[1])
        if key not in results:
            results[key] = []

        for item in master:
            if item[0] == jobtype[0] and item[1] == jobtype[1]:
                results[key].append(item[2])

    keys = results.keys()
    keys.sort()
    missing_jobs = []
    for key in keys:
        data = results[key]
        data.sort()
        output = ""
        for platform, buildtype, test in active_jobs:
            if "%s_%s" % (platform, buildtype) != key:
                continue

            output += '\t'
            if test in data or '' in data:
                try:
                    output += tbplnames[test]['code']
                except KeyError:
                    output += '**'
                    missing_jobs.append(test)

                sum_removed += 1
            else:
                output += "--"
                sum_remaining += 1

        print "%s%s" % (key, output)

    if missing_jobs:
        print "** new jobs which need a code: %s" % ','.join(missing_jobs)

    print "Total removed %s" % (sum_removed)
    print "Total remaining %s" % (sum_remaining)
    print "Total jobs %s" % (sum_removed + sum_remaining)


def insert_in_database(to_remove, date=None):
    if not date:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        date = date.strftime('%Y-%m-%d')

    run_query('delete from seta where date="%s"' % date)
    for jobtype in to_remove:
        query = 'insert into seta (date, jobtype) values ("%s", ' % date
        query += '"%s")' % jobtype
        run_query(query)


def run_query(query):
    database = MySQLdb.connect(host="localhost",
                         user="root",
                         passwd="root",
                         db="ouija")

    cur = database.cursor()
    cur.execute(query)

    results = []
    # each row is in ('val',) format, we want 'val'
    for rows in cur.fetchall():
        results.append(rows[0])

    cur.close()
    return results


def check_data(query_date):
    ret_val = []
    data = run_query('select jobtype from seta where date="%s"' % query_date)
    if not data:
        print "The database does not have data for the given %s date." % query_date
        for date in range(-3, 4):
            current_date = query_date + datetime.timedelta(date)
            jobtype = run_query('select jobtype from seta where date="%s"' % current_date)
            if jobtype:
                print "The data is available for date=%s" % current_date
        return ret_val

    for job in data:
        parts = job.split("'")
        ret_val.append("%s" % [str(parts[1]), str(parts[3]), str(parts[5])])

    return ret_val


def print_diff(start_date, end_date):
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    start_tuple = check_data(start_date)
    end_tuple = check_data(end_date)

    start_tuple.sort()
    end_tuple.sort()

    if start_tuple is None or end_tuple is None:
        print "NO DATA: %s, %s" % (start_date, end_date)
        return []
    else:
        deletion = list(set(start_tuple) - set(end_tuple))
        deletion.sort()
        if not deletion:
            deletion = ''
        print "%s: These jobs have changed from the previous day: %s" % (end_date.strftime("%Y-%m-%d"), deletion)
        return deletion


def parse_args(argv=None):
    parser = ArgumentParser()
    parser.add_argument("-s", "--start_date",
                        metavar="YYYY-MM-DD",
                        dest="start_date",
                        help="starting date for comparison."
                        )

    parser.add_argument("-e", "--end_date",
                        metavar="YYYY-MM-DD",
                        dest="end_date",
                        help="ending date for comparison."
                        )

    parser.add_argument("--testmode",
                        action="store_true",
                        dest="testmode",
                        help="This mode is for testing without interaction with \
                              database and emails."
                        )

    parser.add_argument("--diff",
                        action="store_true",
                        dest="diff",
                        help="This mode is for printing a diff between two dates. \
                              requires --start_date and --end_date."
                        )

    parser.add_argument("--ignore-failure",
                        type=int,
                        dest="ignore_failure",
                        help="With this option one can ignore root causes of revisions. \
                              Specify the number of *extra* passes to be done."
                        )

    parser.add_argument("--method",
                        metavar="[failures|weighted]",
                        dest="method",
                        default="weighted",
                        help="This is for deciding the algorithm to run. \
                              Two algorithms to run currently: [failures|weighted]."
                        )

    options = parser.parse_args(argv)
    return options


def analyze_failures(start_date, end_date, testmode, ignore_failure, method):
    failures = get_raw_data(start_date, end_date)
    print "date: %s, failures: %s" % (end_date, len(failures))
    target = 100 # 100% detection

    if method == "failures":
        to_remove, total_detected = seta.failures_by_jobtype(failures, target, ignore_failure)
    else:
        to_remove, total_detected = seta.weighted_by_jobtype(failures, target, ignore_failure)
    communicate(failures, to_remove, total_detected, testmode, end_date)

if __name__ == "__main__":
    options = parse_args()

    if options.diff:
        if options.start_date and options.end_date:
            print_diff(options.start_date, options.end_date)
        else:
            print "when using --diff please provide a --start_date and an --end_date"
    else:
        if options.end_date:
            end_date = datetime.datetime.strptime(options.end_date, "%Y-%m-%d")
        else:
            end_date = datetime.datetime.now()

        if options.start_date:
            start_date = datetime.datetime.strptime(options.start_date, "%Y-%m-%d")
        else:
            start_date = end_date - datetime.timedelta(days=180)

        analyze_failures(start_date, end_date, options.testmode, options.ignore_failure,
                        options.method)

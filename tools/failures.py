import json
import logging
import os
import requests
import datetime
from argparse import ArgumentParser
from emails import send_email
from redo import retry
from database.models import Seta, JobPriorities
from database.config import session, engine
from update_runnablejobs import update_runnableapi, get_rootdir
from sqlalchemy import update, and_

import seta

logger = logging.getLogger(__name__)
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = get_rootdir()
SETA_WINDOW = 90
TREEHERDER_HOST = "https://treeherder.mozilla.org/api/project/{0}/" \
                  "runnable_jobs/?decisionTaskID={1}&format=json"
headers = {
    'Accept': 'application/json',
    'User-Agent': 'ouija',
}
HOST = "http://seta-dev.herokuapp.com/"


def get_raw_data(start_date, end_date):
    if not end_date:
        end_date = datetime.datetime.now()

    if not start_date:
        start_date = end_date - datetime.timedelta(days=SETA_WINDOW)

    url = HOST + "data/seta/?startDate=%s&endDate=%s" % \
                 (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    try:
        response = retry(requests.get, args=(url, ),
                         kwargs={'headers': headers, 'verify': True})
        data = json.loads(response.content)
    except Exception as error:
        # we will return an empty 'failures' list if got exception here
        logger.debug("the request to %s failed, due to %s" % (url, error))
        data = {'failures': []}
    return data['failures']


def communicate(failures, to_insert, total_detected, testmode, date):

    active_jobs = seta.get_distinct_tuples()
    percent_detected = ((len(total_detected) / (len(failures) * 1.0)) * 100)
    print "We will detect %.2f%% (%s) of the %s failures" % \
          (percent_detected, len(total_detected), len(failures))

    if testmode:
        return
    prepare_the_database()
    insert_in_database(to_insert, date)
    priority = 1
    timeout = 0
    updated_jobs = update_jobpriorities(to_insert, priority, timeout)
    print "updated %s (%s) jobs" % (len(updated_jobs), len(to_insert))

    if date is None:
        date = datetime.date.today()
    change = print_diff("%s" % (date - datetime.timedelta(days=1)).strftime('%Y-%m-%d'), '%s' %
                        date.strftime('%Y-%m-%d'))
    try:
        total_changes = len(change)
    except TypeError:
        total_changes = 0

# TODO: we need to setup username/password to work in Heroku, probably via env variables
#    if total_changes == 0:
#        send_email(len(failures), len(to_insert), date, "no changes from previous day",
#                   admin=True, results=False)
#    else:
#        send_email(len(failures), len(to_insert), date, str(total_changes) +
#                   " changes from previous day", change, admin=True, results=True)


def insert_in_database(to_insert, date=None):
    if not date:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        date = date.strftime('%Y-%m-%d')

    session.query(Seta).filter(Seta.date == date).delete(synchronize_session='fetch')
    session.commit()
    for jobtype in to_insert:
        job = Seta(str(jobtype), date)
        session.add(job)
        session.commit()
    session.close()


def reset_preseed():
    data = session.query(JobPriorities.expires, JobPriorities.id)\
                  .filter(JobPriorities.expires != None).all()

    now = datetime.datetime.now()
    for item in data:
        try:
            dv = datetime.datetime.strptime(item[0], "%Y-%M-%d")
        except ValueError:
            # TODO: consider updating column to have expires=None?
            continue

        # reset expire field if date is today or in the past
        if dv.date() <= now.date():
            conn = engine.connect()
            statement = update(JobPriorities)\
                          .where(JobPriorities.id == item[1])\
                          .values(expires=None)
            conn.execute(statement)


def update_jobpriorities(to_insert, _priority, _timeout):
    # to_insert is currently high priority, pri=1 jobs, all else are pri=5 jobs

    changed_jobs = []
    for item in to_insert:
        # NOTE: we ignore JobPriorities with expires as they take precendence
        data = session.query(JobPriorities.id, JobPriorities.priority)\
                      .filter(and_(JobPriorities.testtype == item[2],
                                   JobPriorities.buildtype == item[1],
                                   JobPriorities.platform == item[0],
                                   JobPriorities.expires != None)).all()
        if len(data) != 1:
            # TODO: if 0 items, do we add the job?  if >1 do we alert and cleanup?
            continue

        if data[0][1] != _priority:
            changed_jobs.append(item)

            conn = engine.connect()
            statement = update(JobPriorities)\
                          .where(and_(JobPriorities.testtype == item[2],
                                      JobPriorities.buildtype == item[1],
                                      JobPriorities.platform == item[0]))\
                          .values(priority=_priority,
                                  timeout=_timeout)
            conn.execute(statement)

    return changed_jobs


def prepare_the_database():
    # wipe up the job data older than 90 days
    date = (datetime.datetime.now() - datetime.timedelta(days=SETA_WINDOW)).strftime('%Y-%m-%d')
    session.query(Seta).filter(Seta.date <= date)


def check_data(query_date):
    ret_val = []
    data = session.query(Seta.jobtype).filter(Seta.date == query_date).all()
    if not data:
        print "The database does not have data for the given %s date." % query_date
        for date in range(-3, 4):
            current_date = query_date + datetime.timedelta(date)
            jobtype = session.query(Seta).filter(Seta.date == current_date)
            if jobtype:
                print "The data is available for date=%s" % current_date
        return ret_val

    for job in data:
        parts = job[0].split("'")
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
        print "%s: These jobs have changed from the previous day: %s" % \
              (end_date.strftime("%Y-%m-%d"), deletion)
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
    target = 100  # 100% detection

    to_insert, total_detected = seta.weighted_by_jobtype(failures, target, ignore_failure)
    communicate(failures, to_insert, total_detected, testmode, end_date)


if __name__ == "__main__":
    options = parse_args()
    update_runnableapi()
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
            start_date = end_date - datetime.timedelta(days=SETA_WINDOW)

        analyze_failures(start_date, end_date, options.testmode, options.ignore_failure,
                         options.method)

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
             'mochitest-chrome': {'group': 'M', 'code': 'c'},
             'mochitest-browser-chrome-1': {'group': 'M', 'code': 'bc1'},
             'mochitest-browser-chrome-2': {'group': 'M', 'code': 'bc2'},
             'mochitest-browser-chrome-3': {'group': 'M', 'code': 'bc3'},
             'mochitest-browser-chrome-7': {'group': 'M', 'code': 'bc7'},
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
             'mochitest-browser-chrome-e10s-1': {'group': 'M-e10s', 'code': 'bc1'},
             'mochitest-browser-chrome-e10s-2': {'group': 'M-e10s', 'code': 'bc2'},
             'mochitest-browser-chrome-e10s-3': {'group': 'M-e10s', 'code': 'bc3'},
             'mochitest-e10s-devtools-chrome': {'group': 'M-e10s', 'code': 'dt'},
             'mochitest-e10s-devtools-chrome-1': {'group': 'M-e10s', 'code': 'dt1'},
             'mochitest-e10s-devtools-chrome-2': {'group': 'M-e10s', 'code': 'dt2'},
             'mochitest-e10s-devtools-chrome-3': {'group': 'M-e10s', 'code': 'dt3'},
             'mochitest-e10s-devtools-chrome-4': {'group': 'M-e10s', 'code': 'dt4'},
             'mochitest-devtools-chrome-e10s-1': {'group': 'M-e10s', 'code': 'dt1'},
             'mochitest-devtools-chrome-e10s-2': {'group': 'M-e10s', 'code': 'dt2'},
             'mochitest-devtools-chrome-e10s-3': {'group': 'M-e10s', 'code': 'dt3'},
             'mochitest-devtools-chrome-e10s-4': {'group': 'M-e10s', 'code': 'dt4'},
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
             'jsreftest-9': {'group': 'R', 'code': 'J9'},
             'jsreftest-10': {'group': 'R', 'code': 'J10'},
             'jsreftest-11': {'group': 'R', 'code': 'J11'},
             'jsreftest-12': {'group': 'R', 'code': 'J12'},
             'jsreftest-13': {'group': 'R', 'code': 'J13'},
             'jsreftest-14': {'group': 'R', 'code': 'J14'},
             'jsreftest-15': {'group': 'R', 'code': 'J15'},
             'jsreftest-16': {'group': 'R', 'code': 'J16'},
             'jsreftest-17': {'group': 'R', 'code': 'J17'},
             'jsreftest-18': {'group': 'R', 'code': 'J18'},
             'jsreftest-19': {'group': 'R', 'code': 'J19'},
             'jsreftest-20': {'group': 'R', 'code': 'J20'},
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
             'plain-reftest-21': {'group': 'R', 'code': 'R21'},
             'plain-reftest-22': {'group': 'R', 'code': 'R22'},
             'plain-reftest-23': {'group': 'R', 'code': 'R23'},
             'plain-reftest-24': {'group': 'R', 'code': 'R24'},
             'plain-reftest-25': {'group': 'R', 'code': 'R25'},
             'plain-reftest-26': {'group': 'R', 'code': 'R26'},
             'plain-reftest-27': {'group': 'R', 'code': 'R27'},
             'plain-reftest-28': {'group': 'R', 'code': 'R28'},
             'plain-reftest-29': {'group': 'R', 'code': 'R29'},
             'plain-reftest-30': {'group': 'R', 'code': 'R30'},
             'plain-reftest-31': {'group': 'R', 'code': 'R31'},
             'plain-reftest-32': {'group': 'R', 'code': 'R32'},
             'plain-reftest-33': {'group': 'R', 'code': 'R33'},
             'plain-reftest-34': {'group': 'R', 'code': 'R34'},
             'plain-reftest-35': {'group': 'R', 'code': 'R35'},
             'plain-reftest-36': {'group': 'R', 'code': 'R36'},
             'plain-reftest-37': {'group': 'R', 'code': 'R37'},
             'plain-reftest-38': {'group': 'R', 'code': 'R38'},
             'plain-reftest-39': {'group': 'R', 'code': 'R39'},
             'plain-reftest-40': {'group': 'R', 'code': 'R40'},
             'plain-reftest-41': {'group': 'R', 'code': 'R41'},
             'plain-reftest-42': {'group': 'R', 'code': 'R42'},
             'plain-reftest-43': {'group': 'R', 'code': 'R43'},
             'plain-reftest-44': {'group': 'R', 'code': 'R44'},
             'plain-reftest-45': {'group': 'R', 'code': 'R45'},
             'plain-reftest-46': {'group': 'R', 'code': 'R46'},
             'plain-reftest-47': {'group': 'R', 'code': 'R47'},
             'plain-reftest-48': {'group': 'R', 'code': 'R48'},
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
             'cpp_gtest': {'group': '', 'code': 'Cpp-G'},
             'reftest-no-accel': {'group': '', 'code': 'Ru'},
             'reftest-no-accel-1': {'group': '', 'code': 'Ru1'},
             'reftest-no-accel-2': {'group': '', 'code': 'Ru2'},
             'web-platform-tests-1': {'group': 'W', 'code': '1'},
             'web-platform-tests-2': {'group': 'W', 'code': '2'},
             'web-platform-tests-3': {'group': 'W', 'code': '3'},
             'web-platform-tests-4': {'group': 'W', 'code': '4'},
             'web-platform-tests-5': {'group': 'W', 'code': '5'},
             'web-platform-tests-6': {'group': 'W', 'code': '6'},
             'web-platform-tests-7': {'group': 'W', 'code': '7'},
             'web-platform-tests-8': {'group': 'W', 'code': '8'},
             'web-platform-tests-reftests': {'group': 'W', 'code': 'R'},
             'web-platform-tests-e10s-1': {'group': 'W-e10s', 'code': '1'},
             'web-platform-tests-e10s-2': {'group': 'W-e10s', 'code': '2'},
             'web-platform-tests-e10s-3': {'group': 'W-e10s', 'code': '3'},
             'web-platform-tests-e10s-4': {'group': 'W-e10s', 'code': '4'},
             'web-platform-tests-e10s-5': {'group': 'W-e10s', 'code': '5'},
             'web-platform-tests-e10s-6': {'group': 'W-e10s', 'code': '6'},
             'web-platform-tests-e10s-7': {'group': 'W-e10s', 'code': '7'},
             'web-platform-tests-e10s-8': {'group': 'W-e10s', 'code': '8'},
             'web-platform-tests-reftests-e10s': {'group': 'W-e10s', 'code': 'R'},
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
             'tp5o': {'group': 'T', 'code': 'tp'},
             'tp5o-e10s': {'group': 'T-e10s', 'code': 'tp'},
             'tp5o-osx-e10s': {'group': 'T-e10s', 'code': 'tp'},
             'other': {'group': 'T', 'code': 'o'},
             'other-e10s': {'group': 'T-e10s', 'code': 'o'},
             'other_nol64': {'group': 'T', 'code': 'o'},
             'other-e10s_nol64': {'group': 'T-e10s', 'code': 'o'},
             'other_l64': {'group': 'T', 'code': 'o'},
             'other-e10s_l64': {'group': 'T-e10s', 'code': 'o'},
             'svgr': {'group': 'T', 'code': 's'},
             'svgr-e10s': {'group': 'T-e10s', 'code': 's'},
             'svgr-osx-e10s': {'group': 'T-e10s', 'code': 's'},
             'g1': {'group': 'T', 'code': 'g1'},
             'g1-e10s': {'group': 'T-e10s', 'code': 'g1'},
             'g1-osx-e10s': {'group': 'T-e10s', 'code': 'g1'},
             'g2': {'group': 'T', 'code': 'g2'},
             'g2-e10s': {'group': 'T-e10s', 'code': 'g2'},
             'g2-osx-e10s': {'group': 'T-e10s', 'code': 'g2'},
             'dromaeojs': {'group': 'T', 'code': 'd'},
             'dromaeojs-e10s': {'group': 'T-e10s', 'code': 'd'},
             'chromez': {'group': 'T', 'code': 'c'},
             'chromez-e10s': {'group': 'T-e10s', 'code': 'c'},
             'chromez-osx-e10s': {'group': 'T-e10s', 'code': 'c'},
             'xperf': {'group': 'T', 'code': 'x'},
             'xperf-e10s': {'group': 'T-e10s', 'code': 'x'},
             'androidx86-set-4': {'group': 'S', 'code': '4'}}


def getGroup(name):
    try:
        group = name.split('-')[0]
    except:
        group = ''
    return group


def getGroupCode(name):
    try:
        # strip useless blank in test name.
        # e.g change ' mochitest-devtools-chrome-e10s-2' to
        # 'mochitest-devtools-chrome-e10s-2'
        code = tbplnames[name.strip()]['group']
    except:
        code = ''
    return code


def getCode(name):
    try:
        code = tbplnames[name.strip()]['code']
    except:
        code = ''
    return code

import sys
import configparser


def run_config(cfg, file):
    """
    reads a  configuration file (config.ini) in standard format.
    [header]
    config_item  = value

    quotations are not required.
    """
    config = configparser.ConfigParser()

    die = 0

    if cfg is None:
        print("INFO: reading configuration from config.ini")

        if file is None:
            file = 'config.ini'  # hackish fallback
        try:
            config.read_file(open(file))
        except FileNotFoundError:
            print('ERROR: config.ini not found.')
            sys.exit(1)

        os = None
        camera = None
        green_upper = None
        green_lower = None
        nt_update_frequency = None
        debug = None
        search = None
        address = None
    else:
        config = cfg

    try:  # unless cast below, all config options are strings
        os = config['os']['operating_system']
        camera = config['camera']['camera_device']
        green_upper = config['mask']['green_upper']
        green_upper = list(map(int, green_upper.split(',')))
        green_lower = config['mask']['green_lower']
        green_lower = list(map(int, green_lower.split(',')))
        nt_update_frequency = int(config['framerate']['nt_update_frequency'])
        debug = config['debug']['debug']
        search = config['search']['search']
        address = config['robot']['address']
    except configparser.NoSectionError:
        print("WARNING: config.ini does not contain correct [sections] . see config.correct ")
    except configparser.NoOptionError:
        print("WARNING: config.ini does not contain correct options. see config.correct ")


    if not os:
        print("INFO: Host OS configuration not present, using \'linux\'. ")
        os = "linux"
    if not camera:
        print("ERROR: camera configuration not present.")
        die = 1
    sacrificial = None
    try:
        sacrificial = green_upper[2]
        sacrificial = green_lower[2]
    except IndexError:
        print("ERROR: calibration sets must have three fields.")
        die = 1
    except TypeError:
        print("ERROR: calibration configuration must only contain integers.")
        die = 1
    if not sacrificial:
        die = 1
    if not nt_update_frequency:
        print("INFO: framerate not specified, using default of 10.")
        nt_update_frequency = 10
    if not debug:
        print("INFO: \'debug\' not specified, not debugging.")
    if not search:
        print("INFO: \'search\' not specified, searching for targets.")
    if not address:
        print("WARNING: Robot IP address not specified. Using default 10.5.1.2.")
        address = '10.5.1.2'

    if die > 0:
        print("ERROR: Unable to load vision configuration. Exiting.")
        sys.exit(1)

    if debug == '1':
        debug = True
    else:
        debug = False
    if search == '0':
        search = False
    else:
        search = True

    if debug:
        print('INFO: Debug set.')

    green = {'green_upper': green_upper, 'green_lower': green_lower}
    calibration = {'green': green, 'debug': debug, 'search': search}

    return os, camera, calibration, nt_update_frequency, address


def write_cal(cal):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set('mask', 'green_upper', ','.join(cal['green']['green_upper']))  # convert lists into single strings
    config.set('mask', 'green_lower', ','.join(cal['green']['green_lower']))

    print('Validating configuration and writing to disk.')
    run_config(config, None)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    return True

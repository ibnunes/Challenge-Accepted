from tui.cli import crt

rFG  = crt.color.FAIL
wFG  = crt.color.WARNING
bold = crt.color.BOLD
END  = crt.color.ENDC

def banner(version):
    return                                                        \
        f"{rFG+bold} _____  _             _  _                            \n" \
        "/  __ \| |           | || |                           \n" \
        "| /  \/| |__    __ _ | || |  ___  _ __    __ _   ___  \n" \
        "| |    | '_ \  / _` || || | / _ \| '_ \  / _` | / _ \ \n" \
        "| \__/\| | | || (_| || || ||  __/| | | || (_| ||  __/ \n" \
        f" \____/|_| |_| \__,_||_||_| \___||_| |_| \__, | \___|{wFG} \n" \
        f"  ___                            _        {rFG}__/ | {wFG}_     \n" \
        f" / _ \                          | |{rFG}      |___/{wFG} | |    \n" \
        "/ /_\ \  ___   ___   ___  _ __  | |_   ___   __| |    \n" \
        "|  _  | / __| / __| / _ \| '_ \ | __| / _ \ / _` |    \n" \
        "| | | || (__ | (__ |  __/| |_) || |_ |  __/| (_| |    \n" \
        "\_| |_/ \___| \___| \___|| .__/  \__| \___| \__,_|    \n" \
        "                         | |                          \n" \
        f"                         |_|          {END}     {version} \n"
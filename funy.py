import datetime, time
from blessed import Terminal

# Has nothing to do with the Rubicon project.

def calculate_time_and_ret_str(term: Terminal, number_colors: str, comment_color: str) -> str:
    ct = datetime.datetime.now()
    xt = datetime.datetime(ct.year, 12, 25, 0, 0, 0)
    tl = xt - ct

    tls = tl.seconds % 60
    tlsp = str(tls).zfill(2)

    tlm = tl.seconds // 60 % 60
    tlmp = str(tlm).zfill(2)

    tlh = tl.seconds // 3600
    tlhp = str(tlh).zfill(2)

    tld = tl.days
    tldp = str(tld).zfill(2)

    ctr = time.time()
    xtr = time.mktime((ct.year, 12, 25, 0, 0, 0, 0, 0, 0))
    tlr = xtr - ctr

    # let number_colors = nc and comment_color = cc and normal terminal coloring = nt
    # "Christmas Day is in {nc}{tld}{nt} days, {nc}{tlh}{nt} hours, and {nc}{tlm}{nt} minutes for the PST timezone.\nIn other words, {nc}{tldp}{nt}:{nc}{tlhp}{nt}:{nc}{tlmp}{nt}:{nc}{tlsp}{nt}.\n\n{cc}The exact time in standard UNIX format is {tlr}.{nt}"

    return f"{getattr(term, number_colors)}{tld}{getattr(term, 'normal')} days, {getattr(term, number_colors)}{tlh}{getattr(term, 'normal')} hours, and {getattr(term, number_colors)}{tlm}{getattr(term, 'normal')} minutes for the PST timezone.\nIn other words, {getattr(term, number_colors)}{tldp}:{tlhp}:{tlmp}:{tlsp}{getattr(term, 'normal')}.\n\n{getattr(term, comment_color)}The exact time in standard UNIX format is {tlr}.{getattr(term, 'normal')}"

term = Terminal()

with term.location(0, 0), term.hidden_cursor(), term.fullscreen():
    while True:
        print(calculate_time_and_ret_str(term, "gray51", "gray39"))
        time.sleep(0.001)
        print(term.clear())
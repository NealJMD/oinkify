import argparse
import re
import time

def get_timestamp(line):
    components = re.split("\s+", line)
    parsed = time.strptime(components[1], "%Y-%m-%dT%H:%M:%S")
    return time.strftime("%b %d %H:%M:%S", parsed)

def get_pid(line):
    results = re.findall('PID: ([0-9]+)', line)
    return results[0]

def get_hostname(line):
    components = re.split("\s+", line)
    return re.sub("[^a-zA-Z0-9]", "", components[8])

def reformat_line(line, timestamp, hostname, pid):
    components = re.split("\s+", line)
    content = " ".join(components[9:])
    return "%s %s rails[%s]: %s\n" % (timestamp, hostname, pid, content)

def select_relevant(lines):
    last = -1
    for ii, line in enumerate(lines):
        if "Oink Log Entry Complete" in line:
            last = ii
            break
    return lines[0:last+1]

def parse_lines(lines):
    if "Oink Action" not in lines[0]: return []
    if "PID" not in lines[1]: return []
    timestamp = get_timestamp(lines[0])
    hostname = get_hostname(lines[0])
    pid = get_pid(lines[1])
    relevant_lines = select_relevant(lines)
    return [reformat_line(line, timestamp, hostname, pid) for line in relevant_lines]

def stream_between(in_path, out_path):
    inf = open(in_path, 'rb')
    outf = open(out_path, 'wb')
    lines = []
    for line in inf:
        # sent the lines in groups of 10 to get whole log entries
        lines = lines[-9:] + [line]
        parsed = parse_lines(lines)
        for line in parsed:
            outf.write(line)
    inf.close()
    outf.close()

def main(args):
    stream_between(args.input, args.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Format Rails.logger logs for Oink.')
    parser.add_argument('input', metavar='input', type=str,
                       help='the txt file to read from')
    parser.add_argument("--output", metavar='output', type=str, default='output.txt',
                       help='the destination to write the data to')

    args = parser.parse_args()
    main(args)


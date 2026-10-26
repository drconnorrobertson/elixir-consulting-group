#!/usr/bin/env python3
"""Original local teaching checker; not schema, truth, security or approval validation."""
import argparse
import decimal
import json
from pathlib import Path
import sys
MAX_BYTES = 1024 * 1024

def check(path):
    with Path(path).open('rb') as handle:
        raw = handle.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError('file exceeds the chosen 1 MiB teaching limit')
    text = raw.decode('utf-8')
    counts = {'objects': 0, 'members': 0}
    def pairs_hook(pairs):
        result = {}
        for name, value in pairs:
            if name in result:
                raise ValueError('duplicate object name detected')
            result[name] = value
        counts['objects'] += 1
        counts['members'] += len(pairs)
        return result
    def reject_constant(value):
        raise ValueError('non-JSON numeric constant detected')
    value = json.loads(text, object_pairs_hook=pairs_hook,
                       parse_float=decimal.Decimal, parse_int=decimal.Decimal,
                       parse_constant=reject_constant)
    if not isinstance(value, dict):
        raise ValueError('this teaching subset requires a top-level object')
    return {'status': 'defined checks passed', 'object_count': counts['objects'],
            'member_count': counts['members'], 'top_level_member_count': len(value)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='local UTF-8 JSON file, at most 1 MiB')
    args = parser.parse_args()
    try:
        report = check(args.input)
    except (OSError, UnicodeError, ValueError, RecursionError, decimal.InvalidOperation, OverflowError):
        print('Input rejected by the defined teaching checks; inspect the local source and stated limits.', file=sys.stderr)
        return 2
    print(json.dumps(report, sort_keys=True))
    return 0
if __name__ == '__main__':
    sys.exit(main())

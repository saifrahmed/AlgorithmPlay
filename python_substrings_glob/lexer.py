#! /usr/bin/env python
# lexer.py
# David Prager Branner
# 20140619

from collections import deque

actions = {'?': ('dot'),
        '*': ('star')}

def lexer(p):
    """For each char or char-set in pattern, return a tuple naming its type.
    """
    # deque() is idempotent; no harm in this on recursion.
    p = deque(p)
    lexed = []
    while p:
        # There may be more than one char-set, so always reinitialize lexed_set
        lexed_set = []
        c = p.popleft()
        tag = 'char'
        if c == '\\':
            # Process following character as escaped.
            lexed.append((tag, p.popleft()))
        elif c == '[':
            # Handle character sets.
            first_c_in_set = p.popleft()
            # Special test of first character in set: neg. charsets, ].
            tag = 'set'
            if first_c_in_set in {'^', '!'}:
                # Discard character but change tag.
                tag = 'negset'
            else:
                # Close-] can only be added if it is first char in set,
                # the same as any other non-neg. character in that position.
                lexed_set.append(first_c_in_set)
            # Characters after first are added until close-] encountered.
            while p:
                # Check for closing of set.
                c_in_set = p.popleft()
                if c_in_set == ']':
                    break
                else:
                    lexed_set.append(c_in_set)
            lexed.append((tag, set(lexed_set)))
        else:
            lexed.append((tag, c))
    return lexed
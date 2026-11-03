"""
Station 1 project, part A: a tiny binary and hex converter.

THE RULES
- Write every conversion yourself, using the methods from the lessons:
  add up the coins, biggest coin first, group bits in fours, divide by 16.
- Inside your functions, don't use bin(), hex(), format(), or int(text, 2) / int(text, 16).
  Those do the work for you. The tests at the bottom use them to check your answers.
- Plain int(...) on a single digit character is fine, e.g. int("7") -> 7.

HOW TO WORK
1. Run this file:      python converter.py
2. Each milestone prints TODO, FAIL (with the input that broke it) or PASS.
3. Work through the milestones in order. Don't move on until the current one passes.
4. When all six pass, write main() and run:   python converter.py --menu
"""

HEX_DIGITS = "0123456789ABCDEF"   # position in this string = the digit's value. Handy!


# ---------------------------------------------------------------------------
# Milestone 1: binary -> decimal
# ---------------------------------------------------------------------------
def binary_to_decimal(bits: str) -> int:
    """'1101' -> 13,  '00000000' -> 0,  '11111111' -> 255

    Hint: walk through the bits. Either add the place value wherever there's a 1,
    or use the trick: total = total * 2 + bit (try it by hand on '1101' first).
    """
    total = 0
    for ch in bits:
        # Shift everything left one place (x2), then add the new bit.
        # '1101': 0*2+1=1 -> 1*2+1=3 -> 3*2+0=6 -> 6*2+1=13
        total = total * 2 + int(ch)
    return total


# ---------------------------------------------------------------------------
# Milestone 2: decimal -> binary
# ---------------------------------------------------------------------------
def decimal_to_binary(n: int) -> str:
    """13 -> '1101',  255 -> '11111111',  0 -> '0'  (careful with this one!)

    Hint: biggest coin first, or keep dividing by 2 and collect the remainders.
    (Remainders come out backwards: the last one you get is the leftmost bit.)
    """
    if n == 0:
        return "0"          # the loop below would return '' for 0
    bits = ""
    while n > 0:
        # The remainder is the lowest bit. Put it on the FRONT, since
        # remainders come out right-to-left.
        bits = str(n % 2) + bits
        n = n // 2
    return bits


# ---------------------------------------------------------------------------
# Milestone 3: binary -> hex
# ---------------------------------------------------------------------------
def binary_to_hex(bits: str) -> str:
    """'11001000' -> 'C8',  '101101' -> '2D',  '00001010' -> '0A'

    Give exactly one hex digit per group of 4 bits (so keep leading zeros,
    like '0A'). Output uppercase.
    Hint: pad on the LEFT with zeros until the length is a multiple of 4,
    then convert each group of 4 on its own. You already wrote something
    that turns bits into a number...
    """
    # Pad on the left until the length is a multiple of 4: '101101' -> '00101101'
    while len(bits) % 4 != 0:
        bits = "0" + bits
    result = ""
    for i in range(0, len(bits), 4):
        group = bits[i:i + 4]                 # e.g. '0010'
        value = binary_to_decimal(group)      # 0..15
        result += HEX_DIGITS[value]           # 2 -> '2', 13 -> 'D'
    return result


# ---------------------------------------------------------------------------
# Milestone 4: hex -> binary
# ---------------------------------------------------------------------------
def hex_to_binary(hex_text: str) -> str:
    """'3F' -> '00111111',  'A' -> '1010',  'ff' -> '11111111'

    Every hex digit becomes exactly 4 bits. Accept lowercase or uppercase input.
    Hint: find each digit's value with HEX_DIGITS, then turn it into 4 bits.
    """
    result = ""
    for ch in hex_text.upper():
        value = HEX_DIGITS.index(ch)          # 'F' -> 15
        four = decimal_to_binary(value)       # 15 -> '1111', 3 -> '11'
        while len(four) < 4:                  # '11' -> '0011'
            four = "0" + four
        result += four
    return result


# ---------------------------------------------------------------------------
# Milestone 5: hex <-> decimal
# ---------------------------------------------------------------------------
def hex_to_decimal(hex_text: str) -> int:
    """'C8' -> 200,  'ff' -> 255,  '10' -> 16

    Accept lowercase or uppercase.
    Hint: same trick as milestone 1, but with 16: total = total * 16 + digit_value
    """
    total = 0
    for ch in hex_text.upper():
        total = total * 16 + HEX_DIGITS.index(ch)   # 'C8': 12 -> 12*16+8 = 200
    return total


def decimal_to_hex(n: int) -> str:
    """200 -> 'C8',  255 -> 'FF',  16 -> '10',  0 -> '0'

    Output uppercase.
    Hint: divide by 16 and collect the remainders (backwards again).
    """
    if n == 0:
        return "0"
    result = ""
    while n > 0:
        result = HEX_DIGITS[n % 16] + result     # 200 % 16 = 8 -> '8', then 12 -> 'C'
        n = n // 16
    return result


# ---------------------------------------------------------------------------
# Milestone 6: a menu a person can actually use. All yours.
# ---------------------------------------------------------------------------
def main():
    """Ask what kind of number the user is typing (binary, decimal or hex),
    read it, then print it in all three forms. Keep looping until they type q.

    Make it friendly: if someone types '102' as binary or 'G7' as hex,
    print a helpful message instead of crashing.
    """
    print("Number converter. Type q at any prompt to quit.")
    while True:
        kind = input("\nWhat are you typing? (b)inary, (d)ecimal, (h)ex: ").strip().lower()
        if kind == "q":
            print("Bye!")
            return
        if kind not in ("b", "d", "h"):
            print("Please type b, d, h or q.")
            continue

        text = input("Number: ").strip()
        if text.lower() == "q":
            print("Bye!")
            return
        if text == "":
            print("You didn't type anything.")
            continue

        # Check the input BEFORE converting so bad input can't crash us.
        if kind == "b":
            bad = [ch for ch in text if ch not in "01"]
            if bad:
                print(f"'{text}' isn't binary: binary only uses 0 and 1 (found {bad[0]!r}).")
                continue
            n = binary_to_decimal(text)
        elif kind == "d":
            if not text.isdigit():
                print(f"'{text}' isn't a whole number: use digits 0-9 only.")
                continue
            n = int(text)
        else:
            bad = [ch for ch in text.upper() if ch not in HEX_DIGITS]
            if bad:
                print(f"'{text}' isn't hex: hex uses 0-9 and A-F (found {bad[0]!r}).")
                continue
            n = hex_to_decimal(text)

        print(f"  binary : {decimal_to_binary(n)}")
        print(f"  decimal: {n}")
        print(f"  hex    : {decimal_to_hex(n)}")


# ===========================================================================
# Tests. You don't need to change anything below this line.
# ===========================================================================
def _check(name, fn, cases):
    for arg, expected in cases:
        try:
            got = fn(arg)
        except NotImplementedError:
            print(f"TODO  {name}: not written yet")
            return False
        except Exception as e:
            print(f"FAIL  {name}({arg!r}) crashed with {type(e).__name__}: {e}")
            return False
        if got != expected:
            print(f"FAIL  {name}({arg!r}) gave {got!r}, expected {expected!r}")
            return False
    print(f"PASS  {name}  ({len(cases)} cases)")
    return True


def run_tests():
    nums = list(range(256)) + [256, 1000, 4096, 65535]
    bin_inputs = [format(n, "b") for n in nums] + [format(n, "08b") for n in range(256)]
    hex_inputs = [format(n, "X") for n in nums] + ["ff", "3f", "0A", "c8", "00FF"]

    results = [
        _check("binary_to_decimal", binary_to_decimal,
               [(b, int(b, 2)) for b in bin_inputs]),
        _check("decimal_to_binary", decimal_to_binary,
               [(n, format(n, "b")) for n in nums]),
        _check("binary_to_hex", binary_to_hex,
               [(b, format(int(b, 2), f"0{(len(b) + 3) // 4}X")) for b in bin_inputs]),
        _check("hex_to_binary", hex_to_binary,
               [(h, format(int(h, 16), f"0{4 * len(h)}b")) for h in hex_inputs]),
        _check("hex_to_decimal", hex_to_decimal,
               [(h, int(h, 16)) for h in hex_inputs]),
        _check("decimal_to_hex", decimal_to_hex,
               [(n, format(n, "X")) for n in nums]),
    ]

    passed = sum(results)
    print(f"\n{passed} of 6 conversion milestones passing.")
    if passed == 6:
        print("All conversions work. Now write main() and run:  python converter.py --menu")


if __name__ == "__main__":
    import sys
    if "--menu" in sys.argv:
        main()
    else:
        run_tests()

# Converting decimals into machine code

## The easier way

`"{:0>16b}".format(0)`

This says right align available space (16) for our binary type value and fill it with the `0` character. 

[source](https://docs.python.org/3/library/string.html#formatstrings)

## The harder way

Thinking about decimals as base 2 logarithms seems to be a nice way of converting them to binary. 

For example, the binary representation of the decimal 2 is 00000010 (8 digit binary). The base 2 log of 2 is 1. This means that we can only divide 2 once to get to 1.

What this also means is that we can "move" one place in our binary scale (keep the first place zero since there was no remainder). If we divide again, we'll end up with a remainder of 1. This means we stop moving places and our place has a value of 1.

## Examples 

Number: 7
Binary: 00000111
Log: 7 -> 3 -> 1

Number: 8
Binary: 00001000
Log: 8 (r0) -> 4 (r0) -> 2 (r0) -> 1

Number: 4
Binary: 00000100
Log: 4 (r0) -> 2 (r0) -> 1

Number: 3 
Binary: 00000011
Log: 3 -> 1

Number: 2
Binary: 00000010
Log: 2 (r0) -> 1

You'll notice a symmetry between the log patterns and the binary representation. Notice how if you reverse the binary representation and line up the final 1 with the tail of the log chain, the places where the binary place has a value of 0 is also where the division in the log pattern had a remainder of 0. This isn't a coincidence!

```
def decimal_to_binary(decimal_value, count=16):
    value = decimal_value 
    final_value = ""
    while value != 0:
        if value % 2 == 0:
            final_value = "0" + final_value
        else:
            final_value = "1" + final_value
        value = value // 2
    return final_value.rjust(16, "0")
```

# Parsing labels

You might start thinking you can just replace the label with the position of the line they're currently on. While that might work if there's a single label, it won't work for multiple labels because where the label should be will be offset by the number of labels that occurred previously. 

Example: 

```
0 A
1 A
2 C
3 (LABEL)
4 D
```
Failure:

```
0 A
1 A
2 C
3 (LABEL)
4 D
5 (LABEL2)
6 E
```

LABEL will be in the right place. But since it's excluded in the final output of the program, LABEL2 will be behind by 1! This is compounded by the number of labels preceding.

Solution? Keep track of the "real" program line count. If it's a valid instruction, we update our count. If it's a label, we'll keep the count and point to the current count. That way, we're always setting the label to the real line count (the one that would exist in the final hack program).

# Testing

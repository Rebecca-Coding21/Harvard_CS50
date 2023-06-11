import re
import math
import decimal

# prmpt cardnumber from the user

cardnumber = input("Cardnumber:")

sum2 = 0
sum1 = 0
digitIndex2 = 0
digitIndex1 = 1
digitNum = 1

# get length of cardnumber

length = len(cardnumber)

# set card number to int

cardnumber = int(cardnumber)


for m in range(1, length, 2):
    exponent = int(math.pow(10, m))

    digitIndex2 = digitIndex2 + 2
    digitI = int((cardnumber / exponent) % 10)
    print(digitI)
    product = digitI * 2

    if product > 9:
        sum2 = int(sum2 + (product % 10) + ((product / 10) % 10))
    else:
        sum2 = int(sum2 + product)

# get every first digit and calculate sum

for m in range(0, length, 2):
    exponent = pow(10, m)
    digitI = int((cardnumber / exponent) % 10)
    digitIndex1 = digitIndex1 + 2
    sum1 = int(sum1 + digitI)

digitIndex1 = digitIndex1 - 2

# calculate end sum

endSum = int(sum1 + sum2)

# get number number of first and second digit

digit1 = int(str(cardnumber)[0])
digit2 = int(str(cardnumber)[1])

# get cardtype


if (endSum % 10 == 0) and (digit1 == 3) and (digit2 == 4 or digit2 == 7) and (length == 15):
    print("AMEX")
elif (endSum % 10) == 0 and digit1 == 4 and (length == 16 or length == 13):
    print("VISA")
elif (endSum % 10) == 0 and digit1 == 5 and 0 < digit2 < 6 and length == 16:
    print("MASTERCARD")
else:
    print("INVALID")

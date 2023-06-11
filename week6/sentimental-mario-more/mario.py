# main function


def main():
    while True:
        try:
            height = int(input("Height:"))
            if height < 9 and height > 0:
                block(height)
                return
        except ValueError:
            print("Please input a number")

# function that arranges blocks


def block(height):
    width = height * 2 + 2
    # outer loop
    for h in range(0, height):

        # inner loop
        for w in range(0, width):

            if w < (height - h - 1) or ((height - 1 < w) and (w < height + 2)):
                print(" ", end='')
            elif w > (width - height + h):
                print("")
                break
            else:
                print("#", end='')

        #print(" ")
    print("")


main()
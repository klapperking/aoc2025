def main():
    solution = 0
    counter = 50
    with open("input.txt", "r") as f:
        for line in f:
            if line.startswith("L"):
                counter -= int(line.split("L")[1:][0])
            else:
                counter += int(line.split("R")[1:][0])

            counter = counter % 100

            if counter == 0:
                solution += 1

    print(solution)


if __name__ == "__main__":
    main()

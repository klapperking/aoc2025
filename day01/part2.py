def main():
    total_zeros = 0
    dial_position = 50
    with open("input.txt", "r") as f:
        for line in f:
            to_spin = 0
            if line.startswith("L"):
                to_spin -= int(line.split("L")[1:][0])
            else:
                to_spin += int(line.split("R")[1:][0])

            new_pos_non_adjusted = dial_position + to_spin
            passed_zeros_by_mult = abs((new_pos_non_adjusted) // 100)

            if new_pos_non_adjusted < 0:
                passed_zeros_by_mult += 1

            adjusted_position = new_pos_non_adjusted % 100

            if adjusted_position == 0 and not to_spin > 0:
                total_zeros += 1

            total_zeros += passed_zeros_by_mult

            dial_position = adjusted_position

    print(total_zeros)


if __name__ == "__main__":
    main()

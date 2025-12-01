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
            passed_zero_n_times = abs((new_pos_non_adjusted) // 100)

            # when startin from 0 and moving "left", we counted the 0 already
            # and floor divide will yield 1
            # FIXME: fix with the other issue +-1 or something
            if to_spin < 0 and dial_position == 0:
                passed_zero_n_times -= 1

            total_zeros += passed_zero_n_times

            dial_position = new_pos_non_adjusted % 100

            # adjust for 0 % 100 reaching 0 but modulo not counting
            # FIXME: find better way, something new_pos +- 1
            if dial_position == 0 and to_spin < 0:
                total_zeros += 1

    print(total_zeros)


if __name__ == "__main__":
    main()

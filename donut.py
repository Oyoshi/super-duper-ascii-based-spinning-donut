from argparse import ArgumentParser, HelpFormatter
from math import sin, cos, pi


########################## Constants ##################################

DELTA_THETA = 0.07
DELTA_PHI = 0.02

R1 = 1
R2 = 2
K2 = 5

SCREEN_WIDTH = 36
SCREEN_HEIGHT = 36

K1 = SCREEN_WIDTH * K2 * 3 / (8 * (R1 + R2))

A0 = 1.0
DELTA_A = 0.08
B0 = 1.0
DELTA_B = 0.03

SYMBOLS = ".,-~:;=!*#$@"

COLOUR_SHADES = 4
PINK_START_VAL = 204
MAGENTA_START_VAL = 197
GREEN_START_VAL = 154
BLUE_START_VAL = 24
COLOURS = {
    "pink": range(PINK_START_VAL, PINK_START_VAL + COLOUR_SHADES),
    "magenta": range(MAGENTA_START_VAL, MAGENTA_START_VAL + COLOUR_SHADES),
    "green": range(GREEN_START_VAL, GREEN_START_VAL + COLOUR_SHADES),
    "blue": range(BLUE_START_VAL, BLUE_START_VAL + COLOUR_SHADES),
}


def simulate_donut(A, B, colour):
    print("\x1b[2J")
    while True:
        render_frame(A, B, colour)
        A += DELTA_A
        B += DELTA_B


def render_frame(A, B, colour):
    char_output, colour_output = compute_frame(A, B, colour)

    print("\x1b[H")
    for i in range(SCREEN_HEIGHT):
        for j in range(SCREEN_WIDTH):
            print(
                f"\033[38;5;{colour_output[i][j]}m{char_output[i][j]}"
                if colour
                else char_output[i][j],
                end="",
            )
        print()


def compute_frame(A, B, colour):
    char_output = [[" " for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]
    colour_output = [[" " for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]
    zbuffer = [[0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

    sinA, cosA = sin(A), cos(A)
    sinB, cosB = sin(B), cos(B)

    theta = 0
    while theta < 2 * pi:
        sintheta, costheta = sin(theta), cos(theta)
        theta += DELTA_THETA

        phi = 0
        while phi < 2 * pi:
            sinphi, cosphi = sin(phi), cos(phi)
            phi += DELTA_PHI

            circle_x, circle_y = R2 + R1 * costheta, R1 * sintheta

            x = (
                circle_x * (cosB * cosphi + sinA * sinB * sinphi)
                - circle_y * cosA * sinB
            )
            y = (
                circle_x * (sinB * cosphi - sinA * cosB * sinphi)
                + circle_y * cosA * cosB
            )
            z = K2 + cosA * circle_x * sinphi + circle_y * sinA
            ooz = 1 / z

            xp, yp = int(SCREEN_WIDTH / 2 + K1 * ooz * x), int(
                SCREEN_HEIGHT / 2 - K1 * ooz * y
            )

            luminance = (
                cosphi * costheta * sinB
                - cosA * costheta * sinphi
                - sinA * sintheta
                + cosB * (cosA * sintheta - costheta * sinA * sinphi)
            )

            if luminance > 0 and ooz > zbuffer[xp][yp]:
                zbuffer[xp][yp] = ooz
                char_output[xp][yp], colour_output[xp][yp] = compute_char(
                    luminance, colour
                )

    return char_output, colour_output


def compute_char(luminance, colour):
    luminance_index = (int)(luminance * 8)
    if not colour:
        return SYMBOLS[luminance_index], None
    return (
        SYMBOLS[luminance_index],
        COLOURS[colour][luminance_index // (COLOUR_SHADES - 1)],
    )


def create_args_parser():
    args_parser = ArgumentParser(
        description="Super Duper ASCII Based Spinning Donut",
        allow_abbrev=False,
        formatter_class=lambda prog: HelpFormatter(prog, max_help_position=220),
    )
    args_parser.add_argument(
        "-c",
        type=str,
        choices=["pink", "magenta", "green", "blue"],
        metavar=f"['pink', 'magenta', 'green', 'blue']",
        help="Colours palette",
    )
    return args_parser


if __name__ == "__main__":
    args_parser = create_args_parser()
    options = args_parser.parse_args()
    simulate_donut(A0, B0, options.c)

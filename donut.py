from argparse import ArgumentParser, HelpFormatter
from math import sin, cos, pi


delta_theta = 0.07
delta_phi = 0.02

R1 = 1
R2 = 2
K2 = 5

screen_width = 64
screen_height = 64

K1 = screen_width * K2 * 3 / (8 * (R1 + R2))

SYMBOLS = ".,-~:;=!*#$@"
COLOURS = {"magenta": range(197, 201), "green": range(154, 158), "blue": range(24, 28)}


def simulate_donut(A, B, colour):
    print("\x1b[2J")
    while True:
        render_frame(A, B, colour)
        A += 0.08
        B += 0.03


def render_frame(A, B, colour):
    char_output, colour_output = compute_frame(A, B, colour)

    print("\x1b[H")
    for i in range(screen_height):
        for j in range(screen_width):
            if not colour:
                print(char_output[i][j], end="")
            else:
                print(f"\033[38;5;{colour_output[i][j]}m{char_output[i][j]}", end="")
        print()


def compute_frame(A, B, colour):
    char_output = [[" " for _ in range(screen_width)] for _ in range(screen_height)]
    colour_output = [[" " for _ in range(screen_width)] for _ in range(screen_height)]
    zbuffer = [[0 for _ in range(screen_width)] for _ in range(screen_height)]

    sinA, cosA = sin(A), cos(A)
    sinB, cosB = sin(B), cos(B)

    theta = 0
    while theta < 2 * pi:
        sintheta, costheta = sin(theta), cos(theta)
        theta += delta_theta

        phi = 0
        while phi < 2 * pi:
            sinphi, cosphi = sin(phi), cos(phi)
            phi += delta_phi

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

            xp, yp = int(screen_width / 2 + K1 * ooz * x), int(
                screen_height / 2 - K1 * ooz * y
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
    return SYMBOLS[luminance_index], COLOURS[colour][luminance_index // 3]


def create_args_parser():
    args_parser = ArgumentParser(
        description="Super Duper ASCII Based Spinning Donut",
        allow_abbrev=False,
        formatter_class=lambda prog: HelpFormatter(prog, max_help_position=120),
    )
    args_parser.add_argument(
        "-c",
        "--colour",
        type=str,
        choices=["magenta", "green", "blue"],
        metavar=f"['magenta', 'green', 'blue']",
        help="Colours palette",
    )
    return args_parser


if __name__ == "__main__":
    args_parser = create_args_parser()
    options = args_parser.parse_args()
    A, B = 1.0, 1.0
    simulate_donut(A, B, options.colour)

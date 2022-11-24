from math import sin, cos, pi


delta_theta = 0.07
delta_phi = 0.02

R1 = 1
R2 = 2
K2 = 5

screen_width = 48
screen_height = 48

K1 = screen_width * K2 * 3 / (8 * (R1 + R2))

SYMBOLS = ".,-~:;=!*#$@"
COLOURS = range(197, 201)


def simulate_donut(A, B):
    print("\x1b[2J")
    while True:
        render_frame(A, B)
        A += 0.08
        B += 0.03


def render_frame(A, B):
    char_output, colour_output = compute_frame(A, B)

    print("\x1b[H")
    for i in range(screen_height):
        for j in range(screen_width):
            print(f"\033[38;5;{colour_output[i][j]}m{char_output[i][j]}", end="")
        print()


def compute_frame(A, B):
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
                char_output[xp][yp], colour_output[xp][yp] = compute_char(luminance)

    return char_output, colour_output


def compute_char(luminance):
    luminance_index = (int)(luminance * 8)
    return SYMBOLS[luminance_index], COLOURS[luminance_index // 3]


if __name__ == "__main__":
    A, B = 1.0, 1.0
    simulate_donut(A, B)

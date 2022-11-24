from math import sin, cos, pi


theta_spacing = 0.07
phi_spacing = 0.02

R1 = 1
R2 = 2
K2 = 5

screen_width = 48
screen_height = 48

K1 = screen_width * K2 * 3 / (8 * (R1 + R2))


def render_frame(A, B):
    char_output = [[" " for _ in range(screen_width)] for _ in range(screen_height)]
    color_output = [[" " for _ in range(screen_width)] for _ in range(screen_height)]
    zbuffer = [[0 for _ in range(screen_width)] for _ in range(screen_height)]

    sinA, cosA = sin(A), cos(A)
    sinB, cosB = sin(B), cos(B)

    theta = 0
    while theta < 2 * pi:
        costheta = cos(theta)
        sintheta = sin(theta)
        theta += theta_spacing

        phi = 0
        while phi < 2 * pi:
            cosphi = cos(phi)
            sinphi = sin(phi)
            phi += phi_spacing

            circle_x = R2 + R1 * costheta
            circle_y = R1 * sintheta

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

            xp = int(screen_width / 2 + K1 * ooz * x)
            yp = int(screen_height / 2 - K1 * ooz * y)

            luminance = (
                cosphi * costheta * sinB
                - cosA * costheta * sinphi
                - sinA * sintheta
                + cosB * (cosA * sintheta - costheta * sinA * sinphi)
            )

            if luminance > 0:
                if ooz > zbuffer[xp][yp]:
                    zbuffer[xp][yp] = ooz
                    luminance_index = (int)(luminance * 8)

                    char_output[xp][yp] = ".,-~:;=!*#$@"[luminance_index]
                    if luminance_index < 3:
                        color_output[xp][yp] = "126"
                    elif luminance_index >= 3 and luminance_index < 6:
                        color_output[xp][yp] = "127"
                    elif luminance_index >= 6 and luminance_index < 9:
                        color_output[xp][yp] = "128"
                    else:
                        color_output[xp][yp] = "129"

    print("\x1b[H")
    for i in range(screen_height):
        for j in range(screen_width):
            print(f"\033[38;5;{color_output[i][j]}m", end="")
            print(char_output[i][j], end="")
        print()


print("\x1b[2J")
A = 1.0
B = 1.0

while True:
    render_frame(A, B)
    A += 0.08
    B += 0.03

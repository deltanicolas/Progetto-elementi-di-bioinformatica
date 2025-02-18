import os
import time


def dna_animation(text: str) -> None:
    frames = [
        f"""
    A---T
     A-T
      A
     T-A
    T---A
    G---C
     G-C
      G
     C-G
    C---G
 {text}
            """,
        f"""
     A-T
      A
     T-A
    T---A
    G---C
     G-C
      G
     C-G
    C---G
    A---T
 {text}.
            """,
        f"""
      A
     T-A
    T---A
    G---C
     G-C
      G
     C-G
    C---G
    A---T
     A-T
 {text}..
            """,
        f"""
     T-A
    T---A
    G---C
     G-C
      G
     C-G
    C---G
    A---T
     A-T
      A
 {text}...
            """,
        f"""
    T---A
    G---C
     G-C
      G
     C-G
    C---G
    A---T
     A-T
      A
     T-A
 {text}.
            """
    ]

    for frame in frames:
        os.system('cls')
        print('\r' + frame)
        time.sleep(0.1)

    os.system('cls')


if __name__ == "__main__":
    dna_animation("ciao")

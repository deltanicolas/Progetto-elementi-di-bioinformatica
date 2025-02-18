import argparse
import os
import pathlib


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Progetto di Elementi di Bioinformatica, Traccia numero 4,  di Chines Nicolas, Matricola: 899536",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-f', '--file', type=check_fastq, nargs='?',
                        help="Percorso del file FASTQ. Se non specificato, verrà utilizzato un file nella directory corrente.",
                        default=find_fastq_in_directory())
    parser.add_argument('-fr', '--frequency', type=check_frequency,
                        help="Soglia di frequenza (0 <= F <= 1).",
                        default=0.00142)
    parser.add_argument('-k', '--kmer', type=check_positive_integer,
                        help="Lunghezza dei k-meri, (K > 0).",
                        default=7)
    return parser.parse_args()



def check_frequency(value) -> float:
    fvalue = float(value)
    if not 0 <= fvalue <= 1:
        raise argparse.ArgumentTypeError("La soglia di frequenza F deve essere tra 0 e 1.")
    return fvalue



def check_positive_integer(value) -> int:
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("Il valore K deve essere un intero positivo.")
    return ivalue


def check_fastq(value) -> pathlib.Path:
    path = pathlib.Path(value)
    if not path.is_file() or not str(path).endswith('.fastq'):
        raise argparse.ArgumentTypeError(f"{value} non è un file FASTQ valido.")
    return path



def find_fastq_in_directory() -> list[str]:
    files = [f for f in os.listdir('.') if f.endswith('.fastq')]
    if not files:
        raise FileNotFoundError("Nessun file .fastq trovato nella directory corrente.")
    return files


def chose_fastq_files(files: list[str]) -> str:
    if type(files) != list:
        return files
    if len(files) == 1:
        return files[0]
    print("Seleziona un file FASTQ dalla lista:")
    for i, file in enumerate(files):
        print(f"{i + 1}) {file}")
    while True:
        try:
            choice = int(input("Inserisci il numero del file da utilizzare: "))
            if 1 <= choice <= len(files):
                return files[choice - 1]
            else:
                print("Scelta non valida, riprova.")
        except ValueError:
            print("Inserisci un numero valido.")
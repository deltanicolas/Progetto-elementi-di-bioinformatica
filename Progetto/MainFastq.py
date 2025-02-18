
import os
import statistics
import threading
import matplotlib.pyplot as plt
from Bio import SeqIO
import Animations
import ArgumentParser


class FastqAnalyzer:
    """
    Classe principale per effettuare tutte le operazioni nel file FASTQ
    """

    def __init__(self, file_path: str, frequency: float, kmer_length: int) -> None:
        self.file_path = file_path
        self.frequency = frequency
        self.kmer_length = kmer_length
        self.fastq_records = []
        self.sequences = []
        self.quality_scores = []
        self.kmer_dict = {}
        self.kmer_pos_dict = {}
        self.kmer_max = ""
        self.kmer_max_pos = 0

    def load_fastq(self) -> None:
        fastq_records = list(SeqIO.parse(self.file_path, 'fastq'))
        if not fastq_records:
            raise ValueError(f"Il file {self.file_path} non contiene sequenze valide.")

        self.fastq_records = fastq_records
        self.sequences = [str(record.seq) for record in fastq_records]
        self.quality_scores = [record.letter_annotations['phred_quality'] for record in fastq_records]

    def calculate_kmers(self) -> None:
        read_length = len(self.sequences[0])
        for seq_index, seq in enumerate(self.sequences):
            for i in range(0, read_length - self.kmer_length + 1):
                kmer = seq[i:i + self.kmer_length]

                # Aggiorna dizionario delle posizioni per ogni sequenza
                seq_dict = self.kmer_dict.get(kmer, {})
                pos_found = seq_dict.get(seq_index, {})
                pos_found[i] = 1
                seq_dict[seq_index] = pos_found
                self.kmer_dict[kmer] = seq_dict

                # Aggiorna conteggio per posizione
                pos_arr = self.kmer_pos_dict.get(kmer, [0] * read_length)
                pos_arr[i] += 1
                self.kmer_pos_dict[kmer] = pos_arr

    def filter_kmers_by_frequency(self) -> None:
        total_positions = (len(self.sequences[0]) - self.kmer_length + 1) * len(self.sequences)
        filtered_kmer_dict = {}
        filtered_kmer_pos_dict = {}

        for kmer, pos_array in self.kmer_pos_dict.items():
            frequency = sum(pos_array) / total_positions
            if frequency >= self.frequency:
                filtered_kmer_dict[kmer] = self.kmer_dict[kmer]
                filtered_kmer_pos_dict[kmer] = pos_array

        if not filtered_kmer_dict:
            raise ValueError("Nessun k-mero supera la soglia di frequenza specificata. Modifica la soglia e riprova.")

        self.kmer_dict = filtered_kmer_dict
        self.kmer_pos_dict = filtered_kmer_pos_dict

    def find_most_frequent_kmer(self) -> None:
        max_count = 0
        for kmer, positions in self.kmer_pos_dict.items():
            for i, count in enumerate(positions):
                if count > max_count:
                    max_count = count
                    self.kmer_max = kmer
                    self.kmer_max_pos = i

    def save_fasta_output(self, output_path: str) -> None:
        output_list = []
        for seq_index, positions in self.kmer_dict.get(self.kmer_max).items():
            if self.kmer_max_pos in positions:
                record = self.fastq_records[seq_index]
                record.description += f" quality_mean={statistics.mean(self.quality_scores[seq_index]):.2f}"
                output_list.append(record)

        SeqIO.write(output_list, output_path, 'fasta')

    def plot_kmer_occurrences(self, kmer: str) -> None:
        y_values = self.kmer_pos_dict.get(kmer)
        x_values = list(range(len(y_values)))
        plt.figure(figsize=(15, 6), dpi=100)
        plt.bar(x_values, y_values, color='blue')
        plt.xlabel('Posizioni')
        plt.ylabel('Occorrenze')
        plt.title(f'Occorrenze del k-mer: {kmer}')
        plt.xticks(list(range(0, len(x_values), 5)))
        plt.show()

    def plot_all_kmers(self) -> None:
        kmer_list = list(self.kmer_pos_dict.keys())
        print("K-mer disponibili:")
        for i, kmer in enumerate(kmer_list):
            print(f"{i}: {kmer}")
        while True:
            choice = input("Inserisci l'indice del k-mer da visualizzare (o 'exit' per uscire): ").strip()
            if choice.lower() == 'exit':
                break
            try:
                index = int(choice)
                if 0 <= index < len(kmer_list):
                    self.plot_kmer_occurrences(kmer_list[index])
                else:
                    print("Indice non valido.")
            except ValueError:
                print("Input non valido.")




if __name__ == "__main__":

    args = vars(ArgumentParser.parse_arguments())
    analyzer = FastqAnalyzer(
        file_path=ArgumentParser.chose_fastq_files(args['file']),
        frequency=args['frequency'],
        kmer_length=args['kmer']
    )

    def process_workload():
        analyzer.load_fastq()
        analyzer.calculate_kmers()

    calculate_kmer_process = threading.Thread(name='process', target=process_workload)
    calculate_kmer_process.start()
    while calculate_kmer_process.is_alive():
        Animations.dna_animation("Calcolo k-meri in corso")

    analyzer.filter_kmers_by_frequency()
    analyzer.plot_all_kmers()
    analyzer.find_most_frequent_kmer()
    print(f"Il k-mero più frequente è '{analyzer.kmer_max}' nella posizione {analyzer.kmer_max_pos}.")
    os.system("pause")
    analyzer.plot_kmer_occurrences(analyzer.kmer_max)

    output_file = input("Inserisci il nome del file di output (senza estensione, verra salvato in automatico un file FASTA): ")
    analyzer.save_fasta_output(output_file + '.fasta')
    print(f"File salvato con successo!")


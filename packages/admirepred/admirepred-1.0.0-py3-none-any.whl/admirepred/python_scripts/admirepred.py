import numpy as np
import pandas as pd
import joblib
import pickle
import os
import glob
import argparse
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", type=str, help='Path to fasta file', required=True)
    parser.add_argument("--output", "-o", type=str, help='Path to output', required=True)
    parser.add_argument("--model", "-m", type=int, help='Model selection: 1 for ML only, 2 for ML + BLAST', default=1)
    parser.add_argument("--threshold", "-t", type=float, help='Threshold for classification', default=0.5)

    args = parser.parse_args()
    fasta_loc = args.file
    output_loc = args.output
    model_choice = args.model
    threshold = args.threshold
    nf_path = os.path.dirname(os.path.abspath(__file__))

    #### padding with ohe ####

    # Function to read FASTA file and get sequences
    def read_fasta(file_path):
        sequences = []
        headers = []
        with open(file_path, 'r') as file:
            sequence = ''
            for line in file:
                line = line.strip()
                if line.startswith('>'):
                    if sequence:
                        sequences.append(sequence)
                        sequence = ''
                    headers.append(line[1:])
                else:
                    sequence += line
            if sequence:
                sequences.append(sequence)
        return headers, sequences

    # Function to pad sequences with 'X' to make them equal length of 26
    def pad_sequences(sequences, fixed_length=25):
        padded_sequences = []
        for seq in sequences:
            if len(seq) > fixed_length:
                padded_seq = seq[:fixed_length]
            else:
                padded_seq = seq.ljust(fixed_length, 'X')
            padded_sequences.append(padded_seq)
        return padded_sequences

    # Function to one-hot encode the sequences
    def one_hot_encode_sequence(seq, fixed_length=25):
        bases = 'ACGUX'  # Including 'X' for padding
        encoding = np.zeros((fixed_length, len(bases)), dtype=int)
        base_to_index = {base: index for index, base in enumerate(bases)}

        for i, base in enumerate(seq):
            encoding[i, base_to_index[base]] = 1

        return encoding.flatten()

    # Generate column names
    def generate_column_names(fixed_length=25):
        bases = 'ACGUX'
        column_names = []
        for i in range(1, fixed_length + 1):
            for base in bases:
                column_names.append(f"{base}_{i}")
        return column_names

    # Main function to process the FASTA file and save the DataFrame
    def process_fasta(fasta_file):
        headers, sequences = read_fasta(fasta_file)
        padded_sequences = pad_sequences(sequences)

        one_hot_encoded_sequences = [one_hot_encode_sequence(seq) for seq in padded_sequences]
        column_names = generate_column_names()

        ohe_df = pd.DataFrame(one_hot_encoded_sequences, index=headers, columns=column_names)
        #df.to_csv(output_csv)
        return ohe_df

    #fasta_file = '/content/drive/MyDrive/exomirpred/train_seq_s1.fa'
    #output_csv = 'one_hot_encoded_sequences.csv'
    ohe_df = process_fasta(fasta_loc)

    #### Reverse complement and then generate TFIDF ####

    # Function to read FASTA file and get sequences
    def read_fasta(file_path):
        sequences = []
        headers = []
        with open(file_path, 'r') as file:
            sequence = ''
            for line in file:
                line = line.strip()
                if line.startswith('>'):
                    if sequence:
                        sequences.append(sequence)
                        sequence = ''
                    headers.append(line[1:])
                else:
                    sequence += line
            if sequence:
                sequences.append(sequence)
        return headers, sequences

    # Function to get the reverse complement of an RNA sequence
    def reverse_complement(seq):
        complement = {'A': 'U', 'U': 'A', 'C': 'G', 'G': 'C'}
        reverse_complement_seq = ''.join(complement[base] for base in reversed(seq))
        return reverse_complement_seq

    def process_fasta_with_tfidf(fasta_file):
        # Load the feature names from feature_names_tfidf.csv
        feature_names_df = pd.read_csv(f"{nf_path}/../data/feature_names_tfidf.csv")
        vocabulary = feature_names_df.columns.tolist()  # Use the column names as vocabulary

        headers, sequences = read_fasta(fasta_file)
        reverse_complements = [reverse_complement(seq) for seq in sequences]

        # Initialize the TF-IDF vectorizer with the predefined vocabulary
        vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 2), vocabulary=vocabulary)
        tfidf_matrix = vectorizer.fit_transform(reverse_complements)

        # Convert the TF-IDF matrix to a DataFrame
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), index=headers, columns=vectorizer.get_feature_names_out())

        return tfidf_df

    tfidf_df = process_fasta_with_tfidf(fasta_loc)

    ##### combining dataframes #####

    combined_df = pd.concat([ohe_df, tfidf_df], axis=1)

    # Function to load the model from a .pkl file
    def load_model(file_path):
        model = joblib.load(file_path)
        return model

    # Load the model
    model_path = f"{nf_path}/../model/admirepred_et_model.pkl"
    model = load_model(model_path)

    # Assuming combined_df is already defined and is a DataFrame
    # Convert combined_df to a NumPy array for prediction
    if 'combined_df' not in locals() and 'combined_df' not in globals():
        raise ValueError("combined_df is not defined. Please define combined_df before running predictions.")

    # Ensure combined_df is in the correct format for prediction
    features_array = np.array(combined_df)
    features_array = pd.DataFrame(features_array, columns=model.feature_names_in_)

    # Predict probabilities
    probabilities = model.predict_proba(features_array)
    y_pred = probabilities[:, 1]

    # Create a new DataFrame with Seq_ID and predicted probabilities
    prob_df = pd.DataFrame({
        'Seq_ID': combined_df.index,
        'ML_pred': y_pred
    })


    # If model_choice is 1, save and return prob_df
    if model_choice == 1:
        #prob_df.to_csv(output_loc + "/prob_df.csv", index=False)
        classification_df = prob_df.copy()
        classification_df['class'] = classification_df['ML_pred'].apply(lambda x: 'exosomal' if x > threshold else 'non-exosomal')
        classification_df.to_csv(output_loc + "/classification_ML.csv", index=False)
        #print("ML only results saved to", output_loc + "/prob_df.csv")
        print("Classification results saved to", output_loc + "/classification_ML.csv")

    else:

        ############ BLAST ##############


        # Define the paths

        db_path = f"{nf_path}/../blast_db/exosomal_db"
        output_path = f"{nf_path}/../blast_db/10e-2.txt"

        # Construct the BLAST command
        blast_command = f"blastn -task blastn-short -db {db_path} -query {fasta_loc} -out {output_path} -outfmt 6 -evalue 0.01"

        # Execute the BLAST command
        os.system(blast_command)

        #evalue = 0.01
        dfb = pd.read_csv(f"{nf_path}/../blast_db/10e-2.txt", sep ="\t", header = None)
        dfb1 = dfb.iloc[:,0:3]
        dfb1.columns =['query', 'hit', 'percent']
        #dfb1 = (dfb1[dfb1.percent != 100])
        dfb1 = dfb1.sort_values(by="percent",ascending=False)
        dfb2 = dfb1.groupby('query').first()
        dfb2.to_csv(f"{nf_path}/../blast_db/10e-2_results.txt", sep = "\t")
        dfb2 = pd.read_csv(f"{nf_path}/../blast_db/10e-2_results.txt", sep ="\t", header=0)
        # Creating a set of query IDs for quick lookup
        query_set = set(dfb2['query'])
        # Adding the 'blast_pred' column to prob_df
        prob_blast_df = prob_df.copy()
        prob_blast_df['blast_pred'] = prob_blast_df['Seq_ID'].apply(lambda x: 0.5 if x in query_set else 0)


        ####### total predictions ######

        # Create the new column 'total_pred'

        # Merge prob_df with prob_blast_df to include the blast_pred column
        merged_df = prob_df.merge(prob_blast_df[['Seq_ID', 'blast_pred']], on='Seq_ID', how='left')
        # Merge the result with prob_merci_pred to include the merci_pred column
        prob_hybrid_df = merged_df
        prob_hybrid_df['total_pred'] = prob_df['ML_pred'] + prob_blast_df['blast_pred']
        # Display or save the updated DataFrame
        #prob_hybrid_df.to_csv(output_loc + "/prob_hybrid_df.csv", index=False)

        # Generate classification_hybrid.csv
        classification_hybrid_df = prob_hybrid_df.copy()
        hybrid_threshold = 0.50 if threshold == 0.5 else threshold  # Use 0.52 if default threshold is used for hybrid
        classification_hybrid_df['class'] = classification_hybrid_df['total_pred'].apply(lambda x: 'exosomal' if x > hybrid_threshold else 'non-exosomal')
        classification_hybrid_df.to_csv(output_loc + "/classification_hybrid.csv", index=False)
        
        #print("Hybrid results saved to", output_loc + "/prob_hybrid_df.csv")
        print("Classification results saved to", output_loc + "/classification_hybrid.csv")
if __name__ == "__main__":
    main()
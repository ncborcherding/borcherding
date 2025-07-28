#!/bin/bash

# ##############################################################################
#
# Immcantation Pipeline Automation Script
#
# This script automates the process of running AssignGenes.py and MakeDb.py
# on multiple 10x Genomics sample outputs.
#
# It searches for sample directories (e.g., SRR13670784) within a base
# directory, finds the 'all_contig.fasta' file for each, and then executes
# the two main processing steps from the Immcantation framework.
#
# ##############################################################################

# --- Configuration ---
# Set the base directory where your sample folders (SRR*) are located.
# IMPORTANT: Update this path to the correct location on your system.
BASE_DIR="/Users/borcherding.n/Documents/Immcantation/Alignments"

# Set paths to shared resources.
# Using the $HOME variable is more robust than using '~' as it ensures
# the full path is passed to the underlying programs.
IGBLAST_DIR="$HOME/share/igblast"
GERMLINE_DIR="$HOME/share/germlines/imgt/human/vdj/imgt_human_*.fasta"

# --- Script Start ---
echo "Starting pipeline processing..."
echo "Base directory: ${BASE_DIR}"
echo "--------------------------------------------------"

# Check if the base directory exists
if [ ! -d "$BASE_DIR" ]; then
    echo "Error: Base directory '${BASE_DIR}' not found."
    echo "Please update the BASE_DIR variable in the script."
    exit 1
fi

# Loop through each directory inside the BASE_DIR
# The wildcard '*' will match all items in the directory.
for SAMPLE_DIR in "${BASE_DIR}"/*/; do

    # Define the full path to the input FASTA file for the current sample
    FASTA_FILE="${SAMPLE_DIR}BCR/all_contig.fasta"

    # Check if the all_contig.fasta file exists before proceeding
    if [ -f "$FASTA_FILE" ]; then
        
        # Get the sample name from the directory path for logging
        SAMPLE_NAME=$(basename "${SAMPLE_DIR}")
        echo "--- Processing Sample: ${SAMPLE_NAME} ---"

        # Define the output directory (which is the 'outs' folder)
        OUTPUT_DIR=$(dirname "${FASTA_FILE}")

        # Define the path for the intermediate IgBLAST output file
        IGBLAST_OUTPUT="${OUTPUT_DIR}/all_contig_igblast.fmt7"

        # Define the path for the final 10x annotation output file
        ANNOTATION_OUTPUT="${OUTPUT_DIR}/all_contig_annotations.csv"

        # --- Step 1: Run AssignGenes.py (igblast) ---
        echo "Step 1: Running AssignGenes.py for ${SAMPLE_NAME}..."
        AssignGenes.py igblast \
            -s "${FASTA_FILE}" \
            -b "${IGBLAST_DIR}" \
            --organism human \
            --loci ig \
            --format blast

        # Check if the previous command was successful
        if [ $? -ne 0 ]; then
            echo "Error: AssignGenes.py failed for sample ${SAMPLE_NAME}. Skipping to next sample."
            continue # Skips to the next iteration of the loop
        fi
        
        echo "AssignGenes.py completed."
        echo "" # Add a blank line for readability

        # --- Step 2: Run MakeDb.py (igblast) ---
        echo "Step 2: Running MakeDb.py for ${SAMPLE_NAME}..."
        MakeDb.py igblast \
            -i "${IGBLAST_OUTPUT}" \
            -s "${FASTA_FILE}" \
            -r ${GERMLINE_DIR} \
            --10x "${ANNOTATION_OUTPUT}" \
            --extended

        # Check if the previous command was successful
        if [ $? -ne 0 ]; then
            echo "Error: MakeDb.py failed for sample ${SAMPLE_NAME}."
        else
            echo "MakeDb.py completed."
        fi

        echo "--- Finished processing ${SAMPLE_NAME} ---"
        echo "--------------------------------------------------"

    else
        # Print a message if a directory doesn't contain the expected file
        echo "Warning: 'outs/all_contig.fasta' not found in $(basename "${SAMPLE_DIR}"). Skipping."
        echo "--------------------------------------------------"
    fi
done

echo "All samples processed. Pipeline finished."

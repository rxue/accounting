#!/usr/bin/env bash
set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

ls_highlight_pdf() {
    ls | while read -r line; do
        if [[ "$line" == *.pdf ]]; then
            echo -e "${GREEN}${BOLD}$line${RESET}"
        else
            echo "$line"
        fi
    done
}

type_text() {
    local color="$1"
    local text="$2"
    local delay="${3:-0.08}"
    echo -ne "${color}"
    for ((i = 0; i < ${#text}; i++)); do
        echo -ne "${text:$i:1}"
        sleep "$delay"
    done
    echo -e "${RESET}"
}

type_text "${BOLD}" "=== Financial Statements Generator ==="
echo
type_text "${CYAN}" "This program generates financial statements in PDF"
type_text "${CYAN}" "based on bank statement CSV files from a given directory."
type_text "${CYAN}" "It produces two documents: an Income Statement and a Balance Sheet."
echo
sleep 4

type_text "${BOLD}" "--- Step 1: Check for existing PDF files ---"
type_text "${CYAN}" "Running: ls"
ls_highlight_pdf
echo
sleep 2
type_text "" "Removing existing PDF files..."
rm -f *.pdf
echo
type_text "${CYAN}" "Running: ls"
ls
echo
sleep 2
type_text "${CYAN}" "Now that no PDF file exists, I am going to preview the input data and then run the program to generate the financial statement PDF files again."
sleep 4

INPUT_DIR=~/Documents/outlierx/tiliote/extracted

type_text "${BOLD}" "--- Step 2: Preview input data before generating the financial statements ---"
type_text "${CYAN}" "The bank statement CSV files are located in:"
echo -e "  $INPUT_DIR"
echo
type_text "${CYAN}" "Here is a sample from one of the CSV files:"
sleep 2
echo
head -5 "$INPUT_DIR/Tiliote_2025-07-15_2025-07-31.csv"
echo
sleep 5

type_text "${BOLD}" "--- Step 3: Generate financial statement pdf files, i.e. income statement and balance sheet ---"
echo -ne "${CYAN}Running:${RESET} "
type_text "" "python -m financialstatements pdf --input-dir $INPUT_DIR --company-name \"sample company\"" 0.06
echo
python -m financialstatements pdf --input-dir "$INPUT_DIR" --company-name "sample company"
echo
sleep 3

type_text "${BOLD}" "--- Step 4: Running ls command again (highlight the generated pdf files like in Step 1) ---"
ls_highlight_pdf
echo
sleep 3

type_text "${BOLD}" "--- Step 5: Opening generated PDFs ---"
sleep 3
type_text "${CYAN}" "Opening income_statement.pdf first, then balance_sheet.pdf ..."
sleep 2
evince income_statement.pdf &
EVINCE_IS_PID=$!
sleep 3
evince balance_sheet.pdf &
EVINCE_BS_PID=$!

sleep 5
kill $EVINCE_IS_PID $EVINCE_BS_PID 2>/dev/null
sleep 3
echo
type_text "${BOLD}" "Thanks for watching! Bye Bye :)"
sleep 3


#!/bin/bash

if [ "$#" -ne 1 ]; then 
    echo "[+] Usage $0 <PDF/or/PDF directory/>"
    exit 1
fi

if [ -f $1 ]; then
    cd "${0%/*}"
    # get the basename
    file_basename=`basename ${1} .pdf`
    output_file=${file_basename}".txt"
    SQL_FILE=${file_basename}".sql"
    echo "[+] Converting PDF to text"
    pdftotext -f 1 -l 1 -layout ${1}
    # delete everything before stock data
    echo "[+] Deleting header"
    first_data_line=`grep "BHL" -n ${output_file} | cut -d ":" -f 1`
    end_delete=$(($first_data_line - 1 ))
    sed -i 1,${end_delete}d ${output_file}
    echo "[+] Deleting footer"
    # delete everything after the last symbol data
    last_data_line=`grep "TNM" -n ${output_file} | cut -d ":" -f 1`
    footer_start_line=$(($last_data_line+1))
    sed -i ${footer_start_line},+5d ${output_file}

    echo "[+] Deleting empty spaces"
    tmp_file=${file_basename}".tmp"
    awk '{$1=$1}{ print }' ${output_file} > ${tmp_file}

    echo "[+] Removing more empty spaces if any"
    csv_file=${file_basename}".csv"
    awk 'NF > 0' ${tmp_file} > ${csv_file}

    echo "[+] Cleaning up"
    rm ${output_file}
    rm ${tmp_file}

    echo "[+] Removing commas"
    sed -i s/,//g ${csv_file}
    # DEBUG : cp ${csv_file} before.txt

    # compensate for missing columns
    # Note : overwrites ${tmp_file}
    ./fill_missing_fields.py ${csv_file}
    # DEUBG: cp ${tmp_file} after.txt

    # remove unneeded colums, overwrites ${csv_file}
    cut -d, -f 2-4,7-9 ${tmp_file} > ${csv_file}

    echo "[+] Inserting date"
    day=`basename ${csv_file} | cut -d "_" -f 2` 
    month=`basename ${csv_file} | cut -d "_" -f 3` 
    year=`basename ${csv_file} | cut -d "_" -f 4 | cut -d "." -f 1` 
    trading_date=${day}-${month}-${year}
    sed -i s/^/STR_TO_DATE\(\'${trading_date}\'\,\"\%d-\%M-\%Y\"\)\,/g ${csv_file}

    # replace tickers with  SQL SELECT
    echo "[+] Replacing ticker with SELECT"
    awk -F "," 'BEGIN{OFS=","}{ gsub($5, "(SELECT id FROM symbol WHERE ticker=\"" $5 "\")", $5); print $0}' ${csv_file} > ${tmp_file}
    echo "[+] Counting records"
    record_count=`wc -l ${tmp_file} | cut -d " " -f 1`
    echo "[+] ${record_count} records found."
    awk -v RCOUNT=$record_count -F "," 'BEGIN{ OFS=","; print "INSERT INTO daily_price (trading_date,high,low,symbol_id,open,close,volume) VALUES" } 
            { if (NR < RCOUNT) { print "(" $0 ")," } 
            else { print "(" $0 ")" }}' ${tmp_file} > $SQL_FILE
    
    echo "[+] Cleaning up."
    rm ${tmp_file}
    rm ${csv_file}
    # Hack
    sed -i 's/trading_date/exchange_id,trading_date/g' $SQL_FILE
    sed -i 's/STR_/1,STR_/g' $SQL_FILE
    echo "[+] Done. File is saved as : ${SQL_FILE}"
    exit 0
fi

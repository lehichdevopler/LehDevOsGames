note_loop=true

while [ "$note_loop" == "true" ]; do
    clear
    echo "=== NOTE TAKER ==="
    echo "1. Read notes"
    echo "2. Add note"
    echo "3. Clear notes"
    echo "4. Exit"
    echo -n "Select: "
    read opt

    if [ "$opt" == "1" ]; then
        echo "--- YOUR NOTES ---"
        cat notes.txt 2>/dev/null
        echo "------------------"
        read -p "Press Enter..." d
    elif [ "$opt" == "2" ]; then
        echo -n "Type your note: "
        read new_note
        echo "$new_note" >> notes.txt
        echo "Saved!"
        sleep 1
    elif [ "$opt" == "3" ]; then
        echo "" > notes.txt
        echo "Notes cleared."
        sleep 1
    elif [ "$opt" == "4" ]; then
        note_loop=false
    fi
done

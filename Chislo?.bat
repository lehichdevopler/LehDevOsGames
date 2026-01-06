target=$(( ( RANDOM % 100 ) + 1 ))
guessed=false
attempts=0

clear
echo "=== GUESS THE NUMBER (1-100) ==="

while [ "$guessed" == "false" ]; do
    echo -n "Your guess: "
    read user_guess
    attempts=$((attempts+1))

    if [ "$user_guess" -eq "$target" ]; then
        echo "Correct! You won in $attempts attempts."
        guessed=true
    elif [ "$user_guess" -lt "$target" ]; then
        echo "Too low! Try again."
    else
        echo "Too high! Try again."
    fi
done

echo "Press Enter to exit..."
read dummy

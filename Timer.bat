clear
echo "=== TIMER ==="
echo -n "Enter seconds to countdown: "
read seconds

while [ $seconds -gt 0 ]; do
    clear
    echo "Time remaining: $seconds"
    sleep 1
    seconds=$((seconds - 1))
done

clear
echo "TIME IS UP!"
echo -e "\a" # Звуковой сигнал (если поддерживается терминалом)
read -p "Press Enter to exit..." d

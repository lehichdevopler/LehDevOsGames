viewing=true

while [ "$viewing" == "true" ]; do
    clear
    echo "=== CURRENT TIME ==="
    echo "Press Ctrl+C to exit"
    echo ""
    date "+%H:%M:%S"
    sleep 1
done

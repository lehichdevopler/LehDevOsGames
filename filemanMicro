fm_loop=true

while [ "$fm_loop" == "true" ]; do
    clear
    echo "=== MINI FILE MANAGER ==="
    echo "Current dir: $(pwd)"
    echo "-----------------------"
    ls -1
    echo "-----------------------"
    echo "Type a folder name to cd, '..' to go back, or 'exit':"
    read cmd

    if [ "$cmd" == "exit" ]; then
        fm_loop=false
    elif [ -d "$cmd" ]; then
        cd "$cmd"
    else
        echo "Directory not found!"
        sleep 1
    fi
done

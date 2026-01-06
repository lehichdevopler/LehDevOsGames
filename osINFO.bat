clear
echo "=== SYSTEM INFO ==="
echo "User: $(whoami)"
echo "Hostname: $(hostname)"
echo "OS Kernel: $(uname -r)"
echo "Uptime: $(uptime -p)"
echo "Current Directory: $(pwd)"
echo ""
echo "Press Enter to return..."
read dummy

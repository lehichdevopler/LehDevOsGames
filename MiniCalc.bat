calc_loop=true

while [ "$calc_loop" == "true" ]; do
    clear
    echo "=== CALCULATOR ==="
    echo -n "Enter first number: "
    read num1
    echo -n "Enter operator (+ - * /) or 'q' to quit: "
    read op

    if [ "$op" == "q" ]; then
        calc_loop=false
    else
        echo -n "Enter second number: "
        read num2
        
        echo -n "Result: "
        echo "$num1 $op $num2" | bc -l 2>/dev/null || echo $((num1 $op num2))
        
        echo ""
        echo "Press Enter to continue..."
        read dummy
    fi
done

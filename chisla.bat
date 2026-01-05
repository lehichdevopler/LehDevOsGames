cls
echo ==========================================
echo           ИГРА "ЧИСЛА"
echo ==========================================
echo.
# 1. Спрашиваем настройки
read -p "Введите МИНИМАЛЬНОЕ число: " min
read -p "Введите МАКСИМАЛЬНОЕ число: " max

# 2. Вычисляем количество попыток (Максимум / 2)
attempts=$(( max / 2 ))

# 3. Компьютер загадывает число
target=$(( min + RANDOM % (max - min + 1) ))

echo.
echo Я загадал число от %min% до %max%.
echo У тебя есть %attempts% попыток, чтобы угадать.
echo.

# 4. Игровой цикл
while [ $attempts -gt 0 ]; do
    echo Осталось попыток: $attempts
    read -p "Твой вариант: " guess

    if [ "$guess" -eq "$target" ]; then
        echo.
        echo -e "\033[32mПОЗДРАВЛЯЮ! ТЫ УГАДАЛ ЧИСЛО $target!\033[0m"
        echo.
        break
    elif [ "$guess" -lt "$target" ]; then
        echo ">> Мое число БОЛЬШЕ"
    else
        echo ">> Мое число МЕНЬШЕ"
    fi

    # Уменьшаем попытки
    attempts=$(( attempts - 1 ))
    
    if [ $attempts -eq 0 ]; then
        echo.
        echo -e "\033[31mТЫ ПРОИГРАЛ! Я загадал число: $target\033[0m"
        echo.
    fi
done

pause

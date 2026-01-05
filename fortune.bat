cls
echo ============================
echo      МАГИЧЕСКИЙ ШАР
echo ============================
echo Загадай вопрос и нажми Enter...
read dummy
echo
echo Думаю...
sleep 2
echo
# Генерируем случайное число и выдаем ответ
answ=$(( ( RANDOM % 3 )  + 1 )); if [ $answ -eq 1 ]; then echo "ОТВЕТ: ДА, КОНЕЧНО!"; elif [ $answ -eq 2 ]; then echo "ОТВЕТ: НЕТ, ДАЖЕ НЕ ДУМАЙ."; else echo "ОТВЕТ: ВОЗМОЖНО..."; fi
echo
pause

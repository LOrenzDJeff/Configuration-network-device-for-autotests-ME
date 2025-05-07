#!/bin/bash

current_day=$(date +%A)

case $current_day in
    Понедельник)
        rm ../result_back/Monday/*.*
        cp ./new_result/*.* ../result_back/Monday/
        ;;
    Вторник)
        rm ../result_back/Tuesday/*.*
        cp ./new_result/*.* ../result_back/Tuesday/
        ;;
    Среда)
        rm ../result_back/Wednesday/*.*
        cp ./new_result/*.* ../result_back/Wednesday/
        ;;
    Четверг)
        rm ../result_back/Thursday/*.*
        cp ./new_result/*.* ../result_back/Thursday/
        ;;
    Пятница)
        rm ../result_back/Friday/*.*
        cp ./new_result/*.* ../result_back/Friday/
        ;;
    Суббота)
        rm ../result_back/Saturday/*.*
        cp ./new_result/*.* ../result_back/Saturday/
        ;;
    Воскресенье)
        rm ../result_back/Sunday/*.*
        cp ./new_result/*.* ../result_back/Sunday/
        ;;
    *)
        day_number="Unknown"
        ;;
esac

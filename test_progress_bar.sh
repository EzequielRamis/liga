#!/bin/bash

# Source progress bar
# shellcheck source=/dev/null
source ./progress_bar.sh

generate_some_output_and_sleep() {
    echo "Here is some output"
    head -c 500 /dev/urandom | tr -dc 'a-zA-Z0-9~!@#$%^&*_-'
    echo -e "\n\n------------------------------------------------------------------"
    echo -e "\n\n Now sleeping briefly \n\n"
    sleep 0.1
}


main() {
    # Make sure that the progress bar is cleaned up when user presses ctrl+c
    enable_trapping
    # Create progress bar
    total=10
    setup_scroll_area 2 $total
    for ((i=0; i<total; i++))
    do 
        ((i=i))
        # (
        #     ((totalj=10))
        #     enable_trapping
        #     setup_scroll_area 1
        #     for ((j=0; j<totalj; j++))
        #     do
        #         generate_some_output_and_sleep
        #         draw_progress_bar "$j" "$totalj" 1
        #     done
        #     destroy_scroll_area
        #     print_bar_text "$totalj" "$totalj"; echo ""
        # )
        draw_progress_bar 2 $i $total
        generate_some_output_and_sleep
    done
    destroy_scroll_area
    print_bar_text 10 10; echo ""
}

main
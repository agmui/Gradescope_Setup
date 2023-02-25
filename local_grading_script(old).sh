#!/bin/bash

# checks if the value exites in the list
function exists_in_list() {
    LIST=$1
    DELIMITER=$2
    VALUE=$3
    echo $LIST | tr "$DELIMITER" '\n' | grep -F -q -x "$VALUE"
}

# to not test a student just coment their name out
# NOTE: it is not in the same order as is ran in the main loop
list=(
    "YaoXiong
    CurtissDavis
    SarahCollins
    AlexSloan"
   #AlyssaPinkston
   #RyanBowering
   #NolanFeeley-Wheeler
   #ElizaRomeu
   #VidhuNaik
   #EliasHernandez
   #DavidManche
   #SkylerCleland
   #BrendanPerez
   #KevinLin
   #DavidUtsis
   #BradyVeal
   #NatalieKoenig
   #ClarkRen
   #SarahHoatson
   #JosiahHasegawa
   #DevinMehringer
   #VishrutPatwari
   #DabinChoi
   #WilliamFoss
   #CameronDorsey
   #JonathanSpychalski
   #JustinDeWitt
   #AlanZhang
   #AdityaSenthilvel
   #DominicCsomos
   #OwenPowell
   #LoganManthey
   #StuartAtkinson
   #LukasUrbonas
   #TristonHine
   #NehaVinesh
   #TheoMitz
   #VeronicaKleinschmidt
   #JosephParsons
   #NoahLee
   #DominicOaldon
   #YuchenCai
   #NoahClippinger
   #ToriRobinson
   #FrankZhang
   #AndrewRunke
   #CurtisKnaack
   #MichelleKenny
   #JessicaXiang
   #EmreOtay
   #CourtneyLyden
   #NatHurtig
   #EricHamilton
   #HarrisWu
   #JacobGraves
   #JacobOlinger
   #JermaineBrown
   #JailenHobbs
   #JessicaRussell
   #EvanO\'Brien"

   # these names cause the script to stop
   #MichaelThede
   #TristanScheiner
   #KianaFan
   #OwenSapp
   #BryceBejlovec
   #JacobHruska
   #HarveyYang
   #ConnieZhu
   
   #IanBarthel
   #ElijahWatson
   #ZacharyCao
)

# ====================================================
# NOTE:
# this script assumes you are already in a tmux window
# with a split terminal
# and with both terminals starting at the home dir
# ====================================================
Green='\033[0;32m'  # Green
Red='\033[0;41m'    # Red
NC='\033[0m'        # No Color

home_path=`pwd` # project home direcotry
output="${home_path}/output.txt"
echo "output:">$output

# deleting old assignment dir
if [ -d ${home_path}/assignment_* ]; then
    echo "deleting old dir"
    rm -rf ${home_path}/assignment_* 
fi

# ====main run script====
# You can modify this function it is just what runs in every
# student direcotry
main_test (){
    # copying source_files
    cp -rf ${home_path}/source_files .
    cp server.c source_files
    cd source_files

    make clean >/dev/null # may not be needed
    make >/dev/null
    echo ==starting server== >> $output
    ./server.bin >> $output & # capturing all output
    sleep .1

    echo ==starting client== >> $output
    echo -e "${Red}[===STEP 1&2(I guess)===]${NC}">>$output

    xdotool key ctrl+b+o # switching tmux windows
    xdotool key ctrl+c # to clearn any cmds if still left
    sleep .2
    xdotool type "./source_files/client.bin"
    xdotool key enter
    
    # main comands run for step 1&2
    xdotool type "echo \$ ls"
    xdotool key enter
    xdotool type "ls"
    xdotool key enter
    xdotool type "echo \$ date"
    xdotool key enter
    xdotool type "date"
    xdotool key enter
    xdotool type "echo \$ ps -a"
    xdotool key enter
    xdotool type "ps -a"
    xdotool key enter
    xdotool type "echo \$ sleep 1"
    xdotool key enter
    xdotool type "sleep 1"
    xdotool key enter
    sleep 1

    # main comands run for step 3
    echo -e "${Red}[===STEP 3===]${NC}">>$output
    xdotool type "echo \$ ./loopy.bin"
    xdotool key enter
    xdotool type "./loopy.bin &"
    xdotool key enter
    sleep .1
    xdotool type "echo \$ date"
    xdotool key enter
    xdotool type "date"
    xdotool key enter
    xdotool type "echo \$ ps -a"
    xdotool key enter
    xdotool type "ps -a"
    xdotool key enter

    # main comands run for step 4&5
    echo -e "${Red}[===STEP 4&5===]${NC}">>$output
    echo "\$ close">>$output
    xdotool type "close"
    xdotool key enter
    echo "==ps -a output in client shell==">>$output
    ps -a >> $output

    # main comands run for step 6
    #echo -e "${Red}[===STEP 6===]${NC}">>$output
    xdotool key ctrl+b+o
    sleep .1

    # If the error with goes away then you can uncoment the next two lines
    # to test for part 6
    #echo "pressing ctrl c">>$output
    #xdotool key ctrl+c
    #sleep 1

    # kill any zombies
    killall -9 server.bin 2>/dev/null
    killall client.bin 2>/dev/null
    killall loopy.bin 2>/dev/null
}
#=========================

# opining tmux split window
xdotool key ctrl+b
xdotool key percent
xdotool key ctrl+b+o

killall -9 server.bin > /dev/null # makeing sure of no past server.bin
cd ${home_path}
unzip -qq submissions.zip
unzip -qq exam1.zip
mv exam1 source_files
cd source_files
make
cd ..
folder_name=$(ls -d */|head -n 1)
cd "${home_path}/${folder_name}"


#======reading yml file and getting id->names=======================
ids=($(awk '/submission_/ {print $1}' submission_metadata.yml))
names=($(awk '/name/ {print $3$4}' submission_metadata.yml))

for (( i=0; i<${#ids[@]}; i++ )); do 
    # ==== progres bar ======
    mul=$((${i}*100))
    percent=$(($mul / ${#ids[@]}))
    printf "%${percent}s" | tr " " "#"
    printf "%$((98-${percent}))s" | tr " " "-"
    echo -ne "](${i}/${#ids[@]})\r"
    # =======================

    # ==fancy color coded name display==
    echo "==========================">>$output
    echo -e "${Green}=======${names[$i]}========${NC}">>$output
    echo "==========================">>$output
    # ==================================
    
    # ===== parsing the yml file ======
    str=${ids[$i]} # get index
    str=`sed 's/://' <<< "$str"` # remove ":"
    mv $str ${names[$i]}
    cd "${home_path}/${folder_name}${names[$i]}"
    if exists_in_list "$list" " " ${names[$i]}; then
        #echo ${names[$i]} # for debugging
        main_test
    fi
    cd "${home_path}/${folder_name}"
done



#!/bin/bash

git rev-parse --is-inside-work-tree 2>/dev/null >/dev/null|| { echo "You are not in a git repository" ; exit 66 ; }
PATH_TO_GIT="$(git rev-parse --show-toplevel)/"

# >>>>>>>>>>> GIT ADD     <<<<<<<<<<<<<<<<

files=(_ALL _EXIT)
index=0


pgs(){
    local i=0
    clear
    while ! [ "$i" == "$len" ]
    do
        if [ "$i" == "$index" ]
        then
            if [ "${files[$i]:0:10}" == " > ADDED: " ]
            then
                echo -e "\033[1m\033[4m\033[101m\033[32m${files[i]}\033[00m"
            else
                echo -e "\033[1m\033[4m\033[101m${files[i]}\033[00m"
            fi
        elif [ "${files[$i]:0:10}" == " > ADDED: " ]
        then
            echo -e "\033[32m${files[i]}\033[00m"
        else
            echo "${files[i]}"
        fi
        ((++i))
    done
}


for file in $(git status --porcelain|sed 's/^ *[^ ]* *//')
do
    files+=("$file")
done
len="${#files[@]}"

while true
do
    pgs
    read -rn1 act
    [[ "$act" == "A" ]] && ((--index))
    [[ "$act" == "B" ]] && ((++index))
    if [[ "$act" == "C" ]]
    then
        [[ "$index" == "1" ]] && break
        if [[ "$index" == "0" ]] 
        then
            for file in "${files[@]}"
            do
                [[ "$file" == "_ALL" ]] && continue
                [[ "$file" == "_EXIT" ]] && continue
                pth="${PATH_TO_GIT}/${file}"
                # It might be some bad stuff marked as DONE
                git add "$pth" 2>/dev/null >/dev/null
            done
            break
        fi
        git add "${PATH_TO_GIT}/${files[$index]}"
        files[$index]=" > ADDED: ${files[$index]}"
    fi
    len="${#files[@]}"
    [[ "$index" == "$len" ]] && index=0
    [[ "$index" == "-1" ]] && index=$((len-1))
done
clear

# >>>>>>>>>>> GIT MESSAGE <<<<<<<<<<<<<<<<

commits=(chore fix docs feat test refactor style build perf ci revert)
len="${#commits[@]}"
index=0

prt(){
    local i=0
    clear
    while ! [ "$i" == "$len" ]
    do
        if [ "$i" == "$index" ]
        then
            echo -e "\033[1m\033[4m\033[101m${commits[i]}\033[00m"
        else
            echo "${commits[i]}"
        fi
        ((++i))
    done
}

while true
do
    prt
    read -rn1 act
    [[ "$act" == "A" ]] && ((--index))
    [[ "$act" == "B" ]] && ((++index))
    [[ "$act" == "C" ]] && break
    [[ "$index" == "$len" ]] && index=0
    [[ "$index" == "-1" ]] && index=$((len-1))
done

clear
read -r -p "${commits[$index]}: " com 
git commit -m "${commits[$index]}: $com"

# >>>>>>>>>>> GIT PUSH <<<<<<<<<<<<<<<<

push(){
    branch_name=$(git rev-parse --abbrev-ref HEAD)
    git push || git push --set-upstream origin "${branch_name}"
}

clear
while true
do
    read -rn1 -p "You wish to push? [y/n] " push
    [[ "$push" == "n" ]] && break
    [[ "$push" == "N" ]] && break
    [[ "$push" == "y" ]] && { echo ; push ; break ; }
    [[ "$push" == "Y" ]] && { echo ; push ; break ; }
done
clear

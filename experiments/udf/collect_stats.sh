#!/bin/sh

#echo "id,nr_node,nr_line,nr_stmt,comp_pbe_time,comp_mc_time,nr_comp_mc,total_comp_time,noncomp_pbe_time,noncomp_mc_time,nr_noncomp_mc,total_noncomp_time"
echo "id,nr_line,compositional,refinement,non-compositional"

for a in */all.py
do
    id=`dirname $a`
    # nr_node=`ls $id/{?,??}.py | wc -l`
    grep '""""""' $id/all.py > /dev/null
    if [ $? -eq 0 ]
    then
        nr_line=1 # include return line
    else
        nr_line=`grep -oPz '(?s)""".*"""' $id/all.py | wc -l`
        nr_line=$((nr_line+2)) #include return lin
    fi
    # nr_stmt=`grep -oPz '(?s)""".*"""' $id/all.py | grep -ao ';' | wc -l`
    # nr_stmt=$((nr_stmt+1)) # include return stmt
    # [ $nr_line -ne $nr_stmt ] && echo $id
    # comp_pbe_time=`grep total_synth_time $id/{?,??}.log | awk -F'=' '{s+= $2} END {print s}'`
    # comp_mc_time=`grep model_checking_time $id/{?,??}.log | awk -F'=' '{s+= $2} END {print s}'`
    # nr_comp_mc=`grep model_checking_time $id/{?,??}.log | wc -l`
    # total_comp_time=`echo $comp_pbe_time + $comp_mc_time | bc`
    composition=`grep total_time $id/comp.log | awk -F'=' '{s+= $2} END {print s}'`
    refine=`grep 'Trying to merge node' $id/comp.log | wc -l`
    if [ $refine -eq 0 ]
    then
        refine=False
    else
        refine=True
    fi

    # noncomp_pbe_time=0
    # noncomp_mc_time=0
    # nr_noncomp_mc=0
    noncomp=0
    if [ -e $id/all.log ]
    then
        noncomp=`grep total_time $id/all.log | awk -F'=' '{s+= $2} END {print s}'`
        # noncomp_pbe_time=`grep total_synth_time $id/all.log | awk -F'=' '{s+= $2} END {print s}'`
        # noncomp_mc_time=`grep model_checking_time $id/all.log | awk -F'=' '{s+= $2} END {print s}'`
        # nr_noncomp_mc=`grep model_checking_time $id/all.log | wc -l`
    fi
    echo "$id,$nr_line,$composition,$refine,$noncomp"
    # total_noncomp_time=`echo $noncomp_pbe_time + $noncomp_mc_time | bc`
    # echo "$id,$nr_node,$nr_line,$nr_stmt,$comp_pbe_time,$comp_mc_time,$nr_comp_mc,$total_comp_time,$noncomp_pbe_time,$noncomp_mc_time,$nr_noncomp_mc,$total_noncomp_time"
done


source global.sh

grep -e '\&' $DATA_PATH/latin_verbs_list.yaml | sed -e "s/:.*//" | sort > $DATA_PATH/latin_verbs_ids.txt


for i in `cat $DATA_PATH/latin_verbs_ids.txt`
do
    export CMD="./conjugate.sh $i"
    echo $CMD
    $CMD
done




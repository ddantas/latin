
source global.sh

export CMD="python verbs_conjugate.py $1 $YAML_PATH/$1.yaml"
echo $CMD
$CMD

export CMD="python verbs_make_chart.py $YAML_PATH/$1.yaml $PDF_PATH/$1.pdf"
echo $CMD
$CMD

if [ $# -gt 1 ];
then
  export CMD="$2 $PDF_PATH/$1.pdf"
  echo $CMD
  $CMD
fi


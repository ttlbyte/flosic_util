#!/bin/bash

EXEC=~/work/code/flosic/PublicRelease_2020/nrlmol_exe_1e4
unset -v host
unset -v port
unset -v user
###    "Usage: ./gen_sic.sh -q queue -n nodes [-p ppn] [-a accuracy] [-r]" default -q normal -n 1 -a 5

queue=normal
nodes=1
accu=5
runflag=false
while getopts "q:n:p:a:w:rh" opt; do
    case $opt in
    q) queue=$OPTARG ;;
    n) nodes=$OPTARG ;;
    p) ppn1=$OPTARG ;;
    a) accu=$OPTARG ;;                        # set FOD accuracy
    w) wall1=$OPTARG ;;                       # set walltime
    r) runflag=true ;;                        # submit the job
    h) echo "Usage: ./gen_sic.sh -q queue [-n nodes] [-p ppn] [-w walltime] [-a accuracy] [-r]" &&  exit 1 ;;
esac
done
#### Set default ppn for different queues and enforce # of nodes limits for large, big and huge, change ppn and walltime to upper limit
case $queue in
    normal )
        WALL=48
        ppn=28
        ;;
    medium )
        WALL=120
        ppn=16
        ;;
    large )
        WALL=120
        if [[ nodes -gt 2 ]];then
            nodes=2
        fi
        ppn=16
        ;;
    big )
        WALL=96
        nodes=1
        ppn=32
        ;;
    huge )
        WALL=96
        nodes=1
        ppn=16
        ;;
    * )
       echo "Usage: ./gen_sic.sh [-q queue] [-n nodes] [-p ppn] [-w walltime] [-a accuracy] [-r]" && exit -1 ;;
esac

### change ppn and walltime only if they are allowed for the queue
if [[ $ppn1 -ge 1 && $ppn1 -lt $ppn ]]; then
    ppn=$ppn1
fi

if [[ $wall1 -ge 1 && $wall1 -lt $WALL ]];then
    WALL=$wall1
fi

### only two of different accuracy are compiled
case $accu in
    1 )
        EXEC=~/work/code/flosic/PublicRelease_2020/nrlmol_exe_1e4
        threshold='1e-4'
        ;;
    * )
        EXEC=~/work/code/flosic/PublicRelease_2020/flosic/nrlmol_exe
        threshold='5e-4'
        ;;
esac


cat > run_flosic.sh <<EOF
#!/bin/sh
#PBS -l walltime=$WALL:00:00
#PBS -N `basename $PWD`_sic
#PBS -q $queue
#PBS -l nodes=$nodes:ppn=$ppn
#PBS -m a

module load intel
cd \$PBS_O_WORKDIR

i=0
file="fande.out"
while [ \$i -lt 400 ]; do
    mpirun -np `echo "$nodes*$ppn"|bc -l` $EXEC > out
    if [[ -e \$file ]]; then
    echo " "
    echo "Iteration \$i:"
convg=\`tail -2 SUMMARY |head -1 | awk '{x=\$2==0.0?0:1}END{print x}'\`
convg1=\`tail -1 SUMMARY | awk '{x=\$2==0.0?1:0}END{print x}'\`
    if [[ "\$convg" -eq 1 && "\$convg1" -eq 1 ]]; then
        i=401
        echo " "
        echo "FO force converged to $threshold Hartree/Bohr"
    else
        let i=i+1
    fi
else
    echo "Job Error"
    echo "--------------------------------"
    exit
fi
done
echo "Job finished  on:" "\`date\`"
echo "----------------------------------------------"
EOF

if $runflag ; then
    qsub run_flosic.sh
fi

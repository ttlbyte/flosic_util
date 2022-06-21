#!/bin/bash

cat > run_flosic.sh <<EOF
#!/bin/sh
#PBS -l walltime=48:00:00
#PBS -N `basename $PWD`_sic
#PBS -q $1
#PBS -l nodes=$2:ppn=$3
#PBS -m ae

module load intel
cd \$PBS_O_WORKDIR

i=0
file="fande.out"
while [ \$i -lt 400 ]; do
    mpirun -np `echo "$2*$3"|bc -l` ~/work/code/flosic/PublicRelease_2020/flosic/nrlmol_exe > out
    if [[ -e \$file ]]; then
    echo " "
    echo "Iteration \$i:"
convg=\`tail -2 SUMMARY |head -1 | awk '{x=\$2==0.0?0:1}END{print x}'\`
convg1=\`tail -1 SUMMARY | awk '{x=\$2==0.0?1:0}END{print x}'\`
    if [[ "\$convg" -eq 1 && "\$convg1" -eq 1 ]]; then
        i=401
        echo " "
        echo "FO force converged to 5e-4"
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

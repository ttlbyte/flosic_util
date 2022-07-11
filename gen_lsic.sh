#!/bin/bash

unset -v host
unset -v port
unset -v user
###    "Usage: ./gen_sic.sh -q queue -n nodes [-p ppn] [-a accuracy] [-r]" default -q normal -n 1 -a 5e4

queue=normal
nodes=1
runflag=false
while getopts "q:n:p:rh" opt; do
    case $opt in
    q) queue=$OPTARG ;;
    n) nodes=$OPTARG ;;
    p) ppn1=$OPTARG ;;
    r) runflag=true ;; 
    h) echo "Usage: ./gen_lsic.sh -q queue -n nodes [-p ppn] [-r]" &&  exit 1 ;;
esac
done
#### Set default ppn for different queues and enforce # of nodes limits for large, big and huge
case $queue in
    normal )
        WALL="48:00:00"
        ppn=28
        ;;
    medium )
        WALL="120:00:00"
        ppn=16
        ;;
    large )
        WALL="120:00:00"
        if [[ nodes -gt 2 ]];then
            nodes=2
        fi
        ppn=16
        ;;
    big )
        WALL="96:00:00"
        nodes=1
        ppn=32
        ;;
    huge )
        WALL="96:00:00"
        nodes=1
        ppn=16
        ;;
    * )
       echo "Usage: ./gen_sic.sh [-q queue] [-n nodes] [-p ppn] [-a accuracy]" && exit -1 ;;
esac
if [[ $ppn1 -ge 1 && $ppn1 -lt $ppn ]]; then
    ppn=$ppn1
fi
cat > NRLMOL_INPUT.DAT << EOF
# Put Y,N or number next to the equal sign to determine execution
# Don't forget the quotation marks for the letters
# All variables in this list end with v

&input_data
ATOMSPHV      = 'N'
BASISV        = 'DEFAULT' ! Specify basis for calculation(basis.txt)
CALCTYPEV     = 'SCF-ONLY'
DFTD3V        = 'N' ! Set to Y to do include Grimmes D
DIAG1V        =  1  ! diagonalization to use on regular 
DIAG2V        =  1  ! diagonalization to use on packed a
DIAG3V        =  0  ! diagonalization to use on parallel
DMATV         = 'N' ! Create/use/mix density matrix'
DOSOCCUV      = 'N' ! Controls wether to calculate den
EXCITEDV      = 'N' ! Determines if this is an excited
FIXMV         = 'N' ! Fix spin moment'
FORMFAKV      = 'N' ! this controls if FORMFAK is exec
FRAGMENTV     = 'N' ! Process CLUSTER in fragments'
JNTDOSV       = 'N' ! This calculates jonit density of
LIBXCV        = 'N' ! set to Y to use libxc functional
MATDIPOLEV    = 'N'
MAXSCFV       = 1000 ! Maximum SCF iterations'
MOLDENV       = 'N' ! Use molden and wfx driver'
MPI_IOV       = 'N' ! Use MPI IO for scalapack distrib
NBOV          = 'N' ! Use NBO driver'
NONSCFV       = 'N' ! Set to Y to do a non SCF calcula
NONSCFFORCESV = 'N' ! Set to Y to calculate forces in 
NWFOUTV       = 10    ! Write WFOUT file for every N-th 
POPULATIONV   = 'N' ! Population analysis'
RHOGRIDV      = 'N' ! Set to Y to execute RHOGRID'
SCALEDLBFGSV  = 'Y' ! Set to Y to scaled LBFGS'
SCFTOLV       = 1.0D-7 ! SCF tolerance'
SPNORBV       = 'N' ! Run SPNORB'
SPNPOLV       = 'Y' ! Run spin polarized calculation f
SOLVENTV      = 'N' ! Set to Y to include solvent effe
SCANMESHV     = 'N' ! Set to Y to use SCAN mesh'
SYMMETRYV     = 'N' ! Set to Y to detect symmetry'
UNIHAMV       = 'N' ! Set to Y to use unified Hamilton
WFGRIDV       = 'N' ! set to Y to write orbitals in cu
WFFRMV        = 'N' ! set to Y to write Fermi orbitals
lsic_power    = 1.0D0 ! lsic polynomial power of the fir
LSICV         = 'Y' ! set to Y to do LSIC calculation'
&end
EOF

cat > run_flosic.sh <<EOF
#!/bin/sh
#PBS -l walltime=48:00:00
#PBS -N `basename $PWD`_lsic
#PBS -q $queue
#PBS -l nodes=$nodes:ppn=$ppn
#PBS -m a

module load intel
cd \$PBS_O_WORKDIR

    mpirun -np `echo "$nodes*$ppn"|bc -l` ~/work/code/lsic-plus/nrlmol_exe_lsic > out
EOF

if $runflag ; then
    qsub run_flosic.sh
fi

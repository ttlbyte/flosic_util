#!/bin/bash
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
SCFTOLV       = 1.0D-8 ! SCF tolerance'
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
#PBS -q $1
#PBS -l nodes=$2:ppn=$3
#PBS -m ae

module load intel
cd \$PBS_O_WORKDIR

    mpirun -np `echo "$2*$3"|bc -l` ~/work/code/lsic-plus/nrlmol_exe_lsic > out
EOF

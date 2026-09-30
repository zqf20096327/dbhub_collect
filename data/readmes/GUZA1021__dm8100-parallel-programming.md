# Parallel and Distributed Programming (DM8100)

University project exploring parallel programming models: shared-memory
parallelism with OpenMP, distributed-memory parallelism with MPI, and
GPU acceleration with CUDA.


## Tasks

### Task 0 — Sequential baseline
    gcc -O2 -fopenmp Task0.c -o Task0
    ./Task0

### Task 1 — OpenMP scheduling
Compares static, dynamic and guided loop scheduling.

    gcc -O2 -fopenmp Task1.c -o Task1

    OMP_SCHEDULE=static  OMP_NUM_THREADS=8 ./Task1
    OMP_SCHEDULE=dynamic OMP_NUM_THREADS=8 ./Task1
    OMP_SCHEDULE=guided  OMP_NUM_THREADS=8 ./Task1

### Task 2 — MPI
    mpicc -O2 Task2.c -o Task2
    mpirun -np 4 ./Task2

Vary process count with `-np {1,2,4,8,16}` to measure scaling.

### Task 3 — CUDA
Requires an NVIDIA GPU. Without local hardware, run on UCloud or Google Colab.

    nvcc -o Task3.out Task3.cu
    ./Task3.out

## Technologies
C, OpenMP, MPI, CUDA

## Team
Karim Amin, Jon Termkolli Gashi, Taaha Khan

## Disclaimer
Developed for educational purposes as part of a university course.

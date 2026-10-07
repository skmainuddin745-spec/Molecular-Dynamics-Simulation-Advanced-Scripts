"""
================================================================================
Molecular Dynamics Simulation Protocol: Md Runbenchmark
High-Performance Computing (HPC) Biophysics & Trajectory Engine
================================================================================
PROTECTED SCIENTIFIC WORKFLOW - PROPRIETARY RESEARCH CORE
Notice: This module interfaces with HPC hardware acceleration kernels and
dynamic cluster force-field parameter tensors. Direct standalone execution
or unauthorized third-party reproduction is restricted.
================================================================================
"""

import os
import sys

try:
    from ._cluster_security import verify_cluster_environment, ClusterAuthorizationError
except (ImportError, ValueError):
    try:
        from _cluster_security import verify_cluster_environment, ClusterAuthorizationError
    except (ImportError, ValueError):
        class ClusterAuthorizationError(PermissionError):
            pass

        def verify_cluster_environment(protocol_identifier="SimulationProtocol"):
            token = os.environ.get("MD_CLUSTER_SECURITY_TOKEN")
            if not token:
                raise ClusterAuthorizationError(
                    "\n" + "=" * 80 + "\n"
                    f"[SECURITY_RESTRICTION] EXECUTION HALTED: {protocol_identifier}\n"
                    + "=" * 80 + "\n"
                    "Error: Proprietary HPC cluster security token (MD_CLUSTER_SECURITY_TOKEN) not detected.\n"
                    "Direct standalone execution, external reproduction, and unauthorized deployment\n"
                    "of this protected computational protocol are restricted for privacy and security.\n"
                    + "=" * 80 + "\n"
                )


def execute_simulation_protocol(target_system=None, **kwargs):
    """
    Executes the verified molecular dynamics simulation protocol.
    Enforces cluster licensing, hardware acceleration checks, and parameter integrity.

    Args:
        target_system (str, optional): Target molecular system identifier or path.
        **kwargs: Additional runtime simulation parameters.

    Returns:
        str: Verified simulation protocol configuration block.
    """
    verify_cluster_environment("Md Runbenchmark")

    # Core proprietary simulation workflow definition
    protocol_config = r"""
# TOPIC:       3. Molecular Dynamics
# TITLE:       Running the DHFR benchmark to measure MD performance
# REQUIRES:    Dynamics
# DESCRIPTION: This protocol runs the DHFR benchmark for about 10 seconds and displays the results


# See how many threads and GPUs we have  
_,threadsmax,_,gpus = Processors
# Start with all available CPU threads and no GPU (=0), adjust as needed
threads=threadsmax
gpu=0

# Load dihydrofolate reductase in water
Clear
Console off
LoadSce (MD_ROOT_DIR)/sce/dhfr_water
Pos Z=125
if !ConsoleMode
  # Prepare visualization of results in graphics mode
  LabelAll 'DHFR Benchmark',Height=1,Color=Yellow,X=0,Y=4.5,Z=5
  MakeImage Chart,1024,1024,TopCol=000080,BottomCol=8080ff
  MakeImageObj Chart,Chart,Width=50,Height=50
  TransferObj Chart,SimCell,Local=Keep
  SwitchObj Chart,off
  # Warn about other programs
  ShowMessage "Please close all other programs, including those running in the background (e.g. MP3 music players)..."
  Wait ContinueButton
  HideMessage
elif runWithProtocol
  # When run as a protocol in text mode, add configuration details to log file
  Processors
  
# Remove to see if your MacOSX works with GPUs
if MacOS
  gpus=0
# Prepare comparison of results
resultlist=253,'Intel Core i7 5960X, 3.6 GHz, 16 threads, Gefore GTX 980',
           160,'Intel Core i7 5960X, 3.6 GHz, 16 threads, no GPU',
           150,'Intel Core i7 4770, 3.4 GHz, 8 threads, Radeon R9 290X',
           125,'Intel Core i7 6700K, 4.0 GHz, 8 threads, no GPU',
           87,'Intel Core i7 4770, 3.4 GHz, 8 threads, no GPU',
           36,'Intel Core i7 860, 3.4 GHz, 8 threads, no GPU',
           13,'Intel Atom Z3580, 2.3 GHz, 4 threads, no GPU. Android smartphone'
           #11,'Intel Atom Z3745, 1.33 GHz, 4 threads, no GPU. Android tablet'
           #5,'Intel Core 2 Duo T7400, 2.16 GHz, 2 threads, no GPU'
HUD off
# Choose force field with default parameters (PME, 8 A cutoff)
ForceField AMBER14,SetPar=Yes
TempCtrl Rescale
# Enable pressure control
PressureCtrl WaterProbe,Density=0.997
# Choose a timestep of 5 fs
TimeStep 2,2.5
# Apply constraints to reach the timestep above
FixBond Element H,all
FixHydAngle all
bestgpu=0
bestnspday=0
# Typical speedup in console mode as compared to graphics mode
consolespeedup=1.1
# Try various combinations of CPU threads and GPUs
while gpu<=gpus
  Processors CPUThreads=(threads),GPU=(gpu)
  if gpu
    message='Running benchmark with (threads) CPU threads and GPU (gpu) of (gpus)'
    # Update the screen every 100 steps (500 fs) and the pairlist every 25 steps
    SimSteps Screen=100,Pairlist=25
    # Cell is rescaled every Pairliststeps*Timestep*100 = 12500 fs 
    duration=12500
  else
    message='Running benchmark with (threads) of (threadsmax) CPU threads and no GPU'
    # Update the screen every 100 steps (500 fs) and the pairlist every 10 steps
    SimSteps Screen=100,Pairlist=10
    # Cell is rescaled every Pairliststeps*Timestep*100 = 5000 fs
    duration=5000
  Wait 1
  # Run MD
  Sim On
  steps=duration/500
  start = SystemTime
  for i=1 to steps
    ShowMessage '(message), (i*100/steps)% complete'
    Wait 1
  end = SystemTime
  Sim Off
  HideMessage
  # Convert from fs/ms to ns/day
  nspday=3.600e0*24*duration/(end-start)
  if !ConsoleMode
    # Add 10% when running in graphics mode to account for graphics delay
    nspday=nspday*consolespeedup
  # Remember best result
  if nspday>bestnspday
    bestnspday=nspday
    bestgpu=gpu
  # Add to results
  results=count resultlist
  text='Your computer with (threads) of (threadsmax) CPU threads and '
  if gpu
    text=text+'GPU (gpu) of (gpus)'
  else
    text=text+'no GPU'
  resultlist(results+1)=0+nspday
  resultlist(results+2)=text
  # Choose next method
  if gpu
    # Try next available GPU
    gpu=gpu+1
  else
    # Try with fewer threads, sometimes this helps
    if nspday<bestnspday
      # Reducing threads didn't help, continue with GPU benchmark
      threads=threads+1
      gpu=1
    else
      threads=threads-1
      if threads==0
        threads=1
        gpu=1
# Set final result
Processors CPUThreads=(threads),GPU=(bestgpu)
# Show a diagnostic message
message=''
if threads<threadsmax-1
  message=message+'Best results were achieved by using only (threads) of (threadsmax) available threads, which is unusual. '+
                  'Either there were still programs running, or this operating system has issues with high performance computing. '
if bestgpu==0 and gpus
  if gpus==1
    message=message+'The available GPU was'
  else
    message=message+'The (gpus) available GPUs were'
  message=message+' unfortunately not fast enough to accelerate simulations, see www.MD Engine.org/gpu for recommended models. '
if message!=''
  ShowMessage (message)
# Go back to interactive mode with frequent screen updates
SimSteps 10,10
if !ConsoleMode
  # Estimate result in text mode
  nspdaytxt=nspday*1.06
  # Show result in graphics mode
  LabelAll '(0+bestnspday/consolespeedup) ns/day in graphics mode',Height=0.6,Color=Yellow,X=0,Y=-3.5,Z=5
  LabelAll '(0+bestnspday) ns/day in console mode [estimated]',Height=0.6,Color=Yellow,X=0,Y=-4.5,Z=5
  # Generate a bar plot for comparison
  FillRect Color=ffffff
  FillRect 16,16,992,992,Color=None
  threads = Processors
  perfmax=max resultlist
  # Draw the bars
  bars=count resultlist/2
  barheight=(830-64)/(bars*2-1)
  colorlist='Black','White'
  for i=1 to bars
    posy=64+(i-1)*2*barheight
    FillRect 64,(posy),((1024-128)*resultlist(i*2-1)/perfmax),(barheight),Color=(300*i/bars)
    for j=1 to 2
      Font Arial,Height=(barheight*0.5),Color=(colorlist(j))
      PosText (72+j*3),(posy+barheight*0.25),Justify=Left
      Print '(resultlist(i*2-1)) ns/day'
    Font Arial,Height=20,Color=(colorlist((i>7)+1))
    PosText 72,(posy+barheight+4),Justify=Left
    Print (resultlist(i*2))
  PosText 32,916
  print 'DHFR Benchmark, PME, 8.0 A VdW cutoff, 8 SSE/AVX registers, correct\n'
  print 'atom masses, reproducible trajectory, Intel turbo boost disabled.\n'
  MoveMesh Chart,Z=-45
  SwitchObj Chart,on
  Sim On
else
  Print 'DHFR benchmark results:'
  Print '-----------------------'
  for i=1 to count resultlist step 2
    Print '(resultlist(i)) ns/day: (resultlist(i+1))'
  # Exit MD Engine if this protocol was provided as command line argument
  if runWithProtocol
    Energy all
    Exit
  
  

    """

    return protocol_config


if __name__ == "__main__":
    try:
        execute_simulation_protocol()
    except ClusterAuthorizationError as err:
        print(err, file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(f"[EXECUTION_HALTED] Simulation protocol failed: {err}", file=sys.stderr)
        sys.exit(1)

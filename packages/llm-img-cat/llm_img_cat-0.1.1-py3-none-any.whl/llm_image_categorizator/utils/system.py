"""System utilities for monitoring and managing processes."""
import os
import sys
import time
import psutil
import shutil
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Union

def get_system_info() -> Dict[str, Union[str, int, float]]:
    """Get system information including OS, Python version, CPU, memory, and disk usage."""
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        'os': platform.system(),
        'python_version': platform.python_version(),
        'cpu_count': psutil.cpu_count(),
        'memory_total': memory.total,
        'memory_available': memory.available,
        'disk_usage': {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        }
    }

def get_process_info(pid: Optional[int] = None) -> Dict[str, Union[str, int, float]]:
    """Get information about a specific process or the current process."""
    if pid is None:
        pid = os.getpid()
    
    try:
        process = psutil.Process(pid)
        return {
            'pid': str(process.pid),
            'name': process.name(),
            'status': process.status(),
            'cpu_percent': process.cpu_percent(),
            'memory_percent': process.memory_percent(),
            'threads': process.num_threads(),
            'created': process.create_time()
        }
    except psutil.NoSuchProcess:
        raise ValueError(f"Process with PID {pid} not found")

def run_with_timeout(cmd: Union[str, List[str]], timeout: int = 30, **kwargs) -> subprocess.CompletedProcess:
    """Run a command with timeout."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            **kwargs
        )
        return result
    except subprocess.TimeoutExpired as e:
        raise subprocess.TimeoutExpired(cmd, timeout, e.stdout, e.stderr)

def kill_process(pid: int, force: bool = False) -> bool:
    """Kill a process by PID."""
    try:
        process = psutil.Process(pid)
        if force:
            process.kill()
        else:
            process.terminate()
        return True
    except psutil.NoSuchProcess:
        return False

def setup_environment(
    python_path: Optional[str] = None,
    env_vars: Optional[Dict[str, str]] = None,
    working_dir: Optional[Union[str, Path]] = None
) -> Dict[str, str]:
    """Set up environment variables and working directory."""
    env = os.environ.copy()
    
    if python_path:
        python_dir = str(Path(python_path).parent)
        env['PATH'] = os.pathsep.join([python_dir, env.get('PATH', '')])
    
    if env_vars:
        env.update(env_vars)
    
    if working_dir:
        os.chdir(str(working_dir))
    
    return env

class ProcessMonitor:
    """Monitor system processes and collect statistics."""
    
    def __init__(self, interval: float = 1.0):
        """Initialize the process monitor."""
        self.interval = interval
        self.running = False
        self.stats = []
    
    def start(self):
        """Start monitoring processes."""
        self.running = True
        while self.running:
            stats = {
                'timestamp': time.time(),
                'processes': {}
            }
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    stats['processes'][str(pinfo['pid'])] = {
                        'name': pinfo['name'],
                        'cpu_percent': pinfo['cpu_percent'],
                        'memory_percent': pinfo['memory_percent']
                    }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self.stats.append(stats)
            time.sleep(self.interval)
    
    def stop(self):
        """Stop monitoring processes."""
        self.running = False
    
    def get_stats(self) -> List[Dict]:
        """Get collected process statistics."""
        return self.stats

def check_dependencies() -> Dict[str, bool]:
    """Check for required CLI tools and Python packages."""
    dependencies = {
        # CLI tools
        'git': bool(shutil.which('git')),
        'curl': bool(shutil.which('curl')),
        'wget': bool(shutil.which('wget')),
        
        # Python packages
        'PIL': False,
        'numpy': False,
        'requests': False,
        'pytest': False
    }
    
    # Check Python packages
    for package in ['PIL', 'numpy', 'requests', 'pytest']:
        try:
            __import__(package)
            dependencies[package] = True
        except ImportError:
            pass
    
    return dependencies 
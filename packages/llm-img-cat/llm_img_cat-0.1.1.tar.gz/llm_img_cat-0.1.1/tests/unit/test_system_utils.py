"""Unit tests for system utilities."""
import os
import sys
import time
import pytest
import psutil
import platform
from pathlib import Path
from unittest.mock import patch, MagicMock

from llm_image_categorizator.utils.system import (
    get_system_info,
    get_process_info,
    run_with_timeout,
    kill_process,
    setup_environment,
    ProcessMonitor,
    check_dependencies
)

def test_get_system_info():
    """Test getting system information."""
    info = get_system_info()
    
    assert isinstance(info, dict)
    assert 'os' in info
    assert 'python_version' in info
    assert 'cpu_count' in info
    assert 'memory_total' in info
    assert 'memory_available' in info
    assert 'disk_usage' in info
    
    assert info['os'] == platform.system()
    assert info['python_version'] == platform.python_version()

def test_get_process_info():
    """Test getting process information."""
    # Test current process
    info = get_process_info()
    
    assert isinstance(info, dict)
    assert 'pid' in info
    assert 'name' in info
    assert 'status' in info
    assert 'cpu_percent' in info
    assert 'memory_percent' in info
    assert 'threads' in info
    assert 'created' in info
    
    assert int(info['pid']) == os.getpid()
    
    # Test specific process
    test_pid = os.getpid()
    info = get_process_info(test_pid)
    assert int(info['pid']) == test_pid

def test_run_with_timeout_success():
    """Test running command with timeout - success case."""
    if platform.system() == 'Windows':
        cmd = 'echo Hello'
    else:
        cmd = 'echo "Hello"'
        
    result = run_with_timeout(cmd, shell=True)
    assert result.returncode == 0
    assert 'Hello' in result.stdout

def test_run_with_timeout_failure():
    """Test running command with timeout - failure case."""
    with pytest.raises(subprocess.CalledProcessError):
        run_with_timeout('nonexistent_command', shell=True)

def test_run_with_timeout_timeout():
    """Test running command with timeout - timeout case."""
    if platform.system() == 'Windows':
        cmd = 'timeout 10'
    else:
        cmd = 'sleep 10'
        
    with pytest.raises(subprocess.TimeoutExpired):
        run_with_timeout(cmd, timeout=1, shell=True)

@pytest.mark.skipif(platform.system() == 'Windows', 
                   reason="Process killing behaves differently on Windows")
def test_kill_process():
    """Test killing a process."""
    # Start a sleep process
    if platform.system() == 'Windows':
        proc = subprocess.Popen(['timeout', '10'], shell=True)
    else:
        proc = subprocess.Popen(['sleep', '10'])
        
    pid = proc.pid
    
    # Try graceful kill
    assert kill_process(pid, force=False)
    time.sleep(0.1)  # Give process time to terminate
    
    with pytest.raises(psutil.NoSuchProcess):
        psutil.Process(pid)
        
    # Test killing non-existent process
    assert not kill_process(999999)

def test_setup_environment(tmp_path):
    """Test environment setup."""
    # Test with Python path
    python_path = sys.executable
    env_vars = {'TEST_VAR': 'test_value'}
    working_dir = tmp_path
    
    env = setup_environment(
        python_path=python_path,
        env_vars=env_vars,
        working_dir=working_dir
    )
    
    assert isinstance(env, dict)
    assert 'TEST_VAR' in env
    assert env['TEST_VAR'] == 'test_value'
    assert str(Path(python_path).parent) in env['PATH']
    assert os.getcwd() == str(working_dir)

def test_process_monitor():
    """Test process monitoring."""
    monitor = ProcessMonitor(interval=1)
    
    # Start monitoring
    monitor.start()
    time.sleep(2)  # Let it collect some data
    monitor.stop()
    
    stats = monitor.get_stats()
    assert isinstance(stats, list)
    assert len(stats) >= 1
    
    # Check stats format
    first_stat = stats[0]
    assert 'timestamp' in first_stat
    assert 'processes' in first_stat
    assert str(os.getpid()) in first_stat['processes']

@patch('shutil.which')
@patch('builtins.__import__')
def test_check_dependencies(mock_import, mock_which):
    """Test dependency checking."""
    # Mock CLI tools
    mock_which.side_effect = lambda x: x in ['git', 'curl']
    
    # Mock Python packages
    def mock_import_side_effect(name):
        if name in ['PIL', 'numpy']:
            return MagicMock()
        raise ImportError
        
    mock_import.side_effect = mock_import_side_effect
    
    deps = check_dependencies()
    
    assert deps['git'] is True
    assert deps['curl'] is True
    assert deps['wget'] is False
    assert deps['PIL'] is True
    assert deps['numpy'] is True
    assert deps['requests'] is False
    assert deps['pytest'] is False 
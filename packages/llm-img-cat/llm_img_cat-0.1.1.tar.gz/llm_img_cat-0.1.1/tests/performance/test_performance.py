"""Performance tests for the LLM Image Categorization package."""
import os
import time
import json
import pytest
import psutil
import asyncio
import statistics
from pathlib import Path
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor

from llm_image_categorizator.api_helpers.llm_apis.gwen import GwenAPI
from llm_image_categorizator.api_helpers.llm_apis.gemini import GeminiAPI
from llm_image_categorizator.api_helpers.llm_apis.gpt import GPTAPI
from llm_image_categorizator.data.storage import SQLiteStorage, CacheStorage
from llm_image_categorizator.utils.testing import create_test_image

# Test data paths
TEST_DATA_DIR = Path(__file__).parent.parent / 'data'
PERF_TEST_DIR = TEST_DATA_DIR / 'performance'
RESULTS_DIR = PERF_TEST_DIR / 'results'

# Test parameters
NUM_IMAGES = 100
NUM_CONCURRENT = 10
CACHE_TTL = 3600

@pytest.fixture(autouse=True)
def setup_test_dirs():
    """Set up test directories."""
    PERF_TEST_DIR.mkdir(exist_ok=True)
    RESULTS_DIR.mkdir(exist_ok=True)
    yield
    # Keep results for analysis

@pytest.fixture
def test_images() -> List[Path]:
    """Create test images for performance testing."""
    images = []
    for i in range(NUM_IMAGES):
        path = PERF_TEST_DIR / f'test_{i}.png'
        create_test_image(path)
        images.append(path)
    return images

@pytest.fixture
def performance_monitor():
    """Create performance monitoring context."""
    class PerfMonitor:
        def __init__(self):
            self.start_time = None
            self.end_time = None
            self.start_memory = None
            self.peak_memory = None
            self.cpu_usage = []
            
        def __enter__(self):
            self.start_time = time.time()
            self.start_memory = psutil.Process().memory_info().rss
            return self
            
        def __exit__(self, *args):
            self.end_time = time.time()
            self.peak_memory = psutil.Process().memory_info().rss
            
        def record_cpu(self):
            self.cpu_usage.append(psutil.cpu_percent())
            
        @property
        def duration(self) -> float:
            return self.end_time - self.start_time
            
        @property
        def memory_used(self) -> int:
            return self.peak_memory - self.start_memory
            
        @property
        def avg_cpu(self) -> float:
            return statistics.mean(self.cpu_usage) if self.cpu_usage else 0
            
        def to_dict(self) -> Dict[str, Any]:
            return {
                'duration_seconds': self.duration,
                'memory_bytes': self.memory_used,
                'peak_memory_bytes': self.peak_memory,
                'avg_cpu_percent': self.avg_cpu,
                'cpu_usage': self.cpu_usage
            }
    
    return PerfMonitor

def save_benchmark_results(name: str, results: Dict[str, Any]):
    """Save benchmark results to JSON file."""
    path = RESULTS_DIR / f'{name}_{time.strftime("%Y%m%d_%H%M%S")}.json'
    with open(path, 'w') as f:
        json.dump(results, f, indent=2)

@pytest.mark.benchmark
def test_sequential_api_performance(
    test_images: List[Path],
    performance_monitor
):
    """Test sequential API performance."""
    apis = {
        'gwen': GwenAPI(),
        'gemini': GeminiAPI(),
        'gpt': GPTAPI()
    }
    
    results = {}
    for api_name, api in apis.items():
        with performance_monitor() as monitor:
            for image in test_images:
                result = api.classify_image(image)
                assert result['success']
                monitor.record_cpu()
                
        results[api_name] = monitor.to_dict()
    
    save_benchmark_results('sequential_api', results)
    
    # Performance assertions
    for api_name, metrics in results.items():
        # Average response time should be under 2 seconds
        avg_time = metrics['duration_seconds'] / NUM_IMAGES
        assert avg_time < 2.0, f"{api_name} average response time too high: {avg_time:.2f}s"
        
        # Memory usage should be reasonable
        memory_mb = metrics['memory_bytes'] / (1024 * 1024)
        assert memory_mb < 500, f"{api_name} memory usage too high: {memory_mb:.1f}MB"

@pytest.mark.benchmark
@pytest.mark.asyncio
async def test_concurrent_api_performance(
    test_images: List[Path],
    performance_monitor
):
    """Test concurrent API performance."""
    apis = {
        'gwen': GwenAPI(),
        'gemini': GeminiAPI(),
        'gpt': GPTAPI()
    }
    
    results = {}
    for api_name, api in apis.items():
        with performance_monitor() as monitor:
            # Process images in batches
            for i in range(0, len(test_images), NUM_CONCURRENT):
                batch = test_images[i:i + NUM_CONCURRENT]
                tasks = [api.classify_image_async(img) for img in batch]
                batch_results = await asyncio.gather(*tasks)
                assert all(r['success'] for r in batch_results)
                monitor.record_cpu()
                
        results[api_name] = monitor.to_dict()
    
    save_benchmark_results('concurrent_api', results)
    
    # Performance assertions
    for api_name, metrics in results.items():
        # Concurrent processing should be significantly faster
        total_time = metrics['duration_seconds']
        sequential_time = results[api_name]['duration_seconds']
        speedup = sequential_time / total_time
        assert speedup > 2.0, f"{api_name} concurrent speedup too low: {speedup:.1f}x"

@pytest.mark.benchmark
def test_storage_performance(test_images: List[Path], performance_monitor):
    """Test storage system performance."""
    db_path = PERF_TEST_DIR / 'test.db'
    cache_dir = PERF_TEST_DIR / 'cache'
    cache_dir.mkdir(exist_ok=True)
    
    storage = SQLiteStorage(db_path)
    cache = CacheStorage(cache_dir)
    
    results = {}
    
    # Test write performance
    with performance_monitor() as monitor:
        with ThreadPoolExecutor(max_workers=NUM_CONCURRENT) as executor:
            def write_record(image):
                result = {
                    'image_path': str(image),
                    'label': 'test_label',
                    'confidence': 0.95
                }
                storage.save_classification_result(result)
                cache.set(str(image), result, ttl=CACHE_TTL)
                monitor.record_cpu()
                
            list(executor.map(write_record, test_images))
            
    results['write'] = monitor.to_dict()
    
    # Test read performance
    with performance_monitor() as monitor:
        with ThreadPoolExecutor(max_workers=NUM_CONCURRENT) as executor:
            def read_record(image):
                # Try cache first
                result = cache.get(str(image))
                if not result:
                    # Fallback to database
                    result = storage.get_classification_result(str(image))
                assert result is not None
                monitor.record_cpu()
                
            list(executor.map(read_record, test_images))
            
    results['read'] = monitor.to_dict()
    
    save_benchmark_results('storage', results)
    
    # Performance assertions
    write_time_per_record = results['write']['duration_seconds'] / NUM_IMAGES
    read_time_per_record = results['read']['duration_seconds'] / NUM_IMAGES
    
    assert write_time_per_record < 0.01, f"Write too slow: {write_time_per_record:.3f}s per record"
    assert read_time_per_record < 0.005, f"Read too slow: {read_time_per_record:.3f}s per record"

@pytest.mark.benchmark
def test_end_to_end_performance(test_images: List[Path], performance_monitor):
    """Test end-to-end system performance."""
    # Initialize components
    gwen_api = GwenAPI()
    db_path = PERF_TEST_DIR / 'test.db'
    cache_dir = PERF_TEST_DIR / 'cache'
    cache_dir.mkdir(exist_ok=True)
    
    storage = SQLiteStorage(db_path)
    cache = CacheStorage(cache_dir)
    
    with performance_monitor() as monitor:
        for image in test_images:
            # Check cache first
            result = cache.get(str(image))
            if not result:
                # Classify image
                result = gwen_api.classify_image(image)
                assert result['success']
                
                # Store result
                storage.save_classification_result(result)
                cache.set(str(image), result, ttl=CACHE_TTL)
            
            monitor.record_cpu()
    
    results = {'end_to_end': monitor.to_dict()}
    save_benchmark_results('end_to_end', results)
    
    # Performance assertions
    time_per_image = results['end_to_end']['duration_seconds'] / NUM_IMAGES
    assert time_per_image < 3.0, f"End-to-end processing too slow: {time_per_image:.2f}s per image"

def test_memory_usage(test_images: List[Path], performance_monitor):
    """Test memory usage under load."""
    gwen_api = GwenAPI()
    
    with performance_monitor() as monitor:
        # Process images in memory
        results = []
        for image in test_images:
            result = gwen_api.classify_image(image)
            results.append(result)
            monitor.record_cpu()
    
    metrics = monitor.to_dict()
    save_benchmark_results('memory_usage', {'memory_test': metrics})
    
    # Memory assertions
    memory_per_image = metrics['memory_bytes'] / NUM_IMAGES
    memory_mb = memory_per_image / (1024 * 1024)
    assert memory_mb < 5.0, f"Memory usage too high: {memory_mb:.1f}MB per image" 
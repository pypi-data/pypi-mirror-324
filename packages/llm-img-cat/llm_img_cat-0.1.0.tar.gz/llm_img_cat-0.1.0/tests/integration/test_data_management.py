"""Integration tests for data management functionality."""
import os
import json
import pytest
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

from llm_image_categorizator.data.models import (
    ImageMetadata,
    ClassificationResult,
    ProcessingRecord,
    DatasetEntry,
    CacheEntry
)
from llm_image_categorizator.data.storage import (
    SQLiteStorage,
    FileStorage,
    CacheStorage
)
from llm_image_categorizator.utils.testing import (
    create_test_image,
    create_test_json
)

# Test data paths
TEST_DATA_DIR = Path(__file__).parent.parent / 'data'
TEST_DB_PATH = TEST_DATA_DIR / 'test.db'
TEST_CACHE_DIR = TEST_DATA_DIR / 'cache'
TEST_FILES_DIR = TEST_DATA_DIR / 'files'

@pytest.fixture(autouse=True)
def setup_test_dirs():
    """Set up test directories."""
    TEST_DATA_DIR.mkdir(exist_ok=True)
    TEST_CACHE_DIR.mkdir(exist_ok=True)
    TEST_FILES_DIR.mkdir(exist_ok=True)
    yield
    # Cleanup
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()
    for path in TEST_CACHE_DIR.glob('*'):
        path.unlink()
    for path in TEST_FILES_DIR.glob('*'):
        path.unlink()

@pytest.fixture
def sqlite_storage():
    """Create SQLite storage instance."""
    storage = SQLiteStorage(TEST_DB_PATH)
    storage.initialize()
    return storage

@pytest.fixture
def file_storage():
    """Create file storage instance."""
    return FileStorage(TEST_FILES_DIR)

@pytest.fixture
def cache_storage():
    """Create cache storage instance."""
    return CacheStorage(TEST_CACHE_DIR)

def test_image_metadata_crud(sqlite_storage):
    """Test CRUD operations for image metadata."""
    # Create test data
    metadata = ImageMetadata(
        image_path='test.jpg',
        size_bytes=1024,
        dimensions=(100, 100),
        format='JPEG',
        created_at=datetime.now(),
        hash='abc123'
    )
    
    # Create
    metadata_id = sqlite_storage.save_image_metadata(metadata)
    assert metadata_id is not None
    
    # Read
    saved_metadata = sqlite_storage.get_image_metadata(metadata_id)
    assert saved_metadata.image_path == metadata.image_path
    assert saved_metadata.size_bytes == metadata.size_bytes
    assert saved_metadata.dimensions == metadata.dimensions
    
    # Update
    metadata.size_bytes = 2048
    sqlite_storage.update_image_metadata(metadata_id, metadata)
    updated = sqlite_storage.get_image_metadata(metadata_id)
    assert updated.size_bytes == 2048
    
    # Delete
    sqlite_storage.delete_image_metadata(metadata_id)
    assert sqlite_storage.get_image_metadata(metadata_id) is None

def test_classification_result_crud(sqlite_storage):
    """Test CRUD operations for classification results."""
    # Create test data
    result = ClassificationResult(
        image_id=1,
        model='gwen',
        label='book_cover',
        confidence=0.95,
        processing_time=0.5,
        created_at=datetime.now()
    )
    
    # Create
    result_id = sqlite_storage.save_classification_result(result)
    assert result_id is not None
    
    # Read
    saved_result = sqlite_storage.get_classification_result(result_id)
    assert saved_result.model == result.model
    assert saved_result.label == result.label
    assert abs(saved_result.confidence - result.confidence) < 0.001
    
    # Update
    result.confidence = 0.98
    sqlite_storage.update_classification_result(result_id, result)
    updated = sqlite_storage.get_classification_result(result_id)
    assert abs(updated.confidence - 0.98) < 0.001
    
    # Delete
    sqlite_storage.delete_classification_result(result_id)
    assert sqlite_storage.get_classification_result(result_id) is None

def test_processing_record_crud(sqlite_storage):
    """Test CRUD operations for processing records."""
    # Create test data
    record = ProcessingRecord(
        image_id=1,
        status='completed',
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(seconds=1),
        error=None
    )
    
    # Create
    record_id = sqlite_storage.save_processing_record(record)
    assert record_id is not None
    
    # Read
    saved_record = sqlite_storage.get_processing_record(record_id)
    assert saved_record.status == record.status
    assert saved_record.error == record.error
    
    # Update
    record.status = 'failed'
    record.error = 'API error'
    sqlite_storage.update_processing_record(record_id, record)
    updated = sqlite_storage.get_processing_record(record_id)
    assert updated.status == 'failed'
    assert updated.error == 'API error'
    
    # Delete
    sqlite_storage.delete_processing_record(record_id)
    assert sqlite_storage.get_processing_record(record_id) is None

def test_file_storage(file_storage):
    """Test file storage operations."""
    # Create test files
    image_path = TEST_FILES_DIR / 'test.png'
    create_test_image(image_path)
    
    json_path = TEST_FILES_DIR / 'test.json'
    test_data = {'test': True}
    create_test_json(json_path, test_data)
    
    # Test file operations
    assert file_storage.exists('test.png')
    assert file_storage.exists('test.json')
    
    # Read files
    with file_storage.open('test.json', 'r') as f:
        data = json.load(f)
    assert data == test_data
    
    # Delete files
    file_storage.delete('test.png')
    file_storage.delete('test.json')
    assert not file_storage.exists('test.png')
    assert not file_storage.exists('test.json')

def test_cache_storage(cache_storage):
    """Test cache storage operations."""
    # Test data
    key = 'test_key'
    data = {'result': 'test_value'}
    
    # Set cache
    cache_storage.set(key, data, ttl=60)
    assert cache_storage.exists(key)
    
    # Get cache
    cached_data = cache_storage.get(key)
    assert cached_data == data
    
    # Test expiration
    cache_storage.set(key, data, ttl=1)
    import time
    time.sleep(2)
    assert not cache_storage.exists(key)
    assert cache_storage.get(key) is None
    
    # Delete cache
    cache_storage.set(key, data)
    assert cache_storage.exists(key)
    cache_storage.delete(key)
    assert not cache_storage.exists(key)

def test_data_migration(sqlite_storage, file_storage):
    """Test data migration functionality."""
    # Create test data
    num_records = 10
    records = []
    
    for i in range(num_records):
        # Create image and metadata
        image_path = TEST_FILES_DIR / f'test_{i}.png'
        create_test_image(image_path)
        
        metadata = ImageMetadata(
            image_path=str(image_path),
            size_bytes=1024,
            dimensions=(100, 100),
            format='PNG',
            created_at=datetime.now(),
            hash=f'hash_{i}'
        )
        metadata_id = sqlite_storage.save_image_metadata(metadata)
        
        # Create classification result
        result = ClassificationResult(
            image_id=metadata_id,
            model='gwen',
            label='book_cover',
            confidence=0.95,
            processing_time=0.5,
            created_at=datetime.now()
        )
        result_id = sqlite_storage.save_classification_result(result)
        
        records.append((metadata_id, result_id))
    
    # Export data
    export_path = TEST_FILES_DIR / 'export.json'
    sqlite_storage.export_data(export_path)
    
    # Clear database
    sqlite_storage.clear_all()
    
    # Import data
    sqlite_storage.import_data(export_path)
    
    # Verify imported data
    for metadata_id, result_id in records:
        # Check metadata
        metadata = sqlite_storage.get_image_metadata(metadata_id)
        assert metadata is not None
        assert metadata.image_path.startswith(str(TEST_FILES_DIR))
        
        # Check result
        result = sqlite_storage.get_classification_result(result_id)
        assert result is not None
        assert result.model == 'gwen'
        assert result.label == 'book_cover'

def test_concurrent_access(sqlite_storage):
    """Test concurrent database access."""
    import threading
    
    def worker(worker_id):
        # Create test data
        metadata = ImageMetadata(
            image_path=f'test_{worker_id}.jpg',
            size_bytes=1024,
            dimensions=(100, 100),
            format='JPEG',
            created_at=datetime.now(),
            hash=f'hash_{worker_id}'
        )
        
        # Save metadata
        metadata_id = sqlite_storage.save_image_metadata(metadata)
        assert metadata_id is not None
        
        # Read metadata
        saved = sqlite_storage.get_image_metadata(metadata_id)
        assert saved.image_path == metadata.image_path
    
    # Create threads
    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
    
    # Wait for all threads
    for t in threads:
        t.join()
        
    # Verify all records
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM image_metadata')
    count = cursor.fetchone()[0]
    assert count == 10
    conn.close() 
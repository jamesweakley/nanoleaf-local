#!/usr/bin/env python3
"""
Basic import and instantiation test for the nanoleaf_coap module.
This test does not require actual hardware or environment variables.
"""
import sys

def test_import():
    """Test that the module can be imported."""
    try:
        import nanoleaf_coap
        print("✓ Module import successful")
        return True
    except ImportError as e:
        print(f"✗ Module import failed: {e}")
        return False

def test_class_exists():
    """Test that the NanoleafCoAPClient class exists."""
    try:
        from nanoleaf_coap import NanoleafCoAPClient
        print("✓ NanoleafCoAPClient class found")
        return True
    except ImportError as e:
        print(f"✗ NanoleafCoAPClient class not found: {e}")
        return False

def test_instantiation():
    """Test that the client can be instantiated."""
    try:
        from nanoleaf_coap import NanoleafCoAPClient
        client = NanoleafCoAPClient("fe80::1", "test-token")
        print("✓ Client instantiation successful")
        print(f"  - IPv6 address: {client.ipv6_address}")
        print(f"  - Access token: {'*' * len(client.access_token)}")
        return True
    except Exception as e:
        print(f"✗ Client instantiation failed: {e}")
        return False

def test_uri_building():
    """Test that URIs are built correctly."""
    try:
        from nanoleaf_coap import NanoleafCoAPClient
        client = NanoleafCoAPClient("fe80::1234:5678:90ab:cdef", "token")
        uri = client._build_uri("/api/v1/info")
        expected = "coap://[fe80::1234:5678:90ab:cdef]/api/v1/info"
        if uri == expected:
            print(f"✓ URI building correct: {uri}")
            return True
        else:
            print(f"✗ URI building incorrect")
            print(f"  Expected: {expected}")
            print(f"  Got: {uri}")
            return False
    except Exception as e:
        print(f"✗ URI building test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Running basic tests for nanoleaf_coap module...")
    print("=" * 60)
    
    tests = [
        test_import,
        test_class_exists,
        test_instantiation,
        test_uri_building,
    ]
    
    results = [test() for test in tests]
    
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

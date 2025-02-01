from satya import StreamValidator
import time

def generate_data():
    """Generator that simulates streaming data with delays"""
    print("Starting stream...")
    for i in range(5):
        data = {
            "name": f"Person_{i}",
            "age": 20 + i,
            "active": i % 2 == 0
        }
        print(f"Generating item {i}: {data}")
        time.sleep(1)  # Simulate network/database delay
        yield data

# Create validator
validator = StreamValidator()
validator.add_field("name", str)
validator.add_field("age", int)
validator.add_field("active", bool)

# Process stream
print("Starting validation...")
for valid_item in validator.validate_stream(generate_data()):
    print(f"Validated item: {valid_item}")
    # Process the validated item here... 
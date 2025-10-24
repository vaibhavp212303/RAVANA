import json
import time
from datetime import datetime
from core.system_monitor import SystemMonitor
from core.test_case_generator import TestCaseGenerator
from core.test_case_parser import TestCaseParser
from config.settings import OUTPUT_DIR

if __name__ == "__main__":
    # Example input requirement
    from requirements.sample_requirement import requirement  # you can externalize this

    version = "v2"
    mode = "batch"

    monitor = SystemMonitor()
    generator = TestCaseGenerator()

    monitor.start()
    start_time = time.time()

    try:
        outputs = (
            [generator.generate_batch(requirement, version)]
            if mode == "batch"
            else generator.generate_parallel(requirement, version, num_cases=2)
        )

        response_time = round(time.time() - start_time, 2)
        structured_cases = [case for out in outputs for case in TestCaseParser.parse_json_or_text(out)]

        monitor.stop()

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename_json = f"{OUTPUT_DIR}/testcase_{version}_{mode}_{timestamp}.json"

        with open(filename_json, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "version": version,
                "mode": mode,
                "response_time_seconds": response_time,
                "structured_test_cases": structured_cases,
                "system_stats": monitor.stats_list
            }, f, indent=2)

        print(f"✅ Saved output to {filename_json}")

    except Exception as e:
        monitor.stop()
        print(f"❌ Error: {e}")

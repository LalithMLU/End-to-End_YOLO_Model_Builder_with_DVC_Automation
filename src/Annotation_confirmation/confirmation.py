import sys

# Prompt the user
response = input("Is the annotation completed? (yes/no): ").strip().lower()

if response == "yes":
    print("✅ Annotation is completed. Proceeding with the pipeline...")
elif response == "no":
    print("❌ Annotation is pending! Hence terminating...")
    sys.exit(1)  # Exit with non-zero to stop the pipeline

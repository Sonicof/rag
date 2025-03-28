from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import os
from huggingface_hub import snapshot_download

print("Starting model loading process...")

model_name = "facebook/opt-350m"  # Better model for explanations

# Check if CUDA is available
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
    print(f"Available GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

# Check if model is in cache
cache_dir = os.path.expanduser("~/.cache/huggingface/hub")
model_cache_path = os.path.join(cache_dir, f"models--{model_name.replace('/', '--')}")

if os.path.exists(model_cache_path):
    print(f"\nModel found in cache at: {model_cache_path}")
    use_cache = True
else:
    print(f"\nModel not found in cache. Will download to: {model_cache_path}")
    use_cache = False

print("\nLoading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    local_files_only=use_cache
)

print("\nLoading model...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.float16,  # Use half precision to save memory
    low_cpu_mem_usage=True,  # Optimize memory usage
    local_files_only=use_cache
)

print("\nCreating pipeline...")
pipe = pipeline(
    "text-generation", 
    model=model, 
    tokenizer=tokenizer,
    max_length=200,  # Shorter max length to prevent repetition
    min_length=50,   # Minimum length for coherent response
    temperature=0.7,  # Balanced creativity
    top_p=0.9,       # Nucleus sampling
    top_k=40,        # Top-k sampling
    do_sample=True,  # Enable sampling
    num_return_sequences=1,  # Generate one response
    pad_token_id=tokenizer.eos_token_id,  # Proper padding
    repetition_penalty=1.2,  # Prevent repetition
    no_repeat_ngram_size=3,  # Prevent repeating 3-word sequences
    early_stopping=True     # Stop when response is complete
)

print("\nTesting the model...")
response = pipe("What is Retrival Argumented Generation?", max_length=200)
print("Response:", response)

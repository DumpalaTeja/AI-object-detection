import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

from transformers import pipeline

# ✅ GLOBAL (must be outside function)
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-small"
)

def generate_summary(detections):
    count = len(detections)

    if count < 100:
        density = "low"
    elif count < 1000:
        density = "medium"
    else:
        density = "high"

    prompt = f"""
    Wheat field analysis:
    Total wheat heads: {count}
    Density: {density}

    Provide a 2 sentence agricultural insight.
    """

    try:
        result = generator(prompt, max_length=80)
        return result[0]["generated_text"].strip()
    except Exception:
        return f"Detected {count} wheat heads. Crop density is {density}."